import datetime, os, time, torch
from transformers import pipeline

LOG = "results/rollout.log"

def log(msg):
    os.makedirs("results", exist_ok=True)
    line = f"{datetime.datetime.utcnow().isoformat()}Z {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def load(model_id):
    return pipeline("text-generation", model=model_id,
                    torch_dtype=torch.float16, device=0)

def smoke_test(pipe):
    start = time.time()
    out = pipe("Say hello in one word.", max_new_tokens=8, do_sample=False)
    text = out[0]["generated_text"]
    ms = (time.time() - start) * 1000
    ok = len(text.strip()) > 0 and ms < 30000
    return ok, ms, text

def rollout(new_id, previous_id):
    """Returns (pipe, active_model_id, outcome)."""
    log(f"deploy start: {new_id} (previous: {previous_id})")
    pipe = None
    try:
        pipe = load(new_id)
        ok, ms, _ = smoke_test(pipe)
        log(f"smoke test ok={ok} latency_ms={ms:.0f}")
        if ok:
            log(f"deployed {new_id}")
            return pipe, new_id, "deployed"
        raise RuntimeError("smoke test failed")
    except Exception as e:
        log(f"rolling back to {previous_id}: {e}")
        del pipe
        torch.cuda.empty_cache()
        pipe = load(previous_id)
        ok, ms, _ = smoke_test(pipe)
        log(f"rollback smoke test ok={ok} latency_ms={ms:.0f}")
        return pipe, previous_id, "rolled_back"
