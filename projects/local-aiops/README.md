# Local No-AWS AIOps Assistant

This folder contains a local AIOps health analyzer for the boutique microservices project.

The original project uses AWS Bedrock for AIOps. This version provides a No-AWS alternative that runs locally against a Minikube Kubernetes cluster.

## What it checks

- Argo CD sync and health status
- Boutique namespace pod health
- Pod restart counts
- CrashLoopBackOff, Error, or unhealthy pod states
- Recent Kubernetes events
- A Markdown incident-style health report

## Run

PowerShell command:

python .\projects\local-aiops\aiops_health_check.py

## Output

The script generates:

projects/local-aiops/reports/cluster-health-report.md

## Example statuses

- HEALTHY: Application is running normally
- WATCH: Application is running, but restart counts or warnings need monitoring
- ATTENTION_REQUIRED: One or more components are unhealthy
