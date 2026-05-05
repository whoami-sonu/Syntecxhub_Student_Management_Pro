import json
import os
import csv
from datetime import datetime

FILE = "students.json"
BACKUP_FILE = "backup.json"
PASSWORD = "admin123"


# -------------------------
# STUDENT CLASS
# -------------------------
class Student:
    def __init__(self, name, student_id, grade):
        self.name = name
        self.id = student_id
        self.grade = float(grade)

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "grade": self.grade
        }


# -------------------------
# MANAGER CLASS
# -------------------------
class StudentManager:
    def __init__(self):
        self.students = []
        self.load()

    def load(self):
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                data = json.load(f)
                self.students = [Student(**s) for s in data]

    def save(self):
        with open(FILE, "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def backup(self):
        with open(BACKUP_FILE, "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)
        print("📦 Backup created")

    def add(self):
        name = input("Name: ")
        sid = input("ID: ")
        grade = input("Grade: ")

        if any(s.id == sid for s in self.students):
            print("❌ ID exists")
            return

        self.students.append(Student(name, sid, grade))
        self.save()
        print("✅ Added")

    def list(self):
        if not self.students:
            print("No data")
            return

        print("\n📋 STUDENTS")
        for s in self.students:
            print(f"{s.name} | {s.id} | {s.grade}")

    def delete(self):
        sid = input("Enter ID: ")
        self.students = [s for s in self.students if s.id != sid]
        self.save()
        print("🗑️ Deleted")

    def update(self):
        sid = input("Enter ID: ")
        for s in self.students:
            if s.id == sid:
                s.name = input("New name: ")
                s.grade = float(input("New grade: "))
                self.save()
                print("🔄 Updated")
                return
        print("Not found")

    def search(self):
        key = input("Search: ").lower()
        for s in self.students:
            if key in s.name.lower() or key in s.id:
                print(f"🔍 {s.name} | {s.id} | {s.grade}")

    def sort_by_name(self):
        self.students.sort(key=lambda x: x.name)
        print("Sorted by name")

    def sort_by_grade(self):
        self.students.sort(key=lambda x: x.grade, reverse=True)
        print("Sorted by grade")

    def stats(self):
        if not self.students:
            return

        grades = [s.grade for s in self.students]
        avg = sum(grades) / len(grades)
        topper = max(self.students, key=lambda x: x.grade)

        print("\n📊 STATS")
        print("Total:", len(self.students))
        print("Average:", round(avg, 2))
        print("Topper:", topper.name, topper.grade)

    def export_csv(self):
        with open("students.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "ID", "Grade"])
            for s in self.students:
                writer.writerow([s.name, s.id, s.grade])
        print("📁 Exported to CSV")


# -------------------------
# LOGIN SYSTEM
# -------------------------
def login():
    pwd = input("🔐 Enter admin password: ")
    return pwd == PASSWORD


# -------------------------
# MAIN MENU
# -------------------------
def main():
    if not login():
        print("❌ Wrong password")
        return

    manager = StudentManager()

    while True:
        print("\n🔥 STUDENT SYSTEM PRO")
        print("1 Add")
        print("2 List")
        print("3 Update")
        print("4 Delete")
        print("5 Search")
        print("6 Sort by Name")
        print("7 Sort by Grade")
        print("8 Stats")
        print("9 Backup")
        print("10 Export CSV")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1":
            manager.add()
        elif choice == "2":
            manager.list()
        elif choice == "3":
            manager.update()
        elif choice == "4":
            manager.delete()
        elif choice == "5":
            manager.search()
        elif choice == "6":
            manager.sort_by_name()
        elif choice == "7":
            manager.sort_by_grade()
        elif choice == "8":
            manager.stats()
        elif choice == "9":
            manager.backup()
        elif choice == "10":
            manager.export_csv()
        elif choice == "0":
            break
        else:
            print("Invalid")


if __name__ == "__main__":
    main()
