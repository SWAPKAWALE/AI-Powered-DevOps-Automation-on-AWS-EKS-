import json
import subprocess
from datetime import datetime
from pathlib import Path


NAMESPACE = "boutique"
ARGOCD_NAMESPACE = "argocd"
ARGOCD_APP = "boutique-minikube"


def run_command(command):
    """Run a shell command and return stdout, stderr, and exit code."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def get_json(command):
    """Run kubectl command and parse JSON output."""
    stdout, stderr, code = run_command(command)
    if code != 0:
        return None, stderr
    try:
        return json.loads(stdout), None
    except json.JSONDecodeError:
        return None, "Unable to parse JSON output"


def analyze_argocd():
    app, error = get_json(
        f"kubectl get application {ARGOCD_APP} -n {ARGOCD_NAMESPACE} -o json"
    )

    if error:
        return {
            "status": "UNKNOWN",
            "summary": f"Unable to read Argo CD application: {error}"
        }

    sync_status = app.get("status", {}).get("sync", {}).get("status", "Unknown")
    health_status = app.get("status", {}).get("health", {}).get("status", "Unknown")
    revision = app.get("status", {}).get("sync", {}).get("revision", "Unknown")

    if sync_status == "Synced" and health_status == "Healthy":
        status = "HEALTHY"
    else:
        status = "ATTENTION_REQUIRED"

    return {
        "status": status,
        "sync_status": sync_status,
        "health_status": health_status,
        "revision": revision,
        "summary": f"Argo CD application is {sync_status} and {health_status}."
    }


def analyze_pods():
    pods, error = get_json(f"kubectl get pods -n {NAMESPACE} -o json")

    if error:
        return {
            "status": "UNKNOWN",
            "summary": f"Unable to read pods: {error}",
            "pods": []
        }

    pod_results = []
    unhealthy = []
    total_restarts = 0

    for pod in pods.get("items", []):
        name = pod["metadata"]["name"]
        phase = pod["status"].get("phase", "Unknown")

        container_statuses = pod["status"].get("containerStatuses", [])
        ready_containers = 0
        total_containers = len(container_statuses)
        restarts = 0
        waiting_reason = ""

        for container in container_statuses:
            if container.get("ready"):
                ready_containers += 1

            restarts += container.get("restartCount", 0)

            state = container.get("state", {})
            if "waiting" in state:
                waiting_reason = state["waiting"].get("reason", "")

        total_restarts += restarts

        if phase == "Succeeded":
            is_healthy = True
        else:
            is_healthy = (
                phase == "Running"
                and ready_containers == total_containers
                and total_containers > 0
                and waiting_reason == ""
            )

        pod_info = {
            "name": name,
            "phase": phase,
            "ready": f"{ready_containers}/{total_containers}",
            "restarts": restarts,
            "waiting_reason": waiting_reason,
            "healthy": is_healthy
        }

        pod_results.append(pod_info)

        if not is_healthy:
            unhealthy.append(pod_info)

    if unhealthy:
        status = "ATTENTION_REQUIRED"
        summary = f"{len(unhealthy)} unhealthy pod(s) found."
    elif total_restarts > 10:
        status = "WATCH"
        summary = f"All pods are running, but restart count is high: {total_restarts}."
    else:
        status = "HEALTHY"
        summary = "All pods are running and ready."

    return {
        "status": status,
        "summary": summary,
        "pods": pod_results,
        "unhealthy": unhealthy,
        "total_restarts": total_restarts
    }


def get_recent_events():
    stdout, stderr, code = run_command(
        f"kubectl get events -n {NAMESPACE} --sort-by=.lastTimestamp"
    )

    if code != 0:
        return f"Unable to read events: {stderr}"

    lines = stdout.splitlines()
    if len(lines) <= 1:
        return "No recent events found."

    return "\n".join(lines[-15:])


def generate_report():
    argocd = analyze_argocd()
    pods = analyze_pods()
    events = get_recent_events()

    overall_status = "HEALTHY"
    if argocd["status"] != "HEALTHY" or pods["status"] == "ATTENTION_REQUIRED":
        overall_status = "ATTENTION_REQUIRED"
    elif pods["status"] == "WATCH":
        overall_status = "WATCH"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = []
    report.append("# Local AIOps Kubernetes Health Report")
    report.append("")
    report.append(f"Generated at: {now}")
    report.append("")
    report.append(f"Overall status: **{overall_status}**")
    report.append("")
    report.append("## Argo CD Status")
    report.append("")
    report.append(f"- Status: {argocd.get('status')}")
    report.append(f"- Sync: {argocd.get('sync_status', 'Unknown')}")
    report.append(f"- Health: {argocd.get('health_status', 'Unknown')}")
    report.append(f"- Revision: {argocd.get('revision', 'Unknown')}")
    report.append(f"- Summary: {argocd.get('summary')}")
    report.append("")
    report.append("## Boutique Pod Status")
    report.append("")
    report.append(f"- Status: {pods.get('status')}")
    report.append(f"- Summary: {pods.get('summary')}")
    report.append(f"- Total restarts: {pods.get('total_restarts')}")
    report.append("")
    report.append("| Pod | Phase | Ready | Restarts | Waiting Reason |")
    report.append("|---|---|---:|---:|---|")

    for pod in pods.get("pods", []):
        report.append(
            f"| {pod['name']} | {pod['phase']} | {pod['ready']} | "
            f"{pod['restarts']} | {pod['waiting_reason'] or '-'} |"
        )

    report.append("")
    report.append("## AIOps Recommendation")
    report.append("")

    if overall_status == "HEALTHY":
        report.append("The application is healthy. No immediate action is required.")
    elif overall_status == "WATCH":
        report.append(
            "The application is currently running, but restart counts are elevated. "
            "Monitor pods and check logs if restarts continue."
        )
    else:
        report.append(
            "One or more components need attention. Check unhealthy pod logs using "
            "`kubectl logs <pod-name> -n boutique` and review recent Kubernetes events."
        )

    report.append("")
    report.append("## Recent Kubernetes Events")
    report.append("")
    report.append("```text")
    report.append(events)
    report.append("```")
    report.append("")

    output_path = Path("projects/local-aiops/reports/cluster-health-report.md")
    output_path.write_text("\n".join(report), encoding="utf-8")

    print(f"AIOps report generated: {output_path}")
    print(f"Overall status: {overall_status}")


if __name__ == "__main__":
    generate_report()
