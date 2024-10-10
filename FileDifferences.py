import os
import difflib
import sys

def get_cs_files(directory):
    """
    Recursively get all .cs files in the directory.
    
    Args:
        directory (str): The directory to search for .cs files.
        
    Returns:
        list: A list of paths to all .cs files in the directory.
    """
    cs_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                cs_files.append(os.path.join(root, file))
    return cs_files

def count_total_lines(file):
    """
    Count the total number of lines in a file, excluding lines that start with "//".
    
    Args:
        file (str): Path to the file.
        
    Returns:
        int: The number of non-comment lines in the file.
    """
    try:
        with open(file, 'r') as f:
            file_content = f.readlines()
    except:
        try:
            with open(file, 'r', encoding="utf-8") as f:
                file_content = f.readlines()
        except:
            return 0
        
    return len([line for line in file_content if not line.startswith("//")])

def file_similarity(file1, file2):
    """
    Compare two files and return the similarity ratio based on content.
    
    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.
        
    Returns:
        float: Similarity ratio between the two files (0.0 to 1.0).
    """
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
    except:
        try:
            with open(file1, 'r', encoding="utf-8") as f1, open(file2, 'r', encoding="utf-8") as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()
        except:
            return 0.0
    
    # Calculate similarity ratio using difflib
    similarity_ratio = difflib.SequenceMatcher(None, lines1, lines2).ratio()
    return similarity_ratio

def remove_build_files(files_list):
    """
    Remove files from 'Release' and 'Debug' folders.
    
    Args:
        files_list (list): List of file paths to filter.
        
    Returns:
        list: Filtered list of file paths, excluding those in build folders.
    """
    files_list = [file for file in files_list if '\\Release\\' not in file]
    files_list = [file for file in files_list if '\\Debug\\' not in file]
    return files_list

def compare_folders(folder1, folder2, similarity_threshold=0.8):
    """
    Compare all .cs files in two folders based on their content and count similar lines.
    
    Args:
        folder1 (str): Path to the first folder.
        folder2 (str): Path to the second folder.
        similarity_threshold (float): Threshold for file similarity (default 0.8).
        
    Returns:
        None: Prints the comparison results.
    """
    cs_files1 = remove_build_files(get_cs_files(folder1))
    cs_files2 = remove_build_files(get_cs_files(folder2))
    
    cs_files1_len = len(cs_files1)
    print(f"Found {cs_files1_len} cs files in {folder1}")
    print(f"Found {len(cs_files2)} cs files in {folder2}")

    total_similar_lines = 0
    total_lines = 0
    processed_files = 0

    # Compare each file in folder1 with all files in folder2
    for file1 in cs_files1:
        best_match = None
        best_similarity = 0

        # Find the most similar file in folder2 for each file in folder1
        for file2 in cs_files2:
            similarity = file_similarity(file1, file2)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = file2

        # If the best similarity is above the threshold, count similar lines
        if best_similarity >= similarity_threshold:
            # Count lines in the first file
            lines_in_file1 = count_total_lines(file1)
            total_lines += lines_in_file1  # Add total lines from the first file

            # Calculate similar lines between the two files
            similar_lines = file_similarity(file1, best_match) * lines_in_file1
            total_similar_lines += similar_lines
            line = f"Similar file found for {file1}, similar lines: {similar_lines}"
        else:
            lines_in_file1 = count_total_lines(file1)
            total_lines += lines_in_file1
            line = f"No similar file found for {file1}, lines: {lines_in_file1}"
        
        processed_files += 1
        print(f"[{str(processed_files).zfill(4)}/{str(cs_files1_len).zfill(4)}]\t{line}")

    # Print overall results
    print(f"Total similar lines across all .cs files: {total_similar_lines}")
    print(f"Total lines across all .cs files: {total_lines}")
    print(f"Total similarity: {(total_similar_lines/total_lines):.2%}")

def main():
    """
    Main function to handle command-line arguments and trigger folder comparison.
    
    Args:
        None
        
    Returns:
        None
    """
    if len(sys.argv) < 3:
        print("Usage: python compare_folders.py <folder1> <folder2> [similarity_threshold]")
        sys.exit(1)
    
    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    
    # Default threshold to 0.8 if not provided
    if len(sys.argv) >= 4:
        try:
            similarity_threshold = float(sys.argv[3])
            if not 0.0 <= similarity_threshold <= 1.0:
                raise ValueError
        except ValueError:
            print("Error: Similarity threshold must be a float between 0.0 and 1.0")
            sys.exit(1)
    else:
        similarity_threshold = 0.8

    if not os.path.exists(folder1):
        print(f"Error: Folder '{folder1}' does not exist")
        raise FileNotFoundError
        
    if not os.path.exists(folder2):
        print(f"Error: Folder '{folder2}' does not exist")
        raise FileNotFoundError

    # Compare the folders
    compare_folders(folder1, folder2, similarity_threshold)

if __name__ == "__main__":
    main()
