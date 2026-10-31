# recipes

Persönliche Rezeptsammlung.

## Neues Rezept hinzufügen

Am einfachsten mit dem Skript (legt die Markdown-Datei an, kopiert ein Bild nach `images/` und trägt das Rezept automatisch in diese Übersicht ein):

```bash
python add_recipe.py "Titel des Rezepts" --image pfad/zum/bild.jpg
# oder interaktiv:
python add_recipe.py
```

Manuell geht es auch: Datei `<name>.md` anlegen (siehe `TEMPLATE.md`) und ein Bild nach `images/<name>.jpg` legen – beim nächsten Lauf von `add_recipe.py` erscheint das Rezept samt Bild in der Liste unten.

## Rezepte

<!-- RECIPES:START -->
- [Focaccia](focaccia.md)
- [Pizza nach neapolitanischer Art](pizza.md)
<!-- RECIPES:END -->
