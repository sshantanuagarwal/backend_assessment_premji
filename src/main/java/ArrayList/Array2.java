package ArrayList;
public class Array2 {
    public static void main(String[] args) {
        int[] a = new int[5];
        a[0] = 10;

        for( int i =0; i < a.length; i++ ) {
            System.out.println("Element at index " + i + ": " + a[i] );
        }

        int[] b = new int[10];

        System.arraycopy(a,0,b,0, a.length);
        for( int i =0; i < b.length; i++ ) {
            System.out.println("Element at index " + i + ": " + b[i] );
        }
    }
}