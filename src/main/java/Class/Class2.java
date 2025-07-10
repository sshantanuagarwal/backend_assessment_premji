package Class;

public class Class2 {
    public static void main(String[] args) {
        System.out.println("Value of final a" + Class.a);

        Class.b = 10;
        String[] arg = new String[5];
        Class.main(arg);


        //Class.b = 10;
        System.out.println("Value of static b:" + Class.b);

        //System.out.println(Class.c);
    }
}
