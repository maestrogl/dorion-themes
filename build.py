#!/usr/bin/env python3
"""Build every theme in themes/ from src/template.css and src/palettes.json.

Usage: python3 build.py
"""
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).parent
TEMPLATE = Template((ROOT / "src" / "template.css").read_text())
PALETTES = json.loads((ROOT / "src" / "palettes.json").read_text())
OUT = ROOT / "themes"

# Translucent variants the template needs, as (colour key, alpha) pairs.
ALPHAS = {
    "raised": [45],
    "yellow": [8, 12],
    "accent": [10, 15, 30],
    "highlight": [20, 30, 40, 55, 60, 70],
    "border": [15, 25, 30, 40],
}


def rgba(hex_colour, alpha):
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def slug(name):
    return (
        name.lower()
        .replace("é", "e")
        .replace(" ", "-")
    )


def build(colours):
    values = dict(colours)
    values.setdefault("badge_text", values["darkest"])
    for key, alphas in ALPHAS.items():
        for a in alphas:
            values[f"{key}_{a:02d}"] = rgba(values[key], a / 100)
    return TEMPLATE.substitute(values)


def main():
    OUT.mkdir(exist_ok=True)
    for name, colours in PALETTES.items():
        path = OUT / f"{slug(name)}.theme.css"
        path.write_text(build(colours))
        print(f"built {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
