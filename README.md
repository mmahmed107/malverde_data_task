# Malverde Data Task - Sanctions List Cleaning

## Output File
**`ConList_cleaned.csv`**
- Cleaned and transformed version of the OFSI Consolidated List
- Sorted alphabetically by `Full Name`
- Saved in `.csv` format for ease of analysis and compatibility

## Files Submitted
- `ConList_cleaned.csv`: Final cleaned output
- `data_transformation_complete.py`: Python script containing all transformation logic and unit tests
- `README.md`: This documentation file

## How to Run the Script
**Requirements:**
- Python 3.10+
- Required libraries:
  ```bash
  pip install pandas openpyxl
  ```

**Execution:**
Ensure `ConList.xlsx` (input file) is in the same directory as the script. Then run:
```bash
python data_transformation_complete.py
```
This will generate `ConList_cleaned.csv` in the same folder.

## Data Quality Issues Identified
The following data quality issues were observed and handled:

- **Name inconsistencies:**
  - Entries included formatting artifacts such as `(1)`, `(2)`, `(GENERAL)`, and stray quotes (`'`, `"`)
  - A general-purpose name cleaning function was implemented using regular expressions to remove these patterns throughout

- **Incomplete or missing data:**
  - Fields like `DOB`, `Nationality`, `Alias Quality`, and `Country` often had missing values — especially for organizational entities and aliases
  - These were retained as-is to avoid discarding relevant but partial entries

- **Duplicate-like records:**
  - Some individuals/entities appear multiple times with slightly varied names or DOBs, but identical metadata (e.g., same Regime, Country, etc.)
  - These represent aliases or transliterations as listed by OFSI and were intentionally preserved

- **Formatting inconsistencies:**
  - Extra whitespace, punctuation, and non-uniform structures were cleaned using regex
  - Nationality field was cleaned to remove prefixed labels like `(1)` and `(2)` for dual citizens

## Testing
Basic unit tests were included for all core transformation functions:
- `build_full_name()`
- `parse_dob()`
- `clean_nationality()`

These ensure proper functionality for edge cases such as missing names, malformed dates, and inconsistent formatting.

