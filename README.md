# vizualize

A Claude skill for fast, rigorous in-chat visualisations of advanced mathematics and STEM. Correctness first, speed second, decoration last.

## Covers

- **Abstract algebra** – groups, Cayley graphs, subgroup lattices, quotients, field extensions, Galois
- **Complex analysis** – complex plane, conformal maps, domain colouring, contours, residues
- **Geometry and geometric algebra**
- **Functional analysis** – norms and unit balls, projections, Hahn-Banach, Riesz, operators
- **Graphs and graph algorithms**
- **Commutative and proof-structure diagrams**
- **STEM** – ODE phase portraits, distributions and CLT, electric fields, projectile motion, RLC/RC circuits, thin lenses

Output is inline SVG / Mermaid (interactive sliders only when varying a parameter teaches). Generators are deterministic Python with no dependencies.

## Install

Copy the `vizualize/` folder (it holds `SKILL.md`) into your skills directory:

```sh
cp -r vizualize ~/.claude/skills/        # Claude Code, personal
cp -r vizualize .claude/skills/          # Claude Code, per project
```

For claude.ai: zip the `vizualize/` folder and upload it under Settings > Capabilities > Skills.

## Layout

```
vizualize/   the skill (SKILL.md, scripts/, references/)  <- this is what ships
dev/         tests, golden regression, trigger evals, roadmap (not shipped)
```

## Develop

```sh
python3 dev/check.py
```

Runs certificate tests, golden regression, determinism and size-budget checks. Browser checks need Playwright; see [dev/README.md](dev/README.md).

## License

[MIT](LICENSE)
