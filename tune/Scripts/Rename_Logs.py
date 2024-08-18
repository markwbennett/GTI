'''Script that iterates through Simostools files in the directory (passed argument or default) and renames them with {name of tune}_{min_gear}-{max_gear}_{min_rev}-{max_rev}_{date}_{time}.csv'''

import os
import sys
import re
from pandas import read_csv

DEFAULT_DIRECTORY = "/Volumes/4TB/Users/MB/Library/CloudStorage/GoogleDrive-mb@ivi3.com/My Drive/GTI_local/Simos/Logs"

def is_has_hrpm(filename):
    """Check if the filename already contains 'HRPM'."""
    base_name = os.path.splitext(filename)[0]  # Get the base name without extension
    return "HRPM" in base_name


def extract_tune_name(tune_field):
    """Extract the tune name from the 'SimosTools' field."""
    print(f"Debug: tune_field type: {type(tune_field)}, content: {tune_field}")  # Debug line
    if isinstance(tune_field, bytes):
        tune_field = tune_field.decode('utf-8')
    match = re.search(r':([^:]+)\.bin]', tune_field)
    return match.group(1) if match else ''


def rename_csv_with_rpm(csv_filename):
    """Rename CSV files based on RPM, Gear values, and Tune name."""
    # Return if the filename does not begin with 'simos' or a digit
    filename = os.path.basename(csv_filename)
    print(filename)
    if not (filename.startswith('simos') or filename[0].isdigit()):
        return

    try:
        df = read_csv(csv_filename)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error reading {csv_filename}: {e}")
        return

    print(f"Debug: DataFrame columns: {df.columns}")  # Debug line
    print(f"Debug: DataFrame first row: {df.iloc[0]}")  # Debug line

    rpm_column = [col for col in df.columns if 'RPM' in col or 'rpm' in col]
    gear_column = [col for col in df.columns if 'Gear' in col or 'gear' in col]
    tune_column = [col for col in df.columns if 'SimosTools' in col]

    if not rpm_column:
        print(f"No column containing 'RPM' found in {csv_filename}")
        return

    rpm_values = df[rpm_column[0]]
    gear_values = df[df[gear_column[0]] != 0][gear_column[0]] if gear_column else ''

    tune_name = ''
    if tune_column:
        tune_name = extract_tune_name(tune_column[0])

    min_rpm = f"{int(rpm_values.min() / 100):02}"
    max_rpm = f"{int(rpm_values.max() / 100):02}"
    rpm_part = f"{min_rpm}-{max_rpm}"

    gear_part = ''
    if not gear_values.empty:
        min_gear = gear_values.min()
        max_gear = gear_values.max()
        gear_part = f"{int(min_gear)}-{int(max_gear)}" if min_gear != max_gear else str(int(max_gear))

    filename, extension = os.path.splitext(csv_filename)
    directory, filename = os.path.split(filename)

    patterns = [
        r'(\d{4}[-_]\d{2}[-_]\d{2})[-_](\d{2}[-_]\d{2}[-_]\d{2})',
        r'(\d{8})[-_](\d{6})',
        r'(\d{8})(\d{6})'
    ]
    result = None
    for pattern in patterns:
        result = re.search(pattern, filename)
        if result:
            break

    date, time = '', ''
    if result:
        date = result.group(1).replace("_", "").replace("-", "")
        time = result.group(2).replace("_", "").replace("-", "")

    new_filename = f'{tune_name}_{gear_part}_{rpm_part}HRPM_{date}_{time}{extension}'

    new_path = os.path.join(directory, new_filename)
    if not os.path.exists(new_path):
        try:
            os.rename(csv_filename, new_path)
            print(f"File renamed to: {new_filename}")
        except Exception as e:
            print(f"Error renaming file {csv_filename} to {new_filename}: {e}")


def handle_file(path):
    """Handle the renaming of a single file."""
    rename_csv_with_rpm(path)


# Process files passed as arguments or iterate through CSV files in the specified directory
if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        file_path = ' '.join(args)
        handle_file(file_path)
    else:
        directory = DEFAULT_DIRECTORY
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                handle_file(file_path)
