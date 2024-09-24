from os import path
import PySimpleGUI as sg
from gradebook import GradeBook
import traceback


def main():
    gradebook = GradeBook()

    layout = [
        # [sg.Image(image_path)],  # Display the image
        [sg.Text('Health Net Scholars', size=(25, 1), justification='center', font=("Arial", 36, "bold"), text_color="blue")],
        [sg.Frame(layout=[
            [sg.Text('Student ID', size=(15, 1)), sg.InputText(key='student_id')],
            [sg.Text('Student Name', size=(15, 1)), sg.InputText(key='student_name')],
            [sg.Text('Class', size=(15, 1)), sg.InputText(key='class')],
            [sg.Button('Add Student', size=(10, 1))],
        ], title='Add Student', title_color='blue', relief=sg.RELIEF_SUNKEN, element_justification='center', expand_x=True)],
        [sg.Frame(layout=[
            [sg.Text('Student ID', size=(15, 1)), sg.InputText(key='grade_student_id')],
            [sg.Text('Grade', size=(15, 1)), sg.InputText(key='grade')],
            [sg.Button('Add Grade', size=(15, 1))],
            [sg.Button('Delete Grade', size=(15, 1))],
        ], title='Add/Delete Grade', title_color='blue', relief=sg.RELIEF_SUNKEN, element_justification='center', expand_x=True)],
        [sg.Frame(layout=[
            [sg.Text('Student ID', size=(15, 1)), sg.InputText(key='get_grades_student_id')],
            [sg.Button('Get Grades', size=(15, 1))],
            [sg.Button('Calculate Final Grade', size=(15, 1))],
        ], title='Get/Calculate Grades', title_color='blue', relief=sg.RELIEF_SUNKEN, element_justification='center', expand_x=True)],
        [sg.Button('Print All Students', size=(30, 1), expand_x=True)],
        [sg.Button('Search Student', size=(30, 1), expand_x=True)],
        [sg.Multiline(size=(80, 20), key='output', font=('arial', 12), disabled=True, expand_x=True, expand_y=True)],
        [sg.Button('Exit', size=(25, 1), expand_x=True)]
    ]

    window = sg.Window('Health Net Scholars Application', layout, element_justification='center', finalize=True, resizable=True)
    window.Maximize()

    while True:
        try:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == 'Exit':
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

        except Exception as e:
            error_message = traceback.format_exc()
            window['output'].print(f"An error occurred: {str(e)}\n{error_message}")
            print(f"An error occurred: {str(e)}\n{error_message}")

    window.close()