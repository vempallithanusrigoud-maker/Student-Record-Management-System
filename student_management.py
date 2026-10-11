import json
from pathlib import Path

FILE = Path("students.json")


def load_students():
    if FILE.exists():
        try:
            return json.loads(FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read student data.")
    return []


def save_students(students):
    FILE.write_text(
        json.dumps(students, indent=4),
        encoding="utf-8"
    )


def find_student(students, student_id):
    for student in students:
        if student["id"].lower() == student_id.lower():
            return student
    return None


def add_student(students):
    student_id = input("Enter student ID: ").strip()

    if not student_id:
        print("ID cannot be empty.")
        return

    if find_student(students, student_id):
        print("This ID already exists.")
        return

    name = input("Enter student name: ").strip()
    email = input("Enter email: ").strip()

    try:
        gpa = float(input("Enter GPA (0-10): "))
        if not 0 <= gpa <= 10:
            print("GPA must be between 0 and 10.")
            return
    except ValueError:
        print("Please enter a valid GPA.")
        return

    if not name or "@" not in email or "." not in email:
        print("Enter a valid name and email.")
        return

    students.append({
        "id": student_id,
        "name": name,
        "email": email,
        "gpa": gpa
    })

    save_students(students)
    print("Student added successfully!")


def view_students(students):
    if not students:
        print("No student records found.")
        return

    for student in students:
        print("-" * 30)
        print("ID:", student["id"])
        print("Name:", student["name"])
        print("Email:", student["email"])
        print("GPA:", student["gpa"])


def search_student(students):
    query = input("Enter ID or name to search: ").strip().lower()

    matches = [
        student for student in students
        if query in student["id"].lower()
        or query in student["name"].lower()
    ]

    if matches:
        view_students(matches)
    else:
        print("No matching student found.")


def update_student(students):
    student_id = input("Enter student ID to update: ").strip()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    name = input("New name (press Enter to keep current): ").strip()
    email = input("New email (press Enter to keep current): ").strip()
    gpa_text = input("New GPA (press Enter to keep current): ").strip()

    if name:
        student["name"] = name

    if email:
        if "@" not in email or "." not in email:
            print("Invalid email. Email was not changed.")
        else:
            student["email"] = email

    if gpa_text:
        try:
            gpa = float(gpa_text)
            if 0 <= gpa <= 10:
                student["gpa"] = gpa
            else:
                print("GPA must be between 0 and 10.")
        except ValueError:
            print("Invalid GPA. GPA was not changed.")

    save_students(students)
    print("Update completed.")


def delete_student(students):
    student_id = input("Enter student ID to delete: ").strip()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    students.remove(student)
    save_students(students)
    print("Student deleted successfully!")


def main():
    students = load_students()

    while True:
        print("\n=== STUDENT RECORD MANAGEMENT ===")
        print("1. Add student")
        print("2. View students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("Thank you!")
            break
        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()