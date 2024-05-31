# main.py

from LV89test import comMatrix
import statistics

def read_lines(file_path):
    # Read the first three lines from the text file
    with open(file_path, 'r') as file:
        lines = [file.readline().strip() for _ in range(3)]
    return lines

def process_lines(lines, blockLength, anchorLength, max_errors):
    first_line, second_line, third_line = lines

    # Split the first line into equal substrings of length blockLength
    blocks = [first_line[i:i + blockLength] for i in range(0, len(first_line), blockLength)]

    finalString = ""

    for block in blocks:
        # Take a substring of each block consisting of the middle anchorLength characters
        anchor = block[(blockLength - anchorLength) // 2: (blockLength + anchorLength) // 2]

        # Find the starting index of the anchor in the second line
        start_index2 = comMatrix(max_errors, second_line, anchor)
        tempBlock2 = None
        if start_index2 is not None:
            # Calculate the substring from the second line
            tempBlock2 = second_line[start_index2 - (blockLength - anchorLength) // 2: start_index2 - (blockLength - anchorLength) // 2 + blockLength]
        
        # Find the starting index of the anchor in the third line
        start_index3 = comMatrix(max_errors, third_line, anchor)
        tempBlock3 = None
        if start_index3 is not None:
            # Calculate the substring from the third line
            tempBlock3 = third_line[start_index3 - (blockLength - anchorLength) // 2: start_index3 - (blockLength - anchorLength) // 2 + blockLength]

        # Collect non-None blocks
        blocks_to_consider = [block]
        if tempBlock2 is not None:
            blocks_to_consider.append(tempBlock2)
        if tempBlock3 is not None:
            blocks_to_consider.append(tempBlock3)

        # Find the median string of block, tempBlock2, and tempBlock3
        median_string = statistics.median(blocks_to_consider)

        # Add the median string to finalString
        finalString += median_string
    
    return finalString

def main():
    file_path = 'sampleDna.txt'
    blockLength = 10
    anchorLength = 4
    max_errors = 2

    lines = read_lines(file_path)
    finalString = process_lines(lines, blockLength, anchorLength, max_errors)

    print(f"Final String: {finalString}")

if __name__ == "__main__":
    main()
