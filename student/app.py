import json
import os


class Student:
    """Represents an individual student record."""

    def __init__(self, student_id: str, name: str, grade: str):
        self.id = student_id.strip()
        self.name = name.strip()
        self.grade = grade.strip().upper()

    def to_dict(self) -> dict:
        """Converts student object to a dictionary for JSON serialization."""
        return {"id": self.id, "name": self.name, "grade": self.grade}

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Student instance from a dictionary."""
        return cls(data["id"], data["name"], data["grade"])


class StudentManager:
    """Handles CRUD operations and data persistence for students."""

    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = {}  # Dictionary to store student_id: Student object
        self.load_data()

    def load_data(self):
        """Loads student data from the JSON file."""
        if not os.path.exists(self.filename):
            self.students = {}
            return

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                # Reconstruct Student objects from raw dictionary data
                self.students = {
                    sid: Student.from_dict(sdata) for sid, sdata in data.items()
                }
        except (json.JSONDecodeError, KeyError):
            print(
                "⚠️ Error reading data file. Starting with an empty database."
            )
            self.students = {}

    def save_data(self):
        """Saves current student data back to the JSON file."""
        try:
            with open(self.filename, "w") as file:
                # Convert all Student objects back to dictionaries for JSON saving
                serialized_data = {
                    sid: student.to_dict()
                    for sid, student in self.students.items()
                }
                json.dump(serialized_data, file, indent=4)
        except IOError as e:
            print(f"⚠️ Failed to save data to file: {e}")

    def add_student(self, student_id: str, name: str, grade: str) -> bool:
        """Validates and adds a new student."""
        if not student_id or not name or not grade:
            print("❌ Error: Fields cannot be empty.")
            return False

        if student_id in self.students:
            print(f"❌ Error: A student with ID '{student_id}' already exists.")
            return False

        # Create new instance and add to memory map
        new_student = Student(student_id, name, grade)
        self.students[new_student.id] = new_student
        self.save_data()
        print(f"✅ Student '{name}' added successfully.")
        return True

    def update_student(self, student_id: str, name: str, grade: str) -> bool:
        """Updates an existing student's name and/or grade."""
        if student_id not in self.students:
            print(f"❌ Error: Student ID '{student_id}' not found.")
            return False

        student = self.students[student_id]
        if name.strip():
            student.name = name.strip()
        if grade.strip():
            student.grade = grade.strip().upper()

        self.save_data()
        print(f"✅ Student ID '{student_id}' updated successfully.")
        return True

    def delete_student(self, student_id: str) -> bool:
        """Deletes a student record by ID."""
        if student_id not in self.students:
            print(f"❌ Error: Student ID '{student_id}' not found.")
            return False

        del self.students[student_id]
        self.save_data()
        print(f"🗑️ Student ID '{student_id}' deleted successfully.")
        return True

    def display_all_students(self):
        """Prints all students in a nicely formatted console table."""
        if not self.students:
            print("\n--- No student records found ---")
            return

        print("\n" + "=" * 50)
        print(f"{'ID':<12} | {'Name':<22} | {'Grade':<10}")
        print("-" * 50)
        for student in self.students.values():
            print(f"{student.id:<12} | {student.name:<22} | {student.grade:<10}")
        print("=" * 50 + f"\nTotal Students: {len(self.students)}\n")


def main():
    manager = StudentManager()

    while True:
        print("\n=== Student Management System ===")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List All Students")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            print("\n--- Add New Student ---")
            student_id = input("Enter Student ID: ").strip()
            name = input("Enter Student Name: ").strip()
            grade = input("Enter Student Grade: ").strip()
            manager.add_student(student_id, name, grade)

        elif choice == "2":
            print("\n--- Update Existing Student ---")
            student_id = input("Enter Student ID to update: ").strip()
            if student_id in manager.students:
                print("(Leave blank to keep current value)")
                name = input("Enter New Name: ").strip()
                grade = input("Enter New Grade: ").strip()
                manager.update_student(student_id, name, grade)
            else:
                print(f"❌ Error: Student ID '{student_id}' does not exist.")

        elif choice == "3":
            print("\n--- Delete Student Record ---")
            student_id = input("Enter Student ID to delete: ").strip()
            # Confirmation step before destructive action
            confirm = (
                input(
                    f"Are you sure you want to delete {student_id}? (y/N): "
                )
                .strip()
                .lower()
            )
            if confirm == "y":
                manager.delete_student(student_id)
            else:
                print("Deletion cancelled.")

        elif choice == "4":
            manager.display_all_students()

        elif choice == "5":
            print("\nThank you for using the Student Management System. Goodbye!")
            break

        else:
            print("❌ Invalid selection. Please choose a number between 1 and 5.")


if __name__ == "__main__":
    main()