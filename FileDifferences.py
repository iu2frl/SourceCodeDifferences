import os
import difflib

def get_cs_files(directory):
    """Recursively get all .cs files in the directory."""
    cs_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                cs_files.append(os.path.join(root, file))
    return cs_files

def count_total_lines(file):
    """Count the total number of lines in a file."""
    try:
        with open(file, 'r') as f:
            fileContent = f.readlines()
    except:
        try:
            with open(file, 'r', encoding="utf-8") as f:
                fileContent = f.readlines()
        except:
            return 0
        
    return len([line for line in fileContent if not line.startswith("//")])

def file_similarity(file1, file2):
    """Compare two files and return the similarity ratio."""
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
    files_list = [file for file in files_list if '\\Release\\' not in file]
    files_list = [file for file in files_list if '\\Debug\\' not in file]
    return files_list

def compare_folders(folder1, folder2, similarity_threshold=0.8):
    """Compare all .cs files in two folders based on their content and count similar lines."""
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

        for file2 in cs_files2:
            similarity = file_similarity(file1, file2)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = file2

        # If the best similarity is above the threshold, compare them line by line
        if best_similarity >= similarity_threshold:
            #print(f"Comparing {file1} with {best_match} (similarity: {best_similarity:.2%})")

            # Count lines in both files
            lines_in_file1 = count_total_lines(file1)
            total_lines += lines_in_file1  # Add total lines from both files

            # Compare for similar lines using line-by-line comparison
            similar_lines = file_similarity(file1, best_match) * lines_in_file1
            total_similar_lines += similar_lines
            line = f"Similar file found for {file1}, similar lines: {similar_lines}"
        else:
            lines_in_file1 = count_total_lines(file1)
            total_lines += lines_in_file1
            line = f"No similar file found for {file1}, lines: {lines_in_file1}"
        
        processed_files += 1
        print(f"[{str(processed_files).zfill(4)}/{str(cs_files1_len).zfill(4)}]\t{line}")

    print(f"Total similar lines across all .cs files: {total_similar_lines}")
    print(f"Total lines across all .cs files: {total_lines}")
    print(f"Total similarity: {(total_similar_lines/total_lines):.2%}")

# Example usage
if __name__ == "__main__":
    folder1 = r"G:/Documenti/GitHub/OL_Master"
    folder2 = r"G:/Downloads/OpenHPSDR-Thetis-master/Project Files/Source"
    
    compare_folders(folder1, folder2)
