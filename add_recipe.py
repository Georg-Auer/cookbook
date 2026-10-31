#!/usr/bin/env python3
"""Neues Rezept zum Cookbook hinzufügen (optional mit Bild).

Aufruf:
    python add_recipe.py "Titel des Rezepts" [--image pfad/zum/bild.jpg]
    python add_recipe.py            # interaktiv
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
IMAGES = REPO / "images"

UMLAUTS = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
           "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"}


def slugify(title: str) -> str:
    slug = title
    for umlaut, replacement in UMLAUTS.items():
        slug = slug.replace(umlaut, replacement)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", slug).strip("-").lower()
    return slug or "rezept"


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def copy_image(slug: str, image: Path) -> str:
    IMAGES.mkdir(exist_ok=True)
    target = IMAGES / f"{slug}{image.suffix.lower()}"
    shutil.copy2(image, target)
    return f"images/{target.name}"


def build_recipe(title: str, image_ref: str | None) -> str:
    image_line = f"\n![{title}]({image_ref})\n" if image_ref else ""
    return f"""# {title}
{image_line}
## Zutaten

* Menge Zutat

## Zubereitung

Schritt 1 ...

Mahlzeit!
"""


def update_readme() -> None:
    readme = REPO / "README.md"
    content = readme.read_text(encoding="utf-8")
    start = "<!-- RECIPES:START -->"
    end = "<!-- RECIPES:END -->"
    if start not in content or end not in content:
        return
    entries = []
    for md in sorted(REPO.glob("*.md")):
        if md.name in ("README.md", "TEMPLATE.md"):
            continue
        title = first_heading(md)
        image = next(IMAGES.glob(f"{md.stem}.*"), None)
        if image is not None:
            entries.append(f"- [{title}]({md.name}) · ![{title}](images/{image.name})")
        else:
            entries.append(f"- [{title}]({md.name})")
    listing = "\n".join(entries) if entries else "_Noch keine Rezepte._"
    updated = re.sub(
        rf"({re.escape(start)})\n.*?\n({re.escape(end)})",
        lambda m: f"{m.group(1)}\n{listing}\n{m.group(2)}",
        content,
        flags=re.DOTALL,
    )
    readme.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Neues Rezept hinzufügen")
    parser.add_argument("title", nargs="?", help="Titel des Rezepts")
    parser.add_argument("--image", type=Path, help="Pfad zu einem Bild des Gerichts")
    args = parser.parse_args()

    title = args.title or input("Titel des Rezepts: ").strip()
    if not title:
        sys.exit("Kein Titel angegeben – abgebrochen.")

    image = args.image
    if image is None and input("Bild hinzufügen? [j/N]: ").strip().lower() == "j":
        image = Path(input("Pfad zum Bild: ").strip().strip('"'))

    slug = slugify(title)
    recipe_path = REPO / f"{slug}.md"
    if recipe_path.exists():
        sys.exit(f"{recipe_path.name} existiert bereits – abgebrochen.")

    image_ref = None
    if image is not None:
        if not image.is_file():
            sys.exit(f"Bild nicht gefunden: {image}")
        image_ref = copy_image(slug, image)

    recipe_path.write_text(build_recipe(title, image_ref), encoding="utf-8")
    update_readme()
    print(f"Rezept angelegt: {recipe_path.name}")
    if image_ref:
        print(f"Bild kopiert nach: {image_ref}")


if __name__ == "__main__":
    main()
