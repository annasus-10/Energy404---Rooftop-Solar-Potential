#!/usr/bin/env python
# split_combined_stratified.py
# One global train/test split, stratified by (City × Assumed_building_type), robust to rare strata.
# Usage:
#   python split_combined_stratified.py --input cleaned_datasets/all_cities_clean.parquet --outdir splits/combined_stratified_city_type --test-size 0.2 --seed 404 --write-csv

import argparse, json, math, hashlib
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path, help="Combined canonical dataset (parquet or csv)")
    ap.add_argument("--outdir", required=True, type=Path, help="Output folder")
    ap.add_argument("--test-size", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=404)
    ap.add_argument("--write-csv", action="store_true")
    args = ap.parse_args()

    # Load
    if args.input.suffix.lower() == ".parquet":
        df = pd.read_parquet(args.input)
    else:
        df = pd.read_csv(args.input)

    for col in ["City", "Assumed_building_type"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df = df.copy()
    df["_city_type"] = df["City"].astype(str) + " | " + df["Assumed_building_type"].astype(str)

    # Rare strata guard
    p = args.test_size
    min_count = max(math.ceil(1/p), math.ceil(1/(1-p)))  # need ≥1 sample for both sets
    counts = df["_city_type"].value_counts()
    rare_keys = set(counts[counts < min_count].index)

    if rare_keys:
        def collapse_rare(s):
            city, typ = s.split(" | ", 1)
            return f"{city} | RARE" if s in rare_keys else s
        df["_strat"] = df["_city_type"].apply(collapse_rare)
        # Verify collapsed buckets now large enough
        ok = (df["_strat"].value_counts() >= min_count).all()
        stratify = df["_strat"] if ok else None
        used_key = "_strat" if ok else None
    else:
        stratify = df["_city_type"]
        used_key = "_city_type"

    # Split (deterministic)
    train_df, test_df = train_test_split(
        df,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=stratify
    )

    # Write
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    drop_cols = [c for c in ["_city_type", "_strat"] if c in df.columns]
    train_out = train_df.drop(columns=drop_cols, errors="ignore")
    test_out  = test_df.drop(columns=drop_cols, errors="ignore")

    p_train = outdir / "train_combined.parquet"
    p_test  = outdir / "test_combined.parquet"
    train_out.to_parquet(p_train, index=False)
    test_out.to_parquet(p_test, index=False)

    checksums = {
        "train_parquet_sha1": sha1(p_train),
        "test_parquet_sha1": sha1(p_test),
    }

    if args.write_csv:
        c_train = outdir / "train_combined.csv"
        c_test  = outdir / "test_combined.csv"
        train_out.to_csv(c_train, index=False)
        test_out.to_csv(c_test, index=False)
        checksums.update({
            "train_csv_sha1": sha1(c_train),
            "test_csv_sha1": sha1(c_test),
        })

    # Manifest + tiny distribution check
    manifest = {
        "source_file": args.input.as_posix(),
        "strategy": "combined_stratified_city_type",
        "test_size": args.test_size,
        "seed": args.seed,
        "rows_total": int(len(df)),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "stratify_key": used_key or "FALLBACK_RANDOM",
        **checksums
    }

    # Optional: distribution similarity metric (median abs diff of key shares)
    try:
        import numpy as np
        if used_key:
            tr_share = train_df[used_key].value_counts(normalize=True).sort_index()
            te_share = test_df[used_key].value_counts(normalize=True).sort_index()
            common = tr_share.index.intersection(te_share.index)
            manifest["median_abs_diff_share"] = float(np.median((tr_share.loc[common] - te_share.loc[common]).abs()))
    except Exception:
        pass

    with open(outdir / "manifest_combined.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("Combined stratified split done.")
    print(f"- Out: {outdir}")
    print(f"- Manifest: {outdir / 'manifest_combined.json'}")
    print(f"- Stratify key used: {manifest['stratify_key']}")

if __name__ == "__main__":
    main()
