import numpy as np

class SuffixArray:
    def __init__(self, s):
        self.s = s
        self.n = len(s)
        # Build the suffix array and LCP array
        self.suffix_array = self.build_suffix_array()
        self.lcp_array = self.compute_lcp()

    def build_suffix_array(self):
        # Create and sort suffixes
        suffixes = [(self.s[i:], i) for i in range(self.n)]
        suffixes.sort()
        # Return the starting indices of sorted suffixes
        return [suffix[1] for suffix in suffixes]

    def compute_lcp(self):
        # Compute the Longest Common Prefix (LCP) array
        lcp = [0] * self.n
        rank = [0] * self.n
        for i, suffix in enumerate(self.suffix_array):
            rank[suffix] = i
        h = 0
        for i in range(self.n):
            if rank[i] > 0:
                j = self.suffix_array[rank[i] - 1]
                while i + h < self.n and j + h < self.n and self.s[i + h] == self.s[j + h]:
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1
        return lcp

class RMQ:
    def __init__(self, array):
        self.array = array
        self.n = len(array)
        # Precompute the RMQ table
        self.precompute_rmq()

    def precompute_rmq(self):
        # Initialize the RMQ table
        self.rmq = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            self.rmq[i][i] = i
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.array[j] < self.array[self.rmq[i][j - 1]]:
                    self.rmq[i][j] = j
                else:
                    self.rmq[i][j] = self.rmq[i][j - 1]

    def query(self, i, j):
        # Query the minimum value in the range [i, j]
        return self.array[self.rmq[i][j]]

class MatrixL:
    def __init__(self, max_errors, text, pattern):
        self.k = max_errors
        self.text = text
        self.pattern = pattern
        self.n = len(text)
        self.m = len(pattern)
        # Concatenate the text and pattern with a delimiter
        self.str = self.concat(text, pattern)
        # Initialize the suffix array
        self.suffix_array = SuffixArray(self.str)
        # Initialize the matrix
        self.matrix = np.zeros((self.n - self.m + self.k + 1, self.k + 1), dtype=int)

    def concat(self, string1, string2):
        # Concatenate two strings with a delimiter
        return string1 + '#' + string2

    def init_step_two(self):
        # Initialize matrix according to step two of the algorithm
        for d, i in zip(range(-self.k, 0), range(1, self.k + 1)):
            self.matrix[self.transform(d, self.k)][self.k - i] = self.k - i

    def init_step_three(self):
        # Initialize matrix according to step three of the algorithm
        for d, i in zip(range(-self.k, 0), range(1, self.k + 1)):
            self.matrix[self.transform(d, self.k)][self.k - i + 1] = self.k - i + 1

    def transform(self, x, y):
        # Transform logical index to physical index
        return x + y

    def fill_matrix(self):
        # Fill the matrix according to the Landau-Vishkin algorithm
        for e in range(1, self.k + 1):
            for d in range(-e, self.n - self.m + e + 1):
                row = max(
                    self.matrix[self.transform(d - 1, e - 1)][e - 1] + 1 if d - 1 >= -self.k else 0,
                    self.matrix[self.transform(d, e - 1)][e - 1],
                    self.matrix[self.transform(d + 1, e - 1)][e - 1] + 1 if d + 1 <= self.k else 0
                )
                row = min(row, self.m)
                self.matrix[self.transform(d, e)][e] = self.m + self.lcp(row + d, row + self.n + 1)
                if self.matrix[self.transform(d, e)][e] == self.m and d + self.m <= self.n:
                    print(f"Occurrence ending at index {d + self.m - 1}")

    def lcp(self, x, y):
        # Compute the LCP for given indices
        return self.suffix_array.lcp_array[min(self.suffix_array.suffix_array.index(x), self.suffix_array.suffix_array.index(y))]

    def print_matrix(self):
        # Print the matrix
        for row in self.matrix:
            print(' '.join(map(str, row)))

    def compute_matrix_l(self):
        # Compute the L matrix
        self.init_step_two()
        self.init_step_three()
        self.fill_matrix()
        self.print_matrix()

def comMatrix(max_errors, text, pattern):
    # Function to compute the L matrix with provided inputs
    matrix_l = MatrixL(max_errors, text, pattern)
    matrix_l.compute_matrix_l()

# Example usage
if __name__ == "__main__":
    # Example with predefined values
    max_errors = 2
    text = "exampletext"
    pattern = "text"
    comMatrix(max_errors, text, pattern)
    
    # Uncomment the following lines to test with different inputs
    # max_errors = 3
    # text = "yourtext"
    # pattern = "yourpattern"
    # comMatrix(max_errors, text, pattern)
