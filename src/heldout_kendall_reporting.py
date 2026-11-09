"""Report sections generated from the shared saved-prediction score table."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def report_suffix(path):
    sections=json.loads((ROOT/'results/heldout_kendall/report_sections.json').read_text())
    section=sections.get(str(path))
    return '' if section is None else '\n'+section
