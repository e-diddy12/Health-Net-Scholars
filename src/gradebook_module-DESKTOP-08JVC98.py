import traceback
import os
import json
import PySimpleGUI as sg
from gradebook import GradeBook

# File path for the JSON data
json_file_path = r'C:\Users\erika\OneDrive\Documents\projects\Grade_Book\src\gradebook.json'

def load_json(json_file_path):
    """
    Load JSON data from a file.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        dict: The data loaded from the JSON file, or an empty dictionary if the file does not exist.
    """
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    return {}

def login():
    """
    Display a login window for user authentication.

    If the login is successful, the main application window is opened.
    """
    sg.theme('DarkBlue13')  # Set the same theme as the main application
    layout = [
        [sg.Text('Username:', size=(10, 1)), sg.InputText(key='username')],
        [sg.Text('Password:', size=(10, 1)), sg.InputText(key='password', password_char='*')],
        [sg.Button('Login', size=(10, 1)), sg.Button('Cancel', size=(10, 1))]
    ]

    window = sg.Window('Login', layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            break
        if event == 'Login':
            username = values['username']
            password = values['password']
            gradebook = GradeBook(json_file_path)
            if gradebook.authenticate(username, password):
                window.close()
                main_app()
            else:
                sg.popup('Login Failed', 'Invalid username or password')

    window.close()

def main_app():
    """
    Display the main application window for managing student and grade data.
    """
    gradebook = GradeBook(json_file_path)
    gradebook.students = load_json(json_file_path)

    sg.theme('Dark')

    layout = [
        [sg.Text('Health Net Scholars', size=(25, 1), justification='center', font=("Arial", 36, "bold"), text_color="white")],
        [sg.TabGroup([
            [sg.Tab('Student Management', [
                [sg.Frame('Add/Delete Student', [
                    [sg.Text('Student ID', size=(15, 1)), sg.InputText(key='student_id')],
                    [sg.Text('Student Name', size=(15, 1)), sg.InputText(key='student_name')],
                    [sg.Text('Class', size=(15, 1)), sg.InputText(key='class')],
                    [sg.Button('Add Student', size=(10, 1))],
                    [sg.Button('Delete Student', size=(10, 1))]
                ], title_color='blue', relief=sg.RELIEF_GROOVE, element_justification='center', expand_x=True)]
            ]),
            sg.Tab('Grade Management', [
                [sg.Frame('Add/Delete Grade', [
                    [sg.Text('Student ID', size=(15, 1)), sg.InputText(key='grade_student_id')],
                    [sg.Text('Grade', size=(15, 1)), sg.InputText(key='grade')],
                    [sg.Button('Add Grade', size=(15, 1))],
                    [sg.Button('Delete Grade', size=(15, 1))]
                ], title_color='blue', relief=sg.RELIEF_GROOVE, element_justification='center', expand_x=True)]
            ]),
            sg.Tab('Grade Calculations', [
                [sg.Frame('Get/Calculate Grades', [
                    [sg.Text('Student ID', size=(15, 1)), sg.InputText(key='get_grades_student_id')],
                    [sg.Button('Get Grades', size=(15, 1))],
                    [sg.Button('Calculate Final Grade', size=(15, 1))]
                ], title_color='blue', relief=sg.RELIEF_GROOVE, element_justification='center', expand_x=True)]
            ]),
            sg.Tab('Other Operations', [
                [sg.Button('Print All Students', size=(30, 1), expand_x=True)],
                [sg.Button('Search Student', size=(30, 1), expand_x=True)],
                [sg.Button('Export Data', size=(30, 1), expand_x=True)],
                [sg.Button('Help', size=(30, 1), expand_x=True)]
            ])
        ]])],
        [sg.Multiline(size=(80, 20), key='output', font=('arial', 12), disabled=True, expand_x=True, expand_y=True)],
        [sg.Button('Exit', size=(25, 2), expand_x=True)]  # Increase the size of the Exit button
    ]

    window = sg.Window('Health Net Scholars Application', layout, element_justification='center', finalize=True, resizable=True, size=(800, 600))
    window.Maximize()

    while True:
        try:
            event, values = window.read()

            if event in (sg.WINDOW_CLOSED, 'Exit'):
                gradebook.save_data()
                break

            if event == 'Add Student':
                student_id = values['student_id']
                student_name = values['student_name']
                class_name = values['class']
                if student_id and student_name and class_name:
                    student_info = {
                        'ID': student_id,
                        'Name': student_name,
                        'Class': class_name
                    }
                    print(f"Adding student: {student_info}")
                    if gradebook.add_student(student_info):
                        window['output'].print(f"Student {student_name} (ID: {student_id}) added.")
                    else:
                        window['output'].print(f"Student with ID {student_id} already exists.")
                else:
                    window['output'].print("Please provide all student information.")

            if event == 'Delete Student':
                student_id = values['student_id']
                if student_id:
                    print(f"Deleting student ID: {student_id}")
                    if gradebook.delete_student(student_id):
                        window['output'].print(f"Student with ID {student_id} deleted.")
                    else:
                        window['output'].print(f"Student with ID {student_id} does not exist.")
                else:
                    window['output'].print("Please provide the student ID.")

            if event == 'Add Grade':
                student_id = values['grade_student_id']
                try:
                    grade = float(values['grade'])
                    print(f"Adding grade: {grade} for student ID: {student_id}")
                    if gradebook.add_grade(student_id, grade):
                        window['output'].print(f"Grade {grade} added for student ID {student_id}.")
                    else:
                        window['output'].print(f"Student with ID {student_id} does not exist.")
                except ValueError:
                    window['output'].print("Invalid grade. Please enter a numeric value.")

            if event == 'Delete Grade':
                student_id = values['grade_student_id']
                try:
                    grade = float(values['grade'])
                    print(f"Deleting grade: {grade} for student ID: {student_id}")
                    if gradebook.delete_grade(student_id, grade):
                        window['output'].print(f"Grade {grade} deleted for student ID {student_id}.")
                    else:
                        window['output'].print(f"Grade {grade} not found for student ID {student_id}.")
                except ValueError:
                    window['output'].print("Invalid grade. Please enter a numeric value.")

            if event == 'Get Grades':
                student_id = values['get_grades_student_id']
                grades = gradebook.get_grades(student_id)
                print(f"Getting grades for student ID: {student_id}")
                if grades is not None:
                    window['output'].print(f"Grades for student ID {student_id}: {grades}")
                else:
                    window['output'].print(f"Student with ID {student_id} does not exist.")

            if event == 'Calculate Final Grade':
                student_id = values['get_grades_student_id']
                final_grade = gradebook.calculate_final_grade(student_id)
                print(f"Calculating final grade for student ID: {student_id}")
                if final_grade is not None:
                    window['output'].print(f"Final grade for student ID {student_id}: {final_grade:.2f}")
                else:
                    window['output'].print(f"Student with ID {student_id} does not exist or has no grades.")

            if event == 'Print All Students':
                students = gradebook.print_all_students()
                print("Printing all students")
                if students:
                    for student_id, info in students.items():
                        window['output'].print(f"Student ID: {student_id}, Name: {info['Name']}, Class: {info['Class']}, Grades: {info['Grades']}")
                else:
                    window['output'].print("No students in the grade book.")

            if event == 'Search Student':
                search_id = sg.popup_get_text('Enter Student ID to search', 'Search Student')
                if search_id:
                    student = gradebook.students.get(search_id)
                    print(f"Searching for student ID: {search_id}")
                    if student:
                        window['output'].print(f"Found student: ID: {student['ID']}, Name: {student['Name']}, Class: {student['Class']}, Grades: {student['Grades']}")
                    else:
                        window['output'].print(f"No student found with ID: {search_id}")

            if event == 'Export Data':
                export_path = sg.popup_get_file('Save Data As', save_as=True, no_window=True)
                if export_path:
                    gradebook.export_data(export_path)
                    window['output'].print(f"Data exported to {export_path}")

            if event == 'Help':
                sg.popup('Help', 'This is the Health Net Scholars application.\n\nUse the tabs to manage students and grades.\nClick "Export Data" to save the current data to a file.\nContact support for more help at Eferr6@uis.edu.')

        except Exception as e:
            error_message = traceback.format_exc()
            window['output'].print(f"An error occurred: {str(e)}\n{error_message}")
            print(f"An error occurred: {str(e)}\n{error_message}")

    window.close()

if __name__ == '__main__':
    login()
