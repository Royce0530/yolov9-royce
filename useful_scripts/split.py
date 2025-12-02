#!/usr/bin/env python3
import os
import sys
import argparse
from tqdm import tqdm

def split_labels(input_file, output_dir):
    """
    Split a large YOLO-like label txt file into individual YOLOv9-compatible txt files.
    Each label on its own line, commas replaced by spaces.
    """
    if not os.path.exists(input_file):
        print(f"[ERROR] Input file '{input_file}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        lines = f.readlines()

    print(f"[INFO] Splitting {len(lines)} lines from '{input_file}' into '{output_dir}'...")

    for line_num, line in enumerate(tqdm(lines, desc="Splitting labels", unit="line")):
        line = line.strip()
        if not line:
            continue

        parts = line.split(maxsplit=1)
        filename = parts[0]
        labels = parts[1] if len(parts) > 1 else ""

        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(output_dir, txt_filename)

        fixed_lines = []
        for label in labels.split():
            try:
                fixed_line = " ".join(label.split(","))
                # Validate format: first element is class, rest are floats
                parts_val = fixed_line.split()
                if len(parts_val) < 5:
                    raise ValueError("Not enough elements in label")
                class_id = parts_val[0]
                coords = [float(x) for x in parts_val[1:]]  # validate floats
                fixed_lines.append(fixed_line)
            except Exception as e:
                print(f"[WARN] Skipping corrupt label in '{filename}' line {line_num+1}: {label}")

        if fixed_lines:
            with open(txt_path, "w") as out_f:
                for fl in fixed_lines:
                    out_f.write(fl + "\n")
        else:
            # Create empty file if no labels
            open(txt_path, "w").close()

    print(f"[INFO] Finished splitting labels into '{output_dir}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split YOLO label txt file into individual files")
    parser.add_argument("--input", required=True, help="Input label txt file (e.g., train2017.txt)")
    parser.add_argument("--output", required=True, help="Destination folder for split label files")
    args = parser.parse_args()

    split_labels(args.input, args.output)
