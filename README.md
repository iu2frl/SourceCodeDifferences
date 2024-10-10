# C# Folder Comparison Tool

This Python script compares `.cs` (C# source code) files in two directories, calculating the similarity of files based on their content. It counts the number of non-comment lines in each file and compares files in both directories to find the most similar pairs, printing the results of the comparison.

## Features

- Recursively finds all `.cs` files in the provided directories.
- Compares the files based on content similarity using Python's `difflib` module.
- Ignores files inside `Release` and `Debug` directories.
- Excludes commented lines (lines that start with `//`) when counting lines in a file.
- Compares file similarity based on a threshold (default: 0.8) which can be adjusted by the user.
- Outputs the similarity percentage, total lines, and total similar lines for all the `.cs` files.

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository or download the script.
2. Make sure Python 3.x is installed.
3. Install required libraries (all standard Python libraries):
    - `os`
    - `sys`
    - `difflib`

## Usage

To use the script, run the following command in your terminal or command prompt:

```bash
python compare_folders.py <folder1> <folder2> [similarity_threshold]
```

- `<folder1>`: Path to the first folder containing `.cs` files.
- `<folder2>`: Path to the second folder containing `.cs` files.
- `[similarity_threshold]`: (Optional) A similarity threshold (between `0.0` and `1.0`) for comparing files. Default is `0.8`.

### Example

```bash
python compare_folders.py "G:/Projects/Folder1" "G:/Projects/Folder2" 0.85
```

This will compare all `.cs` files in `Folder1` and `Folder2` using a similarity threshold of `0.85`.

### Output

- The script will print the number of `.cs` files found in both folders.
- For each `.cs` file in `folder1`, it will display whether a similar file was found in `folder2` and print the number of similar lines.
- At the end, the total number of similar lines and the total similarity percentage for all files will be printed.

## Overview of the Code

### `get_cs_files(directory)`

- Recursively searches for all `.cs` files in the provided directory and returns a list of file paths.

### `count_total_lines(file)`

- Reads the file and counts the total number of non-comment lines (ignoring lines starting with `//`).

### `file_similarity(file1, file2)`

- Compares two files using `difflib.SequenceMatcher` and returns a similarity ratio between `0.0` and `1.0`.

### `remove_build_files(files_list)`

- Removes files located in `Release` or `Debug` directories from the list of files.

### `compare_folders(folder1, folder2, similarity_threshold=0.8)`

- Compares `.cs` files between two directories.
- For each file in `folder1`, it finds the most similar file in `folder2` based on the content.
- If the similarity exceeds the given threshold, it calculates and prints the number of similar lines.
- Prints the overall similarity ratio and total similar lines for all files.

### `main()`

- Handles command-line arguments to specify the directories and similarity threshold.
- Validates the directories and threshold value.
- Calls `compare_folders` to perform the comparison.

## Error Handling

- The script checks if the provided directories exist and raises a `FileNotFoundError` if either of them does not exist.
- If an invalid similarity threshold is provided (i.e., not between `0.0` and `1.0`), the script will print an error message and exit.
