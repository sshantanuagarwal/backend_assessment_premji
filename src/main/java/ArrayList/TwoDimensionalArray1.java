package ArrayList;

import java.util.Random;

public class TwoDimensionalArray1 {

    public static final int N = 3;
	public static final int M = 3;

	public static void print(int[][] arr) {
		System.out.println("=========Array:============");
		for(int i =0; i < arr.length; i ++ ) {
			// arr[i] <- i th row

			System.out.print( (i+1) + "th ROW elements:\t" );
			for(int j = 0; j < arr[i].length; j++) {
				System.out.print( arr[i][j] + "\t" );
			}
			System.out.println();
		}
		System.out.println("\n");
	}

	public static void insert( int[][] arr) {

		Random rand = new Random();
		for( int i =0 ; i < arr.length; i ++ ) {
			for(int j = 0; j < arr[i].length; j++ ){
				arr[i][j] = Math.abs(rand.nextInt()) % 10;
			}
		}
		print(arr);
	}

	public static void add (int[][] arr1, int[][] arr2){
		System.out.println("=========Addition:============");

		int[][] resultArray = new int[N][M];
		for( int i =0 ; i < N; i ++ ) {
			for(int j = 0; j < M; j++ ){
				resultArray[i][j] =arr1[i][j] + arr2[i][j];
			}
		}
		print(resultArray);
	}

	public static void multiply (int[][] arr1, int[][] arr2){
		System.out.println("=========Multiplication:============");

		int[][] resultArray = new int[N][M];
		for( int i =0 ; i < N; i ++ ) {
			for(int j = 0; j < M; j++ ){
				resultArray[i][j]= 0;
				for(int k = 0; k < M; k++ ){
					resultArray[i][j]+= arr1[i][k] * arr2[k][j];
				}
			}
		}
		print(resultArray);
	}

	public static void transpose(int[][] arr){
		System.out.println("=========Tranposition:============");

		int[][] resultArray = new int[M][N];
		for( int i =0 ; i < N; i ++ ) {
			for(int j = 0; j < M; j++ ){
				resultArray[j][i]= arr[i][j];
			}
		}
		print(resultArray);
	}

	public static void transposeInline(int[][] arr) {
		System.out.println("=========Transposition Inline:============");
	}

	public static void printBoundaryInline(int[][] arr) {
		System.out.println("=========Print Boundary Inline:============");

	}

	public static void main(String[] args) {
		int[][] arr1 = new int[N][M];
		int[][] arr2 = new int[N][M];
		insert(arr1);
		insert(arr2);
		add(arr1,arr2);
		multiply(arr1,arr2);
		transpose(arr1);
	}
}
