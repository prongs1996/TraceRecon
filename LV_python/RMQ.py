class RMQ:
    def __init__(self, input_array):
        self.A = input_array
        self.n = len(self.A)
        self.M = [[0]*self.n for _ in range(self.n)]
        self.fill_M()

    def fill_M(self):
        for i in range(self.n):
            for j in range(i, self.n):
                if i == j:
                    self.M[i][j] = i
                else:
                    self.M[i][j] = j if self.A[j] < self.A[self.M[i][j-1]] else self.M[i][j-1]
                self.M[j][i] = self.M[i][j]

    def query(self, i, j):
        return self.M[i][j]

# Example usage
if __name__ == "__main__":
    arr = [10, 2, 5, 4, 6, 7, 2, 4, 2, 90]
    array = RMQ(arr)
    print(array.query(5, 1))
