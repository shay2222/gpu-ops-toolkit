# Runbook: Pod in CrashLoopBackOff from out-of-memory errors

## Symptoms
A pod restarts repeatedly, and its status shows CrashLoopBackOff.

## Diagnose
1. Run `kubectl describe pod <pod>` and look for `OOMKilled` under Last State.
2. Run `kubectl logs <pod> --previous` to see the last crash.
3. Compare the memory limit with the model's memory need.

## Decide
- If the limit is too low for the model, raise it.
- If the model is too large for the GPU, use a smaller model or a quantized version.

## Fix or roll back
1. Roll back to the previous image: `kubectl rollout undo deployment/llm-server`.
2. Then make the change in the manifest and redeploy through the normal change process.

## Verify
Run `kubectl get pods` and confirm the pod is Running and Ready for at least 10 minutes.

## After the incident
Record the pod name, the cause, the limit that was changed, and the follow-up to set memory limits in the manifest.
