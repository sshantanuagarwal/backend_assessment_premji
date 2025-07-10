package ArrayList;

import java.util.Arrays;
import java.util.Random;

public class AssignmentArray {

    public static void print(int[] arr) {
        for(int i = 0; i < arr.length; i++) {
            System.out.print(arr[ i ] + " ");
        }
        System.out.println();
    }

    public static void question1(int[] arr) {
        System.out.println("\n========Question 1==========\n");
        for(int i = 0; i < arr.length; i++) {
            for(int j = i+1; j < arr.length; j++) {
                if(arr[i] > arr[j]) {
                    int tmp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = tmp;
                }
            }
        }
        print(arr);
    }
    public static void question2(int[] arr) {
        System.out.println("\n========Question 2==========\n");
        int sum = 0;
        for(int i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        System.out.println("Sum = " + sum);
    }


    public static void question3(int[] arr) {
        System.out.println("\n========Question 3==========\n");
        for(int i = 0; i < arr.length; i++) {
            for(int j = 0; j < arr.length; j++) {
                System.out.print("- ");
            }
            System.out.println();
        }
    }


    public static void question4(int[] arr) {
        System.out.println("\n========Question 4==========\n");
        int sum = 0;
        for(int i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        System.out.println("Average = " + sum/arr.length);
    }


    public static void question5(int[] arr) {
        System.out.println("\n========Question 5==========\n");
        int k = 10;
        boolean found = false;
        for(int i = 0; i < arr.length; i++) {
            if(arr[i] == k) {
                found = true;
                break;
            }
        }
        System.out.println("Element " + k + " is " +
                (found ? "found" : "not found") + " in array"  );
    }


    public static void question6(int[] arr) {
        System.out.println("\n========Question 6==========\n");
        int k = arr[5];
        for(int i = 0; i < arr.length; i++) {
            if(arr[i] == k) {
                System.out.println("Element " + k + "is in array at index " + i  );
                return;
            }
        }
    }

    public static void question7(int[] arr) {
        System.out.println("\n========Question 7==========\n");
        int k = arr[5];
        int pos = 5;
        for( int j = pos; j < arr.length - 1; j++) {
            arr[j] = arr[j+1];
        }
        print(arr);;
    }

    public static void question8(int[] arr) {
        System.out.println("\n========Question 8==========\n");
        int[] arrCopy = new int[arr.length];
        for(int i = 0; i < arr.length; i++) {
            arrCopy[i] = arr[ i ];
         }
        print(arrCopy);
    }

    public static void question9(int[] arr) {
        System.out.println("\n========Question 9==========\n");
        int k = 10;
        int pos = 5;
        for (int j = arr.length - 1; j > pos; j--) {
            arr[j] = arr[j - 1];
        }
        arr[pos] = k;
        print(arr);
    }

    public static void question10(int[] arr) {
        System.out.println("\n========Question 10==========\n");
        int min = 20, max = -1;
        for( int i = arr.length-1; i >= 0; i--) {
            if(arr[i] < min)
                min = arr[i];

            if(arr[i] > max)
                max = arr[i];
        }
        System.out.println("minimum value: " + min + " Maximum value: " + max);
    }


    public static void question11(int[] arr) {
        System.out.println("\n========Question 11==========\n");
        for( int i = 0; i < arr.length/2; i++) {
            int tmp = arr[i];
            arr[i] = arr[arr.length-i-1];
            arr[arr.length-i-1] = tmp;

        }
        print(arr);
    }

    public static void question12(int[] arr) {
        System.out.println("\n========Question 12==========\n");

        print(arr);
    }


    public static void question13(int[] arr) {
        System.out.println("\n========Question 13==========\n");

        print(arr);
    }


    public static void question14(int[] arr) {
        System.out.println("\n========Question 14==========\n");

        print(arr);
    }


    public static void question15(int[] arr) {
        System.out.println("\n========Question 15==========\n");

        print(arr);
    }


    public static void question16(int[] arr) {
        System.out.println("\n========Question 16==========\n");

        print(arr);
    }


    public static void question17(int[] arr) {
        System.out.println("\n========Question 17==========\n");

        print(arr);
    }


    public static void question18(int[] arr) {
        System.out.println("\n========Question 18==========\n");

        print(arr);
    }
    public static void question19(int[] arr) {
        System.out.println("\n========Question 19==========\n");

        print(arr);
    }

    public static void question20(int[] arr) {
        System.out.println("\n========Question 20==========\n");

        print(arr);
    }
    public static void main(String[] args) {
        int[]  arr = new int[10];
        Random randNum = new Random();
        for (int i = 0; i < 10; i++) {
            arr[i] = Math.abs(randNum.nextInt()) % 20;
        }
        print(arr);
        question1(arr);
        question2(arr);
        question3(arr);
        question4(arr);
        question5(arr);
        question6(arr);
        question7(arr);
        question8(arr);
        question9(arr);
        question10(arr);
        question11(arr);
        question12(arr);
        question13(arr);
        question14(arr);
        question15(arr);
        question16(arr);
        question17(arr);
        question18(arr);
        question19(arr);
        question20(arr);
    }
}
