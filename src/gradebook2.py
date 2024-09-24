import json
import os

class GradeBook:

    def __init__(self, filename='gradebook.json'):
        self.filename = filename
        self.students = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.students, f, indent=4)

    def export_data(self, export_path):
        with open(export_path, 'w') as f:
            json.dump(self.students, f, indent=4)

    def add_student(self, student_info):
        student_id = student_info['ID']
        if student_id in self.students:
            return False
        else:
            self.students[student_id] = student_info
            self.students[student_id]['Grades'] = []
            self.save_data()
            return True

    def delete_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            self.save_data()
            return True
        else:
            return False

    def add_grade(self, student_id, grade):
        if student_id in self.students:
            self.students[student_id]['Grades'].append(grade)
            self.save_data()
            return True
        else:
            return False

    def delete_grade(self, student_id, grade):
        if student_id in self.students:
            try:
                self.students[student_id]['Grades'].remove(grade)
                self.save_data()
                return True
            except ValueError:
                return False
        else:
            return False

    def calculate_final_grade(self, student_id):
        if student_id in self.students:
            grades = self.students[student_id]['Grades']
            if grades:
                return sum(grades) / len(grades)
            else:
                return None
        else:
            return None

    def get_grades(self, student_id):
        if student_id in self.students:
            return self.students[student_id]['Grades']
        else:
            return None

    def print_all_students(self):
        return self.students

