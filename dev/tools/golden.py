#!/usr/bin/env python3
"""Golden regression + determinism + size budget for every generator.
  python3 dev/tools/golden.py            check against dev/golden.json (exit 1 on any drift, refusal change or >25% size growth)
  python3 dev/tools/golden.py --update   regenerate golden.json (runs everything twice and demands identical output)
  python3 dev/tools/golden.py --dump DIR write every --widget fragment to DIR (for the browser host test)"""
import hashlib, json, shlex, subprocess, sys, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[2]; MV = ROOT/"vizualize/scripts/mv.py"; GOLD = ROOT/"dev/golden.json"
def cmds():
    for ln in (ROOT/"dev/golden_cmds.txt").read_text().splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            refuse = ln.startswith("!"); body, _, msg = ln.lstrip("!").partition(" ::")
            yield refuse, shlex.split(body), msg.strip()
def run(args, widget):
    return subprocess.run([sys.executable, str(MV), *args, *(["--widget"] if widget else [])], capture_output=True, text=True, timeout=120)
def key(args): return " ".join(shlex.quote(a) for a in args)
def snapshot():
    out = {}
    for refuse, args, msg in cmds():
        k = key(args)
        if refuse:
            r = run(args, False); assert r.returncode != 0, f"expected refusal: {k}"; assert msg in r.stderr, f"{k}: expected '{msg}' in stderr, got: {r.stderr[-200:]}"; out["!" + k] = {"msg": msg}; continue
        ent = {}
        for w in (False, True):
            r = run(args, w); assert r.returncode == 0, f"{k} {'--widget' if w else ''}: {r.stderr[-300:]}"
            ent["widget" if w else "plain"] = [hashlib.sha256(r.stdout.encode()).hexdigest()[:16], len(r.stdout)]
        out[k] = ent
    return out
def main():
    a = sys.argv[1:]
    if a[:1] == ["--dump"]:
        d = pathlib.Path(a[1]); d.mkdir(parents=True, exist_ok=True)
        for i, (refuse, args, _) in enumerate(cmds()):
            if refuse: continue
            r = run(args, True); name = ("slider-" if args[0] == "slider" else "g%03d-" % i) + re.sub(r"[^A-Za-z0-9]+", "_", key(args))[:40] + ".frag"; (d/name).write_text(r.stdout)
        print("dumped", len(list(d.glob("*.frag"))), "fragments"); return 0
    cur = snapshot()
    if a[:1] == ["--update"]:
        again = snapshot(); assert cur == again, "non-deterministic output: " + ", ".join(k for k in cur if cur[k] != again[k]); GOLD.write_text(json.dumps(cur, indent=1, sort_keys=True)); print("golden updated:", len(cur), "entries, deterministic ✓"); return 0
    gold = json.loads(GOLD.read_text()); bad = []
    for k in sorted(set(gold) | set(cur)):
        if k not in gold: bad.append(f"NEW      {k}"); continue
        if k not in cur: bad.append(f"MISSING  {k}"); continue
        for v in ("plain", "widget"):
            if v in gold[k] and cur[k][v][0] != gold[k][v][0]:
                g, c = gold[k][v][1], cur[k][v][1]; bad.append(f"CHANGED  {k} [{v}] {g} -> {c} bytes" + ("  (+%d%% SIZE GROWTH)" % round(100*(c-g)/g) if c > 1.25*g else ""))
    print("\n".join(bad) if bad else f"golden: {len(cur)} entries identical ✓"); return 1 if bad else 0
if __name__ == "__main__": sys.exit(main())
