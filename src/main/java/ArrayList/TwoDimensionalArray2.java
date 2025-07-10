package ArrayList;

public class TwoDimensionalArray2 {

    public static void print(int[][] arr) {
        for(int i =0; i < arr.length; i ++ ) {
            // arr[i] <- i th row

            System.out.print( (i+1) + "th ROW elements:\t" );
            for(int j = 0; j < arr[i].length; j++) {
                System.out.print( arr[i][j] + "\t" );
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {

        int[][] arr = new int[3][];
        arr[0] = new int[]{1,2,3};
        arr[1] = new int[]{4,5};
        arr[2] = new int[]{6,7,8,9,10};
        print(arr);


    }
}
