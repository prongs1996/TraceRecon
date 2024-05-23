# main.py

from matrix_l_classes import compute_matrix_l_with_input

def read_lines(file_path):
    # Read the first three lines from the text file
    with open(file_path, 'r') as file:
        lines = [file.readline().strip() for _ in range(3)]
    return lines

def process_lines(lines, blockLength, anchorLength, max_errors):
    first_line, second_line, third_line = lines

    # Split the first line into equal substrings of length blockLength
    blocks = [first_line[i:i + blockLength] for i in range(0, len(first_line), blockLength)]

    # Take a substring of each block consisting of the middle anchorLength characters
    anchors = [block[(blockLength - anchorLength) // 2: (blockLength + anchorLength) // 2] for block in blocks]

    results = []
    for anchor in anchors:
        # Find the starting index of the anchor in the second line
        start_index = compute_matrix_l_with_input(max_errors, second_line, anchor)
        if start_index is not None:
            # Calculate the substring from the second line
            temp_block2 = second_line[start_index - (blockLength - anchorLength) // 2: start_index - (blockLength - anchorLength) // 2 + blockLength]
            results.append(temp_block2)
        
        # Find the starting index of the anchor in the third line
        start_index = compute_matrix_l_with_input(max_errors, third_line, anchor)
        if start_index is not None:
            # Calculate the substring from the third line
            temp_block3 = third_line[start_index - (blockLength - anchorLength) // 2: start_index - (blockLength - anchorLength) // 2 + blockLength]
            results.append(temp_block3)
    
    return results

def main():
    file_path = 'path_to_your_text_file.txt'
    blockLength = 10
    anchorLength = 4
    max_errors = 2

    lines = read_lines(file_path)
    results = process_lines(lines, blockLength, anchorLength, max_errors)

    for result in results:
        print(result)

if __name__ == "__main__":
    main()
