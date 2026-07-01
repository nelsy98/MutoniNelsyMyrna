import csv
import json
import logging
import re
from datetime import datetime
from pathlib import Path


class StudentDataError(Exception):
    """Raised when student data is missing or invalid."""


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "students.csv"
JSON_PATH = BASE_DIR / "students.json"
LOG_PATH = BASE_DIR / "student_system.log"


def setup_logger():
    """Configure the application logger to write to a file."""
    logger = logging.getLogger("student_system")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


def ensure_data_files():
    """Create CSV, JSON, and log files if they do not exist."""
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["registration_number", "full_name", "age"])
            writer.writeheader()

    if not JSON_PATH.exists(): 
        JSON_PATH.write_text("{}", encoding="utf-8")

    if not LOG_PATH.exists():
        LOG_PATH.touch()


def load_data():
    """Load core student records from CSV and extra details from JSON."""
    ensure_data_files()

    with CSV_PATH.open("r", newline="", encoding="utf-8") as csv_file:
        students = list(csv.DictReader(csv_file))

    try:
        details = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StudentDataError(f"The JSON file is invalid: {exc}") from exc

    if not isinstance(details, dict):
        raise StudentDataError("Student detail data is corrupted.")

    for student in students:
        reg_number = student.get("registration_number", "")
        extra = details.get(reg_number, {})
        student["program"] = extra.get("program", "")
        student["address"] = extra.get("address", "")
        student["contact"] = extra.get("contact", "")

    return students, details


def save_data(students, details):
    """Save student records to both CSV and JSON files."""
    with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["registration_number", "full_name", "age"])
        writer.writeheader()
        for student in students:
            writer.writerow(
                {
                    "registration_number": student["registration_number"],
                    "full_name": student["full_name"],
                    "age": student["age"],
                }
            )

    with JSON_PATH.open("w", encoding="utf-8") as json_file:
        json.dump(details, json_file, indent=2)
        json_file.write("\n")


def validate_registration(reg_number, students):
    """Ensure the registration number is in the expected format and unique."""
    if not re.fullmatch(r"REG\d{3}", reg_number):
        raise StudentDataError("Registration number must follow the format REG001.")

    for student in students:
        if student["registration_number"].upper() == reg_number.upper():
            raise StudentDataError("Registration number already exists.")


def validate_age(age_text):
    """Ensure the age is a valid integer between 16 and 100."""
    try:
        age = int(age_text)
    except ValueError as exc:
        raise StudentDataError("Age must be a whole number.") from exc

    if not 16 <= age <= 100:
        raise StudentDataError("Age must be between 16 and 100.")
    return age


def validate_contact(contact):
    """Validate that the contact field contains a plausible phone number."""
    if not re.fullmatch(r"\+?\d{10,15}", contact):
        raise StudentDataError("Contact must contain 10 to 15 digits, optionally starting with +.")
    return contact


def add_student(logger):
    """Add a new student to the system."""
    students, details = load_data()

    print("\nAdd a New Student")
    print("-" * 30)
    reg_number = input("Enter registration number (e.g. REG003): ").strip().upper()
    full_name = input("Enter full name: ").strip()
    age_text = input("Enter age: ").strip()
    program = input("Enter program: ").strip()
    address = input("Enter address: ").strip()
    contact = input("Enter contact number: ").strip()

    validate_registration(reg_number, students)
    age = validate_age(age_text)
    contact = validate_contact(contact)

    if not full_name or not program or not address:
        raise StudentDataError("Name, program and address cannot be empty.")

    student = {
        "registration_number": reg_number,
        "full_name": full_name,
        "age": age,
    }
    students.append(student)
    details[reg_number] = {
        "program": program,
        "address": address,
        "contact": contact,
    }
    save_data(students, details)
    logger.info("Added student with registration number %s", reg_number)
    print("Student added successfully.")


def view_students(logger):
    """Display all stored students."""
    students, _ = load_data()
    if not students:
        print("No student records found.")
        logger.info("Viewed student records; none were available.")
        return

    print("\nAll Students")
    print("-" * 30)
    for student in students:
        print(
            f"ID: {student['registration_number']} | Name: {student['full_name']} | Age: {student['age']} | "
            f"Program: {student.get('program', '-')} | Address: {student.get('address', '-')} | Contact: {student.get('contact', '-') }"
        )
    logger.info("Viewed all student records.")


def search_student(logger):
    """Search for a student by registration number."""
    students, _ = load_data()
    reg_number = input("Enter registration number to search: ").strip().upper()

    for student in students:
        if student["registration_number"].upper() == reg_number:
            print("\nStudent Found")
            print("-" * 30)
            print(
                f"ID: {student['registration_number']} | Name: {student['full_name']} | Age: {student['age']} | "
                f"Program: {student.get('program', '-')} | Address: {student.get('address', '-')} | Contact: {student.get('contact', '-') }"
            )
            logger.info("Searched for student %s and found a match.", reg_number)
            return

    raise StudentDataError("No student found with that registration number.")


def update_student(logger):
    """Update an existing student's basic information."""
    students, details = load_data()
    reg_number = input("Enter registration number to update: ").strip().upper()

    student = None
    for item in students:
        if item["registration_number"].upper() == reg_number:
            student = item
            break

    if student is None:
        raise StudentDataError("No student found with that registration number.")

    print("\nUpdate Student Details")
    print("-" * 30)
    new_name = input(f"Enter new full name (leave blank to keep '{student['full_name']}'): ").strip()
    new_age = input(f"Enter new age (leave blank to keep '{student['age']}'): ").strip()
    new_program = input(f"Enter new program (leave blank to keep '{details[reg_number].get('program', '')}'): ").strip()
    new_address = input(f"Enter new address (leave blank to keep '{details[reg_number].get('address', '')}'): ").strip()
    new_contact = input(f"Enter new contact (leave blank to keep '{details[reg_number].get('contact', '')}'): ").strip()

    if new_name:
        student["full_name"] = new_name
    if new_age:
        student["age"] = validate_age(new_age)
    if new_program:
        details[reg_number]["program"] = new_program
    if new_address:
        details[reg_number]["address"] = new_address
    if new_contact:
        details[reg_number]["contact"] = validate_contact(new_contact)

    save_data(students, details)
    logger.info("Updated student with registration number %s", reg_number)
    print("Student updated successfully.")


def delete_student(logger):
    """Delete a student's record from the system."""
    students, details = load_data()
    reg_number = input("Enter registration number to delete: ").strip().upper()

    updated_students = []
    deleted = False
    for student in students:
        if student["registration_number"].upper() == reg_number:
            deleted = True
            continue
        updated_students.append(student)

    if not deleted:
        raise StudentDataError("No student found with that registration number.")

    details.pop(reg_number, None)
    save_data(updated_students, details)
    logger.info("Deleted student with registration number %s", reg_number)
    print("Student deleted successfully.")


def main():
    """Run the full student record management menu."""
    ensure_data_files()
    logger = setup_logger()
    logger.info("Student system started at %s", datetime.now())

    while True:
        print("\n=== Student Record Management System ===")
        print("1. Add a new student")
        print("2. View all students")
        print("3. Search student by registration number")
        print("4. Update student details")
        print("5. Delete a student record")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_student(logger)
            elif choice == "2":
                view_students(logger)
            elif choice == "3":
                search_student(logger)
            elif choice == "4":
                update_student(logger)
            elif choice == "5":
                delete_student(logger)
            elif choice == "6":
                logger.info("User exited the system.")
                print("Goodbye!")
                break
            else:
                raise StudentDataError("Please choose a valid menu option.")
        except StudentDataError as exc:
            logger.error("User input error: %s", exc)
            print(f"Error: {exc}")
        except (FileNotFoundError, PermissionError, OSError) as exc:
            logger.exception("File system error: %s", exc)
            print(f"File error: {exc}")
        except ValueError as exc:
            logger.error("Value error: %s", exc)
            print(f"Invalid input: {exc}")
        except Exception as exc:  # pragma: no cover - broad safeguard
            logger.exception("Unexpected error: %s", exc)
            print(f"Unexpected error: {exc}")
        finally:
            print("-" * 40)


if __name__ == "__main__":
    main()
