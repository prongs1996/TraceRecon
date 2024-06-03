import java.util.Arrays;
public class SuffixArray {
    private Suffix[] suffixes;
    private static final int MAXCAPACITY = 5000;
    private int[] lcp = new int [MAXCAPACITY];
    public SuffixArray(String str) {
        int N = str.length();
        this.suffixes = new Suffix[N];
        for (int i = 0; i < N; i++)
            suffixes[i] = new Suffix(str, i);
        Arrays.sort(suffixes);        
        buildLCP(str);
    }
    private static class Suffix implements Comparable<Suffix> {
        private final String text;
        private final int index;
        private Suffix(String text, int index) {
            this.text = text;
            this.index = index;
        }
        private int length() {
            return text.length() - index;
        }
        private char charAt(int i) {
            return text.charAt(index + i);
        }
        public int compareTo(Suffix that) {
            if (this == that) return 0;
            int N = Math.min(this.length(), that.length());
            for (int i = 0; i < N; i++) {
                if (this.charAt(i) < that.charAt(i)) 
                	return -1;
                if (this.charAt(i) > that.charAt(i)) 
                	return +1;
            }
            return this.length() - that.length();
        }     
        public String toString() {
            return text.substring(index);
        }
    }
    public int length() {
        return suffixes.length;
    }
    public int index(int i) {
        if (i < 0 || i >= suffixes.length) throw new IndexOutOfBoundsException();
        return suffixes[i].index;
    }
    public int lcp(int i) {
        if (i < 1 || i >= suffixes.length) throw new IndexOutOfBoundsException();     
        lcp [i] = lcp(suffixes[i], suffixes[i-1]);
        return lcp[i];
    }
    private static int lcp (Suffix s, Suffix t) {
        int N = Math.min(s.length(), t.length());
        for (int i = 0; i < N; i++) {
            if (s.charAt(i) != t.charAt(i)) return i;
        }
        return N;
    }
    public String select(int i) {
        if (i < 0 || i >= suffixes.length) 
        	throw new IndexOutOfBoundsException();
         return suffixes[i].toString();
    }
    public int rank(String query) {
        int lo = 0, hi = suffixes.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int cmp = compare(query, suffixes[mid]);
            if (cmp < 0) hi = mid - 1;
            else if (cmp > 0) lo = mid + 1;
            else return mid;
        }
        return lo;
    }
    private static int compare(String query, Suffix suffix) {
        int N = Math.min(query.length(), suffix.length());
        for (int i = 0; i < N; i++) {
            if (query.charAt(i) < suffix.charAt(i)) return -1;
            if (query.charAt(i) > suffix.charAt(i)) return +1;
        }
        return query.length() - suffix.length();
    }
    public void print (String s){
    	System.out.println("  i ind lcp rnk select");
    	System.out.println("---------------------------");
    	for (int i = 0; i < s.length(); i++) {
    		int index = index(i);
    		String ith = "\"" + s.substring(index, Math.min(index + 50, s.length())) + "\"";
    		assert s.substring(index).equals(select(i));
    		int rank = rank(s.substring(index));
    		if (i == 0) 
    			System.out.printf("%3d %3d %3s %3d %s\n", i, index, "-", rank, ith);    		
    		else {
    			int lcp = lcp(i);
    			System.out.printf("%3d %3d %3d %3d %s\n", i, index, lcp, rank, ith);
    		}
    	}
    }
    public void buildLCP (String s){
    	for (int i = 1; i < s.length(); i++) {
    			int lcp = lcp(i);
    	}
    }
    public String concat (String pattern, String text){
    	StringBuilder sb = new StringBuilder();
    	sb= sb.append(pattern).append('#').append(text);
    	System.out.println (sb);
    	return sb.toString();
    }
    public int calculateLCP (String str, int query1, int query2, int textLen, int patternLen){    	
    	int rank1, rank2, rmqResult=-1;
    	if (query1 >= textLen) return 0;
    	else if (query2 > textLen + patternLen) return 0;
    	rank1 = rank(str.substring(query1));
    	rank2 = rank(str.substring(query2));
    	System.out.println ("The rank of query 1 in the LCP array is: " + rank1);
    	System.out.println( "The rank of query 2 in the LCP array is: " + rank2);
        if (rank1<rank2)
        	rank1++;
        else
        	rank2++;
        RMQ array = new RMQ(lcp);
        rmqResult = array.query(rank1, rank2);
    	System.out.println("The RMQ is: " + lcp (rmqResult));    	
    	return lcp(rmqResult);
    }
    public static void main(String[] args) {
    }
}