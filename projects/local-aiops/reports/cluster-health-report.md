# Local AIOps Kubernetes Health Report

Generated at: 2026-07-14 14:52:59

Overall status: **WATCH**

## Argo CD Status

- Status: HEALTHY
- Sync: Synced
- Health: Healthy
- Revision: 5ef48d8c3c8eaff6701ceb7ac34ccd5f9322e91d
- Summary: Argo CD application is Synced and Healthy.

## Boutique Pod Status

- Status: WATCH
- Summary: All pods are running, but restart count is high: 22.
- Total restarts: 22

| Pod | Phase | Ready | Restarts | Waiting Reason |
|---|---|---:|---:|---|
| auth-6bb4446457-lq25k | Running | 1/1 | 0 | - |
| boutique-db-restore-qr6gl | Succeeded | 0/1 | 0 | - |
| boutique-postgres-0 | Running | 1/1 | 1 | - |
| frontend-7dd4c8d7bc-z2fnh | Running | 1/1 | 1 | - |
| gateway-778f96db6-z6kg8 | Running | 1/1 | 1 | - |
| order-service-7757445555-wr2tp | Running | 1/1 | 6 | - |
| orders-5b54fc7b69-2k9ps | Running | 1/1 | 6 | - |
| product-service-7cb9b6c576-j2cbb | Running | 1/1 | 7 | - |
| user-service-64b59c9bfb-gp7pv | Running | 1/1 | 0 | - |

## AIOps Recommendation

The application is currently running, but restart counts are elevated. Monitor pods and check logs if restarts continue.

## Recent Kubernetes Events

```text
14m         Normal    Scheduled           pod/user-service-64b59c9bfb-gp7pv       Successfully assigned boutique/user-service-64b59c9bfb-gp7pv to minikube
14m         Normal    Scheduled           pod/auth-6bb4446457-lq25k               Successfully assigned boutique/auth-6bb4446457-lq25k to minikube
14m         Normal    Created             pod/auth-6bb4446457-lq25k               Created container: auth
14m         Normal    Pulled              pod/user-service-64b59c9bfb-gp7pv       Container image "boutique-user-service:local" already present on machine
14m         Normal    Created             pod/user-service-64b59c9bfb-gp7pv       Created container: user-service
14m         Normal    Pulled              pod/auth-6bb4446457-lq25k               Container image "boutique-auth:local" already present on machine
14m         Normal    Started             pod/auth-6bb4446457-lq25k               Started container auth
14m         Normal    Started             pod/user-service-64b59c9bfb-gp7pv       Started container user-service
14m         Normal    ScalingReplicaSet   deployment/user-service                 Scaled down replica set user-service-5bd6b7bbb6 from 1 to 0
14m         Normal    Killing             pod/user-service-5bd6b7bbb6-dd84p       Stopping container user-service
14m         Normal    SuccessfulDelete    replicaset/user-service-5bd6b7bbb6      Deleted pod: user-service-5bd6b7bbb6-dd84p
14m         Normal    ScalingReplicaSet   deployment/auth                         Scaled down replica set auth-86985b897f from 1 to 0
14m         Normal    Killing             pod/auth-86985b897f-kzvsf               Stopping container auth
14m         Normal    SuccessfulDelete    replicaset/auth-86985b897f              Deleted pod: auth-86985b897f-kzvsf
113s        Warning   Unhealthy           pod/boutique-postgres-0                 Readiness probe failed: command timed out: "sh -c pg_isready -U postgres" timed out after 1s
```
