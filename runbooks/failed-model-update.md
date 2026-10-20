# Runbook: Model update failed its smoke test

## Symptoms
The rollout script reports `rolled_back`, or the deployment does not become Ready.

## Diagnose
1. Read `results/rollout.log` for the step that failed.
2. Confirm the previous version is serving with a test request to `/health`.
3. Check the new model's name and version against the change record.

## Decide
- If the new model failed to load, fix the name or access and retry in a test environment first.
- If the smoke test failed, compare the output with the expected behavior before retrying.

## Fix or roll back
1. Keep the previous version active.
2. Do not retry in production until the cause is known.

## Verify
Run the smoke test again against the active version and confirm `ok=True`.

## After the incident
Record the model version, the failing step, the log entry, and whether the change should be retried.
