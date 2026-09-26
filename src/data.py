"""Download original data on demand; never redistribute downloaded Sushi data."""
from dataclasses import dataclass
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import warnings
import zipfile

import numpy as np
import pandas as pd
import rdata

from .models import pair_counts, validate_rankings

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SOURCES = {s["file"]: s for s in json.loads((ROOT / "data" / "sources.json").read_text())}
URLS = {name: source["url"] for name, source in SOURCES.items()}


def verify_data_file(filename, path):
    """Reject changed/corrupt inputs instead of silently changing the experiment."""
    source = SOURCES[filename]
    payload = Path(path).read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != source["sha256"] or len(payload) != source["bytes"]:
        raise ValueError(f"Checksum/size mismatch for {filename}; expected the version in data/sources.json")
    return digest


def download(filename):
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / filename
    if not path.exists():
        request = urllib.request.Request(URLS[filename], headers={"User-Agent": "RankingResearch/1.0"})
        temporary = path.with_suffix(path.suffix + ".part")
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = response.read()
        try:
            temporary.write_bytes(payload)
            verify_data_file(filename, temporary)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    verify_data_file(filename, path)
    return path


@dataclass
class Dataset:
    name: str
    y: np.ndarray
    labels: list
    groups: np.ndarray | None = None
    exclusions: int = 0

    @property
    def n(self):
        return len(self.labels)


def load_beans():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message='Missing constructor for R class "Date"')
        frame = rdata.read_rda(download("beans.rda"))["beans"]
    cols = ["variety_a", "variety_b", "variety_c"]
    labels = sorted(set(frame[cols].to_numpy().ravel()))
    lookup = dict(zip(labels, range(len(labels))))
    y, seasons, excluded = [], [], 0
    for _, row in frame.iterrows():
        items = row[cols].tolist()
        best, worst = row["best"], row["worst"]
        if (any(pd.isna(x) for x in items+[best, worst]) or len(set(items)) != 3
                or best not in ("A", "B", "C") or worst not in ("A", "B", "C") or best == worst):
            raise ValueError('Whole Beans task is ineligible: invalid original report; no rows removed')
        middle = next(x for x in "ABC" if x not in (best, worst))
        y.append([lookup[items["ABC".index(x)]] for x in [best, middle, worst]])
        seasons.append(str(row["season"]))
    y = validate_rankings(y, len(labels))
    return Dataset("beans", y, labels, np.asarray(seasons), excluded)


def load_sushi(kind):
    if kind not in ("a", "b"):
        raise ValueError(kind)
    path = download("sushi3-2016.zip")
    with zipfile.ZipFile(path) as z:
        member = f"sushi3-2016/sushi3{kind}.5000.10.order"
        lines = z.read(member).decode("ascii").splitlines()
        n = int(lines[0].split()[0])
        a = np.loadtxt(io.StringIO("\n".join(lines[1:])), dtype=int)
    if np.any(a[:, 1] != 10) or np.any(a[:, 0] != 0):
        raise ValueError("Unexpected Sushi order format")
    y = validate_rankings(a[:, 2:], n)
    return Dataset(f"sushi_{kind}", y, [f"{kind}_{i}" for i in range(n)])


def audit(data):
    y, n = data.y, data.n
    item = np.bincount(y.ravel(), minlength=n)
    w = pair_counts(y, n)
    exposure = (w+w.T)[np.triu_indices(n, 1)]
    return {"dataset": data.name, "reports": len(y), "items": n, "r": y.shape[1],
            "excluded_reports": data.exclusions, "item_exposure_min": int(item.min()),
            "item_exposure_max": int(item.max()), "pairs_observed": int((exposure > 0).sum()),
            "pairs_possible": n*(n-1)//2, "pair_exposure_min": int(exposure.min()),
            "pair_exposure_max": int(exposure.max()),
            "season_counts": pd.Series(data.groups).value_counts().to_dict() if data.groups is not None else None}


def load_all():
    return [load_beans(), load_sushi("a"), load_sushi("b")]


def save_manifest(out):
    entries = []
    for filename, url in URLS.items():
        path = download(filename)
        entries.append({"file": filename, "url": url,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "bytes": path.stat().st_size})
    (Path(out)/"data_manifest.json").write_text(json.dumps(entries, indent=2)+"\n")
