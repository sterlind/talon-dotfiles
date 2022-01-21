import csv
from pathlib import Path
from talon import Module, Context, resource

SETTINGS_DIR = Path(__file__).parents[1] / "lists"

def get_list_from_csv(filename: str):
    """Retrieves list from CSV"""
    path = SETTINGS_DIR / filename
    assert filename.endswith(".csv")

    # Now read via resource to take advantage of talon's
    # ability to reload this script for us when the resource changes
    with resource.open(str(path), "r") as f:
        rows = list(csv.reader(f))

    # print(str(rows))
    mapping = {}
    if len(rows) >= 2:
        for row in rows[1:]:
            if len(row) == 0:
                # Windows newlines are sometimes read as empty rows. :champagne:
                continue
            if len(row) == 1:
                output = spoken_form = row[0]
            else:
                output, spoken_form = row[:2]
                if len(row) > 2:
                    print(
                        f'"{filename}": More than two values in row: {row}.'
                        + " Ignoring the extras."
                    )
            # Leading/trailing whitespace in spoken form can prevent recognition.
            spoken_form = spoken_form.strip()
            mapping[spoken_form] = output

    return mapping

mod = Module()
ctx = Context()

mod.list("abbreviations", "List of abbreviations")
ctx.lists["self.abbreviations"] = get_list_from_csv("abbreviations.csv")

mod.list("vocabulary", "List of vocabulary")
ctx.lists["self.vocabulary"] = get_list_from_csv("vocabulary.csv")

mod.list("extensions", "List of extensions")
ctx.lists["self.extensions"] = get_list_from_csv("extensions.csv")