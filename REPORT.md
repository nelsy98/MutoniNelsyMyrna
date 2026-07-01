# Student Record Management System Report

Program Design
The Student Record Management System is a menu-driven Python application that manages student records.
It stores student details in CSV for core information and JSON for additional details such as address, contact, and program.
The application also writes all user actions and errors to a log file.

Key Functions
add_student(): collects student data, validates it, and saves it to the data files.
view_students(): displays all stored student records.
search_student(): finds a student by registration number.
update_student(): changes existing student details while preserving valid data.
delete_student(): removes a student record from the system.
load_data() and save_data(): handle reading and writing data files.

Exception Handling Strategy
The program uses try, except, and finally blocks to manage errors gracefully.
A custom exception, StudentDataError, is used for invalid student input and business-rule violations e.g. duplicate registration numbers.
File and unexpected runtime errors are also captured and logged.

Testing Results
The application was tested by running the program and using the menu options to add, view, search, update, and delete student records. The system successfully created and updated the CSV, JSON, and log files.
Invalid inputs such as duplicate registration numbers were reported with error messages and logged.
