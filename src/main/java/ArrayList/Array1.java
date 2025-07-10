package ArrayList;

public class Array1 {

    public static void main(String[] args) {
        double[] a = new double[5];
        a[0] = 1;
        a[2] = 2;
        a[4] = 5;
        for( int i =0; i < a.length; i++ ) {
            System.out.println("Element at index " + i + ": " + a[i] );
        }

        //System.out.println("Element at index " + 5 + ": " + a[5] );

        System.out.println("\nArray copied:");
        double[] b = new double[10];
        System.arraycopy(a, 3, b, 5, a.length);


        for( int i =0; i < b.length; i++ ) {
            System.out.println("Element at index " + i + ": " + b[i] );
        }
    }
}