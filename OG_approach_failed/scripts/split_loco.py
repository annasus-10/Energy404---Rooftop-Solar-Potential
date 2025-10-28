#!/usr/bin/env python
# split_loco.py
# Deterministic Leave-One-City-Out splits.
# Usage:
#   python split_loco.py --input cleaned_datasets/all_cities_clean.parquet --outdir splits/cross_city_LOCO --write-csv

import argparse, json, hashlib
from pathlib import Path
import pandas as pd

def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def write_pair(df_train, df_test, base_dir: Path, tag: str, write_csv: bool):
    base_dir.mkdir(parents=True, exist_ok=True)

    p_train = base_dir / f"train_{tag}.parquet"
    p_test  = base_dir / f"test_{tag}.parquet"
    df_train.to_parquet(p_train, index=False)
    df_test.to_parquet(p_test, index=False)

    out = {
        "train_parquet_sha1": sha1(p_train),
        "test_parquet_sha1": sha1(p_test),
    }

    if write_csv:
        c_train = base_dir / f"train_{tag}.csv"
        c_test  = base_dir / f"test_{tag}.csv"
        df_train.to_csv(c_train, index=False)
        df_test.to_csv(c_test, index=False)
        out.update({
            "train_csv_sha1": sha1(c_train),
            "test_csv_sha1": sha1(c_test),
        })
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path, help="Combined canonical dataset (parquet or csv)")
    ap.add_argument("--outdir", required=True, type=Path, help="Output root folder")
    ap.add_argument("--write-csv", action="store_true", help="Also write CSV alongside Parquet")
    args = ap.parse_args()

    # Load
    if args.input.suffix.lower() == ".parquet":
        df = pd.read_parquet(args.input)
    else:
        df = pd.read_csv(args.input)

    for col in ["City"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    cities = sorted(df["City"].astype(str).unique())
    root = args.outdir
    root.mkdir(parents=True, exist_ok=True)

    manifest = {
        "source_file": args.input.as_posix(),
        "strategy": "LOCO",
        "cities": [],
    }

    for city in cities:
        test_mask = df["City"].astype(str) == city
        df_test  = df.loc[test_mask].copy()
        df_train = df.loc[~test_mask].copy()

        city_safe = city.replace("/", "-").replace("\\", "-").replace(" ", "_")
        cdir = root / city_safe
        checksums = write_pair(df_train, df_test, cdir, tag=f"LOCO_{city_safe}", write_csv=args.write_csv)

        manifest["cities"].append({
            "city": city,
            "train_rows": int(len(df_train)),
            "test_rows": int(len(df_test)),
            **checksums
        })

    with open(root / "manifest_loco.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("LOCO done.")
    print(f"- Out: {root}")
    print(f"- Manifest: {root / 'manifest_loco.json'}")

if __name__ == "__main__":
    main()
