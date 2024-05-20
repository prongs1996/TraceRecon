import numpy as np

class RMQ:
    def __init__(self, input_array):
        self.A = input_array
        self.n = len(self.A)
        self.M = np.zeros((self.n, self.n), dtype=int)
        self.fill_M()

    def fill_M(self):
        for i in range(self.n):
            for j in range(i, self.n):
                if i == j:
                    self.M[i][j] = i
                else:
                    self.M[i][j] = j if self.A[j] < self.A[self.M[i][j - 1]] else self.M[i][j - 1]
                self.M[j][i] = self.M[i][j]

    def query(self, i, j):
        return self.M[i][j]

class Suffix:
    def __init__(self, text, index):
        self.text = text
        self.index = index

    def length(self):
        return len(self.text) - self.index

    def charAt(self, i):
        return self.text[self.index + i]

    def __lt__(self, other):
        N = min(self.length(), other.length())
        for i in range(N):
            if self.charAt(i) < other.charAt(i):
                return True
            if self.charAt(i) > other.charAt(i):
                return False
        return self.length() < other.length()

    def __str__(self):
        return self.text[self.index:]

class SuffixArray:
    MAXCAPACITY = 5000

    def __init__(self, text):
        self.suffixes = [Suffix(text, i) for i in range(len(text))]
        self.suffixes.sort()
        self.lcp = np.zeros(len(text), dtype=int)
        self.buildLCP(text)

    def buildLCP(self, text):
        for i in range(1, len(self.suffixes)):
            self.lcp[i] = self.lcp_length(self.suffixes[i], self.suffixes[i - 1])

    def lcp_length(self, s, t):
        N = min(s.length(), t.length())
        for i in range(N):
            if s.charAt(i) != t.charAt(i):
                return i
        return N

    def length(self):
        return len(self.suffixes)

    def index(self, i):
        return self.suffixes[i].index

    def select(self, i):
        return str(self.suffixes[i])

    def rank(self, query):
        lo, hi = 0, len(self.suffixes) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            cmp = self.compare(query, self.suffixes[mid])
            if cmp < 0:
                hi = mid - 1
            elif cmp > 0:
                lo = mid + 1
            else:
                return mid
        return lo

    @staticmethod
    def compare(query, suffix):
        m = min(len(query), suffix.length())
        for i in range(m):
            if query[i] < suffix.charAt(i):
                return -1
            if query[i] > suffix.charAt(i):
                return 1
        return len(query) - suffix.length()

    def calculateLCP(self, text, query1, query2, textLen, patternLen):
        if query1 >= textLen or query2 > textLen + patternLen:
            return 0

        rank1 = self.rank(text[query1:])
        rank2 = self.rank(text[query2:])

        if rank1 < rank2:
            rank1 += 1
        else:
            rank2 += 1

        array = RMQ(self.lcp)
        rmq_result = array.query(rank1, rank2)
        return self.lcp[rmq_result]

class MatrixL:
    def __init__(self, max_errors, text, pattern):
        self.k = max_errors
        self.n = len(text)
        self.m = len(pattern)
        self.str = self.concat(text, pattern)
        self.suffix_array = SuffixArray(self.str)  # Assuming SuffixArray is implemented similarly in Python
        self.matrix = np.zeros((self.n - self.m + self.k + 1, self.k + 1), dtype=int)

    def compute_matrix_l(self):
        self.init_step_two()
        self.init_step_three()
        self.fill_matrix()
        self.print_matrix()

    def concat(self, string1, string2):
        return f"{string1}#{string2}"

    def init_step_two(self):
        d, i, j = -(self.k), 1, self.k
        while d < -1 and i >= 1:
            self.matrix[self.transform(d, j)][j - i] = j - i
            d += 1
            i += 1

    def init_step_three(self):
        d, i, j = -(self.k), 1, self.k
        while d < 0 and i >= 1:
            self.matrix[self.transform(d, j)][j - i + 1] = j - i + 1
            d += 1
            i += 1

    def transform(self, x, y):
        return x + y

    def fill_matrix(self):
        for d in range(-self.k, self.n - self.m + 1):
            for e in range(1, self.k + 1):
                try:
                    immediate_left = self.matrix[self.transform(d, self.k)][e - 1]
                except IndexError:
                    immediate_left = 0

                try:
                    upper_left = self.matrix[self.transform(d - 1, self.k)][e - 1]
                except IndexError:
                    upper_left = 0

                try:
                    lower_left = self.matrix[self.transform(d + 1, self.k)][e - 1]
                except IndexError:
                    lower_left = 0

                if d == self.n - self.m:
                    row = max(immediate_left + 1, upper_left + 1)
                else:
                    row = max(immediate_left + 1, lower_left, upper_left + 1)

                row = min(row, self.m)

                lcp = self.suffix_array.calculateLCP(self.str, row + d, row + self.n + 1, self.n, self.m)
                self.matrix[self.transform(d, self.k)][e] = row + lcp

    def print_matrix(self):
        for row in self.matrix:
            print(row)

# Test the MatrixL data type
if __name__ == "__main__":
    max_errors = 2
    text = "AAAGTGCTTAA"
    pattern = "AAA"

    matrix_l = MatrixL(max_errors, text, pattern)
    matrix_l.compute_matrix_l()
