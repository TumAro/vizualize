# vizualize – development notes (not shipped in the zip)

- `python3 dev/check.py` – full quality gate (certificate tests, golden regression of 139 commands in plain + widget mode, determinism, size budget; with a browser also the simulated claude.ai host in light/dark, slider sweeps, JS-vs-Python evaluator parity).
- `python3 dev/tools/golden.py --update` – accept intended output changes (it first proves the output is deterministic). Add a command = add a line to `dev/golden_cmds.txt` (prefix `!` and `:: text` for a command that must refuse).
- Browser checks need Playwright: `npm i playwright && npx playwright install chromium`, then `PW_MODULE=<node_modules/playwright> PLAYWRIGHT_BROWSERS_PATH=<dir> python3 dev/check.py`.
- `dev/trigger_eval.json` – 20 realistic trigger queries (10 should / 10 should not trigger); `dev/trigger_results/` holds the description-optimisation runs.
- `dev/mv.js` – `mv.py slider bundle`, for the optional jsDelivr route (`--cdn <url>`), not published.
- `dev/ROADMAP.md` – phases and decisions.
