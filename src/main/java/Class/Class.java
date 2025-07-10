package Class;

public class Class {
    static final String schoolName = "ABC";

    static final int a = 0;
    static int b = 0;
    int c = 0;

    private static int count = 0;

    Class() {
        count++;
    }

    void set( int i, int j, int k) {
        //this.a = i;
        //this.b = j;
        this.c = k;
    }

    void show() {
        System.out.println("Final  a:" + a);
        System.out.println("Static b:" + b);
        System.out.println("Normal c:" + c);
    }

    public static void main(String[] args) {

        Class c1 = new Class();
        Class c2 = new Class();

        c1.set(1,1,1);
        c1.show(); // 0 1 1
        c2.set(2,2,2);
        c2.show(); // 0 2 2
        c1.show(); // 0 2 1
    }
}
