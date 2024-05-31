# matrix_l_classes.py

import numpy as np

class MatrixL:
    def __init__(self, text, pattern, k):
        self.text = text
        self.pattern = pattern
        self.k = k
        self.n = len(text)
        self.m = len(pattern)
        self.D = np.full((self.m + 1, self.n + 1), np.inf)
        self.L = np.full((self.n + self.k + 1, self.k + 1), -1)
        self.suffix_tree = None  # Placeholder for the suffix tree

    def compute_matrix_d(self):
        """Compute the dynamic programming matrix D."""
        for i in range(self.m + 1):
            self.D[i][0] = i
        for j in range(self.n + 1):
            self.D[0][j] = 0
        for i in range(1, self.m + 1):
            for j in range(1, self.n + 1):
                cost = 0 if self.pattern[i - 1] == self.text[j - 1] else 1
                self.D[i][j] = min(
                    self.D[i - 1][j] + 1,     # Deletion
                    self.D[i][j - 1] + 1,     # Insertion
                    self.D[i - 1][j - 1] + cost  # Substitution
                )

    def compute_l_values(self):
        """Compute the L values using the dynamic programming matrix D."""
        for e in range(self.k + 1):
            for d in range(-e, self.n - self.m + e + 1):
                row = max(
                    self.L[d - 1 + self.k][e - 1] + 1 if d - 1 >= -self.k else 0,
                    self.L[d + self.k][e - 1],
                    self.L[d + 1 + self.k][e - 1] + 1 if d + 1 <= self.k else 0
                )
                row = min(row, self.m)
                while row < self.m and row + d < self.n and self.pattern[row] == self.text[row + d]:
                    row += 1
                self.L[d + self.k][e] = row
                if row == self.m and d + self.m <= self.n:
                    print(f"Occurrence ending at index {d + self.m - 1}")

    def compute_matrix_l(self):
        """Compute the matrix L."""
        self.compute_matrix_d()
        self.compute_l_values()

def compute_matrix_l_with_input(text, pattern, k):
    """Compute the L matrix with provided inputs."""
    matrix_l = MatrixL(text, pattern, k)
    matrix_l.compute_matrix_l()

