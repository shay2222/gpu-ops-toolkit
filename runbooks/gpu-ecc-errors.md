# Runbook: GPU reports uncorrected ECC errors

## Symptoms
A health check reports uncorrected ECC errors, or a job fails with a GPU memory error.

## Diagnose
1. Run `nvidia-smi -q -d ECC` and note the uncorrected counts.
2. Run `python gpu/gpu_health.py` and confirm the status is `fail`.
3. Check whether the errors are increasing between runs.

## Decide
- If the count is 0 and the status is `pass`, close the alert.
- If the count is above 0, drain the node so no new work lands on it.

## Fix or roll back
1. Cordon the node: `kubectl cordon <node>`.
2. Drain running work: `kubectl drain <node> --ignore-daemonsets`.
3. Open a hardware ticket with the GPU index, the error count, and the time.

## Verify
Confirm the workloads moved to healthy nodes with `kubectl get pods -o wide`, and that the failing node is cordoned.

## After the incident
Record the time, the GPU ID, the error count, the action taken, and a follow-up item to check the replacement.
