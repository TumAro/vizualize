#!/usr/bin/env python3
"""One-command quality gate.  python3 dev/check.py
Always: unit/certificate tests (test_mv.py), golden regression (all 139 commands, plain+widget, determinism, size budget).
With a browser (set PW_MODULE=<.../node_modules/playwright> and PLAYWRIGHT_BROWSERS_PATH, see dev/ROADMAP.md): every widget fragment is injected into a
simulated claude.ai host in light+dark and checked for console errors; every slider demo sweeps 500 random states (invariant badge); JS expression evaluator vs Python cmath parity."""
import json, os, pathlib, random, subprocess, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[1]; PY = sys.executable; fails = []
def step(name, cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw); ok = r.returncode == 0
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else "\n" + (r.stdout + r.stderr)[-1500:]))
    if not ok: fails.append(name)
    return r
step("certificate tests (test_mv.py)", [PY, str(ROOT/"vizualize/scripts/test_mv.py")], cwd=ROOT/"vizualize/scripts")
step("golden regression + determinism + size budget", [PY, str(ROOT/"dev/tools/golden.py")])
if os.environ.get("PW_MODULE"):
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t); (t/"frag").mkdir(); (t/"png").mkdir(); (t/"html").mkdir(); (t/"png2").mkdir()
        subprocess.run([PY, str(ROOT/"dev/tools/golden.py"), "--dump", str(t/"frag")], check=True, capture_output=True)
        r = step("browser: all widget fragments, light+dark host", ["node", str(ROOT/"dev/tools/widget_host.js"), str(t/"frag"), str(t/"png")]); print("      ", len([l for l in r.stdout.splitlines() if l.startswith("ok")]), "page checks")
        for n in "pythagoras quadratic sine taylor epsdelta eigen riemann".split():
            (t/"html"/f"{n}.html").write_text(subprocess.run([PY, str(ROOT/"vizualize/scripts/mv.py"), "slider", n], capture_output=True, text=True).stdout)
        step("browser: slider invariant sweeps (500 random states each)", ["node", str(ROOT/"dev/tools/test_sliders.js"), str(t/"html"), str(t/"png2")])
        sys.path.insert(0, str(ROOT/"vizualize/scripts")); import cplx
        (t/"lib.js").write_text(cplx.JSLIB); random.seed(2); S = []
        for e in ["(z-1)**2/(z**3*(z+2i))", "z^2+3.5i*z", "(z**2-1)/(z**2+1)", "exp(z)/z**3", "sqrt(z)-log(z)", "tan(z)/(1+sinh(z))", "2**z", "z**2.5", "e^z+pi"]:
            f = cplx.pyf(e); pts = [[random.uniform(-2, 2), random.uniform(-2, 2)] for _ in range(40)]; S.append({"e": e, "pts": pts, "py": [[f(complex(*p)).real, f(complex(*p)).imag] for p in pts]})
        (t/"s.json").write_text(json.dumps(S)); step("browser: JS evaluator == Python cmath", ["node", str(ROOT/"dev/tools/test_cplx.js"), str(t/"lib.js"), str(t/"s.json")])
else: print("skip browser checks (set PW_MODULE)")
print("\nALL CHECKS PASSED" if not fails else "\nFAILED: " + ", ".join(fails)); sys.exit(1 if fails else 0)
