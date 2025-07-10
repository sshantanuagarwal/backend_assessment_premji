package ArrayList;
import java.util.Arrays;

public class ArraySearch {

    public static boolean findElement(int[] a, int k) {

        // o(n)
        for(int i = 0; i < a.length; i++) {
            if( a[ i ] == k ) {
                return true;
            }
        }
        return false;
    }


    public static void main(String[] args) {
        int[] a = {1,2,3,4,5};

        int sum = 0;
        for(int i = 0; i < a.length; i++) {
            sum += a[i];
        }
        System.out.println("Sum of array:" + Arrays.toString(a) + " = " + sum);

        System.out.println( findElement(a, 6));
    }
}
