"""Obtain the original research inputs and verify their pinned SHA256 hashes."""
import argparse
import json

from src.data import RAW, ROOT, SOURCES, audit, download, load_all, verify_data_file


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="Check local inputs without network access")
    args = parser.parse_args()
    for filename in SOURCES:
        path = RAW / filename if args.verify_only else download(filename)
        if not path.exists():
            parser.error(f"Missing {filename}; run python download_data.py first")
        digest = verify_data_file(filename, path)
        print(f"Verified {filename}: {digest}")
    output = ROOT / "results" / "data_audit.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps([audit(d) for d in load_all()], indent=2) + "\n")
    print("Saved results/data_audit.json. Sushi source data must not be redistributed.")


if __name__ == "__main__":
    main()
