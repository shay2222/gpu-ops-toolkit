# gpu-ops-toolkit

Tools and runbooks for operating GPU clusters and LLM deployments: GPU health checks, a safe model rollout with rollback, Kubernetes manifests, and incident runbooks.

## What's in the repo

| Part | File | What was verified |
|---|---|---|
| GPU health checker | `gpu/gpu_health.py` | Ran on Tesla T4 (Colab); reported status per GPU; load test run before and after |
| Rollout with rollback | `rollout/rollout.py` | Passed on a valid model; rolled back on a missing model |
| Kubernetes manifests | `k8s/model-server.yaml` | Validated with kubeconform in strict mode via GitHub Actions: 2 resources, 0 invalid, 0 skipped |
| Runbooks | `runbooks/` | Written from standard procedures; not tested on a live incident |

## Limitations
- Tested on a single Tesla T4 in Colab. No A100, V100, H100, or B200 testing.
- Kubernetes files were validated, not deployed to a live cluster.
- The image name in the manifest is a placeholder.
- The runbooks are written procedures, not practiced incident responses.
- The rollout smoke test checks that the model loads and answers. It does not measure output quality.
