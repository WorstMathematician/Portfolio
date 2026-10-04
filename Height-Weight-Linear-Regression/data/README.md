# Original data input

The original 10,000-row CSV is not stored in this repository.

To rerun the empirical analysis:

1. Place the original file here as `weight-height.csv`, or update `CSV_PATH` in the notebook.
2. Set `DATA_MODE = "original"`.
3. Run all notebook cells.

## Accepted columns

The notebook accepts common height/weight column names, including:

- `Height` and `Weight`
- `Height_Inches` and `Weight_Pounds`

Column matching is case-insensitive and ignores spaces, hyphens, underscores, and parentheses.

Any extra columns, such as a gender/sex category in the source file, are left unused by this simple bivariate regression.

## Expected units

- Height: inches
- Weight: pounds

The loader converts the selected columns to numeric values, drops rows with missing/non-numeric height or weight, and requires at least three valid observations.
