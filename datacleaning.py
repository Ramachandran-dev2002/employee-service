"""Clean a CSV file and document every cleaning decision.

Usage: python datacleaning.py input.csv
Outputs clean_data.csv, cleaning_summary.csv, and cleaning_decisions.csv
in the current directory (or beside the input file with --output-dir).
"""

import argparse
import re
from pathlib import Path

import pandas as pd


def _is_date_column(name, values):
	"""Recognize likely dates without treating ordinary numbers as dates."""
	if re.search(r"date|time|timestamp|dob", str(name), re.IGNORECASE):
		return True
	sample = values.dropna().astype(str).head(100)
	if sample.empty or not sample.str.contains(r"[-/:]|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", case=False).any():
		return False
	parsed = pd.to_datetime(sample, errors="coerce")
	return parsed.notna().mean() >= 0.8


def clean_data(frame):
	"""Return a cleaned copy and a per-column record of decisions."""
	data = frame.copy()
	decisions = []

	for column in list(data.columns):
		original_missing = int(data[column].isna().sum())
		series = data[column]
		non_null = series.dropna()

		if non_null.empty:
			data.drop(columns=[column], inplace=True)
			decisions.append({
				"column": column,
				"action": "dropped column",
				"reason": "The column contained no non-missing values, so it had no usable information.",
				"missing_filled": 0,
				"outliers_detected": 0,
				"outlier_action": "not applicable",
			})
			continue

		if _is_date_column(column, series):
			data[column] = pd.to_datetime(series, errors="coerce")
			# Unparseable date strings become missing; keep and flag them rather than
			# silently inventing dates.
			missing = int(data[column].isna().sum())
			action = "parsed as datetime; missing values left and flagged"
			reason = "Column name or values indicate dates; invalid/missing dates are retained as NaT for review."
			filled = 0
		else:
			# Convert numeric values stored as text when most populated values parse.
			as_text = series.astype("string").str.strip()
			numeric = pd.to_numeric(as_text.str.replace(",", "", regex=False), errors="coerce")
			numeric_rate = numeric.notna().sum() / max(series.notna().sum(), 1)
			if pd.api.types.is_numeric_dtype(series) or numeric_rate >= 0.8:
				data[column] = numeric
				outliers = 0
				values = data[column].dropna()
				if len(values) >= 4:
					q1, q3 = values.quantile([0.25, 0.75])
					iqr = q3 - q1
					outliers = int(((values < q1 - 1.5 * iqr) | (values > q3 + 1.5 * iqr)).sum())
				missing = int(data[column].isna().sum())
				if missing:
					median = data[column].median()
					data[column] = data[column].fillna(median)
					action = "converted to numeric; filled missing values with median"
					reason = "Numeric data uses the median, which is robust to skew and extreme values."
					filled = missing
				else:
					action = "converted to numeric where needed"
					reason = "Values are numeric; no missing values required imputation."
					filled = 0
				outlier_action = "detected with 1.5×IQR; retained and flagged (no values removed)"
				decisions.append({
					"column": column, "action": action, "reason": reason,
					"missing_filled": filled, "outliers_detected": outliers,
					"outlier_action": outlier_action,
				})
				continue

			# Standardize text categories before selecting the most frequent value.
			if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series) or isinstance(series.dtype, pd.CategoricalDtype):
				standardized = series.astype("string").str.strip().str.lower()
				standardized = standardized.replace("", pd.NA)
				data[column] = standardized
				mode = standardized.mode(dropna=True)
				missing = int(standardized.isna().sum())
				if missing and not mode.empty:
					data[column] = standardized.fillna(mode.iloc[0])
					action = "trimmed/lowercased text; filled missing values with mode"
					reason = "Categorical text is standardized to trimmed lowercase; the mode preserves the most common category."
					filled = missing
				else:
					action = "trimmed/lowercased text"
					reason = "Categorical text is standardized; missing values were absent or no mode was available."
					filled = 0
			else:
				missing = int(series.isna().sum())
				mode = series.mode(dropna=True)
				if missing and not mode.empty:
					data[column] = series.fillna(mode.iloc[0])
					action = "filled missing values with mode"
					reason = "Non-numeric values are filled with their most frequent observed value."
					filled = missing
				else:
					action = "left missing values and flagged"
					reason = "No safe mode was available for imputation."
					filled = 0

		decisions.append({
			"column": column, "action": action, "reason": reason,
			"missing_filled": filled, "outliers_detected": 0,
			"outlier_action": "not evaluated for non-numeric data",
		})

	return data, pd.DataFrame(decisions)


def main():
	parser = argparse.ArgumentParser(description="Clean a CSV and save an audit summary.")
	parser.add_argument("input", help="Path to the source CSV file")
	parser.add_argument("--output-dir", default=".", help="Directory for output files (default: current directory)")
	args = parser.parse_args()

	source = pd.read_csv(args.input)
	before = {
		"rows": len(source),
		"missing_values": int(source.isna().sum().sum()),
		"duplicates": int(source.duplicated().sum()),
	}
	cleaned, decisions = clean_data(source)
	cleaned = cleaned.drop_duplicates().reset_index(drop=True)
	after = {
		"rows": len(cleaned),
		"missing_values": int(cleaned.isna().sum().sum()),
		"duplicates": int(cleaned.duplicated().sum()),
	}

	output_dir = Path(args.output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)
	cleaned.to_csv(output_dir / "clean_data.csv", index=False)
	pd.DataFrame([
		{"stage": "before", **before},
		{"stage": "after", **after},
	]).to_csv(output_dir / "cleaning_summary.csv", index=False)
	decisions.to_csv(output_dir / "cleaning_decisions.csv", index=False)
	print(f"Rows {before['rows']} -> {after['rows']} | Missing values {before['missing_values']} -> {after['missing_values']} | Duplicates {before['duplicates']} -> {after['duplicates']}")


if __name__ == "__main__":
	main()
