package ArrayList;

public class HelloWorld {
    String name;
    int a;
    Integer age = null;
    Character gender;
    Float marks = null;
    Double totalMarks;


    HelloWorld(String data) {
        this.name = data;
    }

    HelloWorld(String data, int age) {
        this.name = data;
        this.age = age;
    }

    public static int add( int a, int b ) {
        return a+b;
    }

    public static int sub( int a, int b ) {
        return a-b;
    }

    void printInfo() {
        System.out.print("Hello " + this.name);
        if(this.age != null) {
            System.out.println(". My age is " + this.age);
        }
        System.out.println("\n");

    }
    public static void main(String[] args) {

        HelloWorld helloSuresh = new HelloWorld("Suresh");
        helloSuresh.printInfo();

        HelloWorld helloVicky = new HelloWorld("Vicky");
        helloVicky.printInfo();

        HelloWorld helloSsh = new HelloWorld("Ssh", 28);
        helloSsh.printInfo();

        System.out.println(HelloWorld.sub(1,2) );
        System.out.println(HelloWorld.add(1,2) );


        System.out.println( sub(1,2) );
        System.out.println( add(1,2) );



    }
}
