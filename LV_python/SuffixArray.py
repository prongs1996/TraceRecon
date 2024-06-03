class Suffix:
    def __init__(self, text, index):
        self.text = text
        self.index = index

    def __lt__(self, other):
        # Python's sort uses < comparison by default
        return self.text[self.index:] < other.text[other.index:]

    def length(self):
        return len(self.text) - self.index

    def char_at(self, i):
        return self.text[self.index + i]

class SuffixArray:
    def __init__(self, s):
        self.suffixes = [Suffix(s, i) for i in range(len(s))]
        self.suffixes.sort()
        self.lcp = self.build_lcp(s)

    def build_lcp(self, s):
        n = len(self.suffixes)
        lcp = [0] * n
        for i in range(1, n):
            lcp[i] = self.lcp_suffix(self.suffixes[i - 1], self.suffixes[i])
        return lcp

    def lcp_suffix(self, s1, s2):
        i = 0
        while i < s1.length() and i < s2.length() and s1.char_at(i) == s2.char_at(i):
            i += 1
        return i

# Example usage
s = "banana"
suffix_array = SuffixArray(s)
print("Sorted Suffixes:", [s.suffixes[i].text[s.suffixes[i].index:] for i in range(len(s.suffixes))])
print("LCP Array:", suffix_array.lcp)
