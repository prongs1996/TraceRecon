import java.util.Arrays;
import java.lang.Math;
public class MatrixL {
	private int n, m, k, matrix[][];
	private SuffixArray suffixArray;
	String str;
    public MatrixL (int maxErrors, String text, String pattern){
    	k=maxErrors;
    	n=text.length();
    	m=pattern.length();
		str = concat(text, pattern);
		suffixArray = new SuffixArray(str);
    	matrix = new int [n-m+k+1][k+1]; 
    }
    public void computeMatrixL(){    	
    	initStepTwo();
    	initStepThree();
    	fillMatrix();
    	printMatrix();
    }
    public String concat (String string1, String string2){  
    	return string1 + '#' + string2;
    }
    public void initStepTwo(){    	
    	int d, i, j=k;
    	for (d=-(j), i=1; d < -1 &&  i>=1; d++, i++)
        	matrix[transform(d, j)][j-i]=j-i;
    }
    public void initStepThree (){     	
    	int d, i, j=k;
    	for (d=-(j), i=1; d < 0 &&  i>=1; d++, i++)
        	matrix[transform(d, j)][j-i+1]=j-i+1;
    }
    public  int transform (int x, int k){    	
    	return x+k;
    }
    public void fillMatrix (){    	
        int e, d, row, upperLeft, immediateLeft, lowerLeft;
        boolean isBottomRow=false;
		upperLeft=immediateLeft=lowerLeft=-1;
        for (e=0; e<=k; e++){
        	for (d= (e*-1)+1; d <= n-m; d++){
     		   System.out.println("\nlogical d: " + d + " physical d: " + transform(d,k) + " e: " + e);
     		   	if (e==0){ 
     				upperLeft=immediateLeft=lowerLeft=-1;
     				System.out.println("Immediate left (initialized): " + immediateLeft);
     				System.out.println("Lower left (initialized): " + lowerLeft);
     				System.out.println("Upper left (initialized): " + upperLeft);     				
     			}
     			else{ 
     				immediateLeft=matrix[transform(d, k)][e-1];
     				System.out.println("Immediate left: " + matrix[transform(d, k)][e-1]);
 					upperLeft=matrix[transform(d-1, k)][e-1];
     				System.out.println("Upper left: " + matrix[transform(d-1, k)][e-1]);
     				if(transform(d, k)<transform(n-m, k)){
     					lowerLeft=matrix[transform(d+1, k)][e-1];
         				System.out.println("Lower left: " + matrix[transform(d+1, k)][e-1]);
     				}
     				else{     					
     					System.out.print ("Cannot read from spot to bottom left at: " + transform(d+1, k) + " ");
     					System.out.println (e-1);
     					isBottomRow=true;
     				}     				
     			}
     			if (isBottomRow=true){
     				row = Math.max(upperLeft+1, immediateLeft+1);
     				System.out.println("max: " + row);
     				isBottomRow=false;
     			}
     			else{
    				 row =  Math.max(Math.max(immediateLeft+1,lowerLeft),upperLeft+1);
    				 System.out.println("max: " + row);
     			}     			
     			row = Math.min(row, m);
     			System.out.println("m: " + m);
     			System.out.println("row: "+row);
     			int lcp= suffixArray.calculateLCP (str, row+d, row+n+1, n, m);
     			System.out.println("lcp: " + lcp);     			
     			matrix[transform(d, k)][e]= row + lcp;
     			System.out.println("matrix element: " + matrix[transform(d, k)][e]);	
         	}
         }
    }
    public void printMatrix() {	
    	for (int[] row : matrix)
	        System.out.println(Arrays.toString(row));       
    }
    public static void main(String[] args)  {	
    	int maxErrors=2;
    	String text = "baananaaan";
    	String pattern = "aaa";
    	MatrixL matrixL = new MatrixL (maxErrors, text, pattern);
    	matrixL.computeMatrixL();
    }
}