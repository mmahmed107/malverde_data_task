import pandas as pd
import re

def clean_name_part(part):
    if pd.isna(part):
        return ""
    part = str(part)
    part = re.sub(r"\(\d+\)", "", part)           # Remove numbered (1), (2)
    part = re.sub(r"\([^)]+\)", "", part)          # Remove bracketed tags like (GENERAL)
    part = part.strip().strip("\"'")              # Strip quotes and whitespace
    part = re.sub(r"\s+", " ", part)                # Normalize spacing
    return part

def build_full_name(row):
    parts = [
        row.get('Name 1'), row.get('Name 2'),
        row.get('Name 3'), row.get('Name 4'), row.get('Name 6')
    ]
    cleaned_parts = [clean_name_part(p) for p in parts if clean_name_part(p)]
    return " ".join(cleaned_parts)

def parse_dob(dob_str):
    try:
        return pd.to_datetime(dob_str, dayfirst=True, errors='coerce').date()
    except Exception:
        return None

def clean_nationality(nat):
    if pd.isna(nat):
        return ""
    return re.sub(r"\(\d+\)\s*", "", str(nat)).replace("..", ".").strip()

def main():
    input_file = "ConList.xlsx"
    output_file = "ConList_cleaned.csv"

    df = pd.read_excel(input_file, header=1)

    # Construct and clean Full Name
    df['Full Name'] = df.apply(build_full_name, axis=1)
    df['Full Name'] = df['Full Name'].str.replace(r'\(\d+\)', '', regex=True).str.strip()

    # Clean other fields
    if 'Nationality' in df.columns:
        df['Nationality'] = df['Nationality'].apply(clean_nationality)
    if 'DOB' in df.columns:
        df['DOB'] = df['DOB'].apply(parse_dob)

    final_columns = ['Full Name', 'DOB', 'Nationality', 'Country', 'Group Type', 'Alias Type',
                     'Alias Quality', 'Regime', 'UK Sanctions List Date Designated',
                     'Last Updated', 'Other Information']

    df_final = df[[col for col in final_columns if col in df.columns]].drop_duplicates()
    df_final = df_final.sort_values(by="Full Name", na_position="last")

    df_final.to_csv(output_file, index=False)
    print("Sanctions list cleaned and saved as:", output_file)

# ------------------
# Unit Tests
# ------------------
def test_build_full_name():
    row = {'Name 1': 'Jim', 'Name 2': 'Jones', 'Name 3': None, 'Name 4': '', 'Name 6': 'Smith'}
    assert build_full_name(row) == "Jim Jones Smith"
    row = {'Name 1': None, 'Name 2': None, 'Name 3': None, 'Name 4': None, 'Name 6': 'ZAPCHAST LLP'}
    assert build_full_name(row) == "ZAPCHAST LLP"
    row = {'Name 1': '(1) John', 'Name 2': '', 'Name 3': '', 'Name 4': '', 'Name 6': '(2) Doe'}
    assert build_full_name(row) == "John Doe"

def test_parse_dob():
    assert parse_dob("22/08/1990") == pd.to_datetime("1990-08-22").date()
    assert pd.isna(parse_dob("not a date"))

def test_clean_nationality():
    assert clean_nationality("(1) Germany. (2) Morocco") == "Germany. Morocco"
    assert clean_nationality("(1) Russia. (2) Ukraine") == "Russia. Ukraine"

if __name__ == "__main__":
    test_build_full_name()
    test_parse_dob()
    test_clean_nationality()
    print("All tests passed.")
    main()
