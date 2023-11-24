# python accuracy.py out/solution.out out/own_solution.out

import sys

def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    # Ensure that we have the same number of lines in both files
    if len(file1_lines) != len(file2_lines):
        print("Files have different number of lines, cannot compare line by line.")
        return

    # Count the number of similar lines.
    similar_count = 0
    total_lines = len(file1_lines)

    for line1, line2 in zip(file1_lines, file2_lines):
        if line1.strip() == line2.strip():  # Remove leading/trailing whitespaces before comparing
            similar_count += 1

    # Calculate the percentage of similar lines
    percentage_similar = (similar_count / total_lines) * 100

    print(f"Percentage of similar lines: {percentage_similar:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_files.py <file1_path> <file2_path>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]

    compare_files(file1_path, file2_path)