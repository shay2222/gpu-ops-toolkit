import json, subprocess, sys, os

FIELDS = ["index", "name", "temperature.gpu", "utilization.gpu",
          "memory.used", "memory.total", "power.draw",
          "ecc.errors.uncorrected.volatile.total"]
TEMP_WARN, TEMP_FAIL = 80, 88

def query_gpus():
    out = subprocess.run(
        ["nvidia-smi", f"--query-gpu={','.join(FIELDS)}",
         "--format=csv,noheader,nounits"],
        capture_output=True, text=True, check=True).stdout
    rows = []
    for line in out.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        rows.append(dict(zip(FIELDS, parts)))
    return rows

def value(raw):
    return None if raw in ("[N/A]", "N/A", "") else raw

def assess(g):
    problems = []
    temp = value(g["temperature.gpu"])
    ecc = value(g["ecc.errors.uncorrected.volatile.total"])
    if temp is not None:
        t = float(temp)
        if t >= TEMP_FAIL:
            problems.append(("fail", f"temperature {t:.0f} C"))
        elif t >= TEMP_WARN:
            problems.append(("warn", f"temperature {t:.0f} C"))
    if ecc is None:
        problems.append(("warn", "ECC errors not reported"))
    elif int(ecc) > 0:
        problems.append(("fail", f"{ecc} uncorrected ECC errors"))
    if any(p[0] == "fail" for p in problems):
        status = "fail"
    elif problems:
        status = "warn"
    else:
        status = "pass"
    return {"gpu": g["index"], "name": g["name"], "status": status,
            "problems": [p[1] for p in problems], "raw": g}

if __name__ == "__main__":
    report = [assess(g) for g in query_gpus()]
    os.makedirs("results", exist_ok=True)
    with open("results/gpu_health.json", "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps([{k: r[k] for k in ("gpu", "name", "status", "problems")}
                      for r in report], indent=2))
    # Non-zero exit when any GPU fails, so automation can react
    sys.exit(1 if any(r["status"] == "fail" for r in report) else 0)
