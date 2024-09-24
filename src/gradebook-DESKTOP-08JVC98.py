import json
import os

class GradeBook:
    """
    Gradbook class to represent a grade book for managing student grades.
        filename (str): The name of the JSON file to save/load data.
        students (dict): A dictionary to store student data.
    """

    def __init__(self, filename='gradebook.json'):
        """
        Initialize the GradeBook with a filename and load existing data.

        Args:
            filename (str): The name of the JSON file to save/load data.
        """
        self.filename = filename
        self.students = self.load_data()

    def load_data(self):
        """
        Load student data from the JSON file.

        Returns:
            dict: The data loaded from the JSON file, or an empty dictionary if the file does not exist.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        """
        Save student data to the JSON file.
        """
        with open(self.filename, 'w') as f:
            json.dump(self.students, f, indent=4)

    def export_data(self, export_path):
        """
        Export student data to a specified file.

        Args:
            export_path (str): The path to the export file.
        """
        with open(export_path, 'w') as f:
            json.dump(self.students, f, indent=4)

    def add_student(self, student_info):
        """
        Add a new student to the grade book.

        Args:
            student_info (dict): A dictionary containing student information with keys 'ID', 'Name', 'Class', 'Grades'.

        Returns:
            bool: True if the student was added, False if the student already exists.
        """
        student_id = student_info['ID']
        if student_id in self.students:
            return False
        else:
            self.students[student_id] = student_info
            self.students[student_id]['Grades'] = []
            self.save_data()
            return True

    def delete_student(self, student_id):
        """
        Delete a student from the grade book.

        Args:
            student_id (str): The ID of the student to delete.

        Returns:
            bool: True if the student was deleted, False if the student does not exist.
        """
        if student_id in self.students:
            del self.students[student_id]
            self.save_data()
            return True
        else:
            return False

    def add_grade(self, student_id, grade):
        """
        Add a grade for a student.

        Args:
            student_id (str): The ID of the student.
            grade (float): The grade to add.

        Returns:
            bool: True if the grade was added, False if the student does not exist.
        """
        if student_id in self.students:
            self.students[student_id]['Grades'].append(grade)
            self.save_data()
            return True
        else:
            return False

    def delete_grade(self, student_id, grade):
        """
        Delete a grade for a student.

        Args:
            student_id (str): The ID of the student.
            grade (float): The grade to delete.

        Returns:
            bool: True if the grade was deleted, False if the grade does not exist or the student does not exist.
        """
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
        """
        Calculate the final grade for a student.

        Args:
            student_id (str): The ID of the student.

        Returns:
            float: The final grade, or None if the student does not exist or has no grades.
        """
        if student_id in self.students:
            grades = self.students[student_id]['Grades']
            if grades:
                return sum(grades) / len(grades)
            else:
                return None
        else:
            return None

    def get_grades(self, student_id):
        """
        Get the grades for a student.

        Args:
            student_id (str): The ID of the student.

        Returns:
            list: The grades of the student, or None if the student does not exist.
        """
        if student_id in self.students:
            return self.students[student_id]['Grades']
        else:
            return None

    def print_all_students(self):
        """
        Print all students in the grade book.

        Returns:
            dict: A dictionary of all students.
        """
        return self.students

    def authenticate(self, username, password):
        """
        Authenticate a user.

        Args:
            username (str): The username.
            password (str): The password.

        Returns:
            bool: True if the username and password are correct false if not
        """
        if username == 'admin' and password == 'password':
            return True
        return False
