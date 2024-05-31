import numpy as np

def read_lines_from_file(file_path):
    """
    Read the first three lines from a file and return them as strings.

    Parameters:
    file_path (str): The path to the input file.

    Returns:
    tuple: A tuple containing the first, second, and third lines as strings.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines[0], lines[1], lines[2]

def split_into_blocks(line, block_length):
    """
    Split a line into equal-length blocks.

    Parameters:
    line (str): The input line to be split.
    block_length (int): The length of each block.

    Returns:
    list: A list of blocks.
    """
    return [line[i:i + block_length] for i in range(0, len(line), block_length)]

def extract_anchor(block, anchor_length):
    """
    Extract the middle anchor_length number of characters from a block.

    Parameters:
    block (str): The input block.
    anchor_length (int): The length of the anchor.

    Returns:
    str: The extracted anchor.
    """
    start = (len(block) - anchor_length) // 2
    return block[start:start + anchor_length]

def compute_median_string(blocks):
    """
    Compute the median string of given blocks.

    Parameters:
    blocks (list): A list of blocks.

    Returns:
    str: The computed median string.
    """
    block_length = len(blocks[0])
    median_string = ""
    for i in range(block_length):
        column_chars = [block[i] for block in blocks]
        median_char = max(set(column_chars), key=column_chars.count)
        median_string += median_char
    return median_string

# def find_starting_index(line, anchor):
   
    # """
    # Find the starting index of the best match of the anchor in the given line.

    # Parameters:
    # line (str): The line in which to search for the anchor.
    # anchor (str): The anchor string to find.

    # Returns:
    # int: The starting index of the best match.
    # """
    # min_distance = float('inf')
    # best_index = 0
    # for i in range(len(line) - len(anchor) + 1):
    #     substring = line[i:i + len(anchor)]
    #     distance = sum(1 for a, b in zip(substring, anchor) if a != b)
    #     if distance < min_distance:
    #         min_distance = distance
    #         best_index = i
    # return best_index
    #
    # this part should be done with the function imported from LV89

def compute_median_blocks(file_path, block_length, anchor_length):
    """
    Read three lines from a file and compute the median DNA string.

    Parameters:
    file_path (str): The path to the input file.
    block_length (int): The length of each block.
    anchor_length (int): The length of each anchor.
    """
    # Read the first three lines from the file
    line1, line2, line3 = read_lines_from_file(file_path)
    
    # Split the first line into blocks of block_length
    blocks = split_into_blocks(line1, block_length)
    
    # Initialize the final string
    final_string = ""

    # Process each block
    for block in blocks:
        # Extract the anchor from the block
        anchor = extract_anchor(block, anchor_length)
        
        # Find the starting index of the anchor in the second line
        start_index2 = find_starting_index(line2, anchor)
        
        # Find the starting index of the anchor in the third line
        start_index3 = find_starting_index(line3, anchor)
        
        # Calculate the substring from the second line
        temp_block2_start = start_index2 - (block_length - anchor_length) // 2
        temp_block2 = line2[temp_block2_start:temp_block2_start + block_length]
        
        # Calculate the substring from the third line
        temp_block3_start = start_index3 - (block_length - anchor_length) // 2
        temp_block3 = line3[temp_block3_start:temp_block3_start + block_length]
        
        # Compute the median string of block, temp_block2, and temp_block3
        median_block = compute_median_string([block, temp_block2, temp_block3])
        
        # Add the median block to the final string
        final_string += median_block

    # Print the final median string
    print(final_string)

# Usage
compute_median_blocks('sampleDna.txt', block_length=10, anchor_length=4)
