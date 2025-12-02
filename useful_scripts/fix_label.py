#!/usr/bin/env python3
import os
import sys
from tqdm import tqdm

def fix_labels_in_folder(folder_path):
    """
    Fix all YOLO label txt files in a folder.
    - Each label on its own line
    - Commas replaced by spaces
    - Skip empty lines
    - Warn if any label is corrupt
    """
    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder '{folder_path}' does not exist.")
        return

    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    if not txt_files:
        print(f"[INFO] No .txt files found in '{folder_path}'.")
        return

    print(f"[INFO] Processing {len(txt_files)} files in '{folder_path}'...")

    for filename in tqdm(txt_files, desc="Fixing labels", unit="file"):
        file_path = os.path.join(folder_path, filename)
        fixed_lines = []

        with open(file_path, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                # Split by spaces (multiple labels per line)
                for label in line.split():
                    try:
                        # Replace commas with spaces
                        fixed_line = " ".join(label.split(","))
                        # Validate that all parts can be converted to float (except first, which is class)
                        parts = fixed_line.split()
                        if len(parts) < 5:
                            raise ValueError("Not enough elements for label")
                        class_id = parts[0]
                        coords = [float(x) for x in parts[1:]]  # validate coordinates
                        fixed_lines.append(fixed_line)
                    except Exception as e:
                        print(f"[WARN] Skipping corrupt label in '{filename}' line {line_num}: {label}")

        # Overwrite the file with fixed content
        with open(file_path, "w") as f:
            for fl in fixed_lines:
                f.write(fl + "\n")

    print(f"[INFO] Finished processing folder '{folder_path}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_labels.py [folder]")
        sys.exit(1)

    folder = sys.argv[1]
    fix_labels_in_folder(folder)
