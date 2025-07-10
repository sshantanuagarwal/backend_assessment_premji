package Class;

import java.util.ArrayList;

public class Student {
    String name;
    int age;

    private static int counter = 0;

    Student(String name){
        this.name = name;
        counter++;
    }

    Student(String name, int age){
        this.name = name; this.age = age;
        counter++;
    }

    public static void main(String[] args) {
        ArrayList<Student> listOfStudents = new ArrayList<Student>();
        listOfStudents.add( new Student("MNO") );
        listOfStudents.add( new Student("Vicky", 29) );

        listOfStudents.add( new Student("Ssh", 29) );
        listOfStudents.add( new Student("Suresh") );
        listOfStudents.add( new Student("ABC") );
        listOfStudents.add( new Student("XYZ") );

        Student s1 = new Student ("PQR");
        System.out.println("Number of students in class: " + Student.counter);
        System.out.println("Number of students in class: " + s1.counter);

        for(Student s : listOfStudents) {
            System.out.println( "Name: " + s.name + "\t Age: " + s.age);
        }
    }

}
