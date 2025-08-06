import json

students = {}

def import_data_from_json(filename):
    global students
    with open(filename, 'r') as file:
        students = json.load(file)
        print("Data imported successfully.")


def export_data_to_json(filename):
    with open(filename, 'w') as file:
        json.dump(students, file, indent=4)
        print("Data exported successfully.")


def register_students(student_id, name, batch):
    student_id = str(student_id).upper()
    if str(student_id) not in students:
        students[str(student_id)] = {
            "name": name,
            "batch": batch,
            "attendance": {
                "present_days": 0,
                "total_days": 0
            },
            "terms":{}
        }
        print("Newly registered", student_id)
    else:
        print("Already Registered....")


def record_attendance(student_id, present_days, total_days):
    student_id = str(student_id).upper()
    if str(student_id) in students:
        students[str(student_id)]['attendance']['present_days'] += present_days
        students[str(student_id)]['attendance']['total_days'] += total_days
        print("recorded... "+str(student_id))
    else:
        print("Student not found.")

def calculate_attendance_percentage(student_id):
    student_id = str(student_id).upper()
    if str(student_id) in students:
        present_days = students[str(student_id)]['attendance']['present_days']
        total_days = students[str(student_id)]['attendance']['total_days']

        if(present_days > 0):
            percentage = (present_days / total_days)*100
            print(f"Attendance :{percentage: .2f}") 
        else:
            print("Attendance not found for this student")
    else:
        print("Student not found")


def add_term_result(student_id, term_name, subject_marks_dict):
    student_id = str(student_id).upper()
    term_name = term_name.lower()
    if str(student_id) in students:
        students[str(student_id)]['terms'][term_name] = subject_marks_dict
        print("added")
    else:
        print("Student not found.")

    
def update_subject_mark(student_id, term, subject, new_mark):
    student_id = str(student_id).upper()
    term = term.lower()
    if str(student_id) in students:
        if term in students[str(student_id)]['terms']:
            if(subject in students[str(student_id)]['terms'][term]):
                students[str(student_id)]['terms'][term][subject] = new_mark
                print("updated")
            else:
                print("subject not found")
        else:
            print("term not found")
    else:
        print("student not found")


def calculate_average(student_id):
    student_id = str(student_id).upper()
    if str(student_id) in students:
        terms =students[str(student_id)]['terms']
        total_marks = 0
        total_subjects = 0
        for term,subjects in terms.items():
            for subject, mark in subjects.items():
                total_marks += mark
                total_subjects += 1
        if total_subjects > 0:
            average = total_marks / total_subjects
            print(f"Overall Average :{average: .2f}")
        else:
            print("subjects not found ")
    else:
        print("student not found")


def terms_average(student_id):
    student_id = str(student_id).upper()
    if str(student_id) in students:
        terms = students[str(student_id)]['terms']
        for term, subjects in terms.items():
            total_marks = sum(subjects.values())
            average = total_marks / len(subjects) 
            print(f"{term} Average: {average: .2f}")
    else:
        print("student not found")


def get_topper_by_term(term):
    term = term.lower()
    if term:
        top_student = None
        top_average = 0
        for student_id, student_data in students.items():
            if term in student_data['terms']:
                term_average = sum(student_data['terms'][term].values()) / len(student_data['terms'][term])
                if term_average > top_average:
                    top_average = term_average
                    top_student = student_id
        if top_student:
            print(f"{term} Topper: {students[top_student]['name']}")
        else:
            print(f"No data found for term {term}")
    else:
        print("Term not found.")


def rank_students_by_overall_average(batch):
    ranked_students = []
    if batch not in [student['batch'] for student in students.values()]:
        print("No students found in this batch")
        return
    for student_id, student_data in students.items():
        if student_data.get("batch") == batch:
            terms = student_data.get('terms', {})
            total_marks = 0
            total_subjects = 0
            for term, subjects in terms.items():
                for subject, mark in subjects.items():
                    total_marks += mark
                    total_subjects += 1
            if total_subjects>0:
                average = total_marks / total_subjects
            else:
                average = None
            if average is not None:
                ranked_students.append((student_id, average))  
    ranked_students.sort(key=lambda x: x[1], reverse=True)

    for rank, (student_id, average) in enumerate(ranked_students, start=1):
        print(f"Rank {rank}: {students[student_id]['name']} Overall Average{average: .2f}")


def generate_student_report(student_id):
    student_id = str(student_id).upper()
    if str(student_id) not in students:
        print("Student not found.")
        return
    print(f"Student Report : {students[student_id]['name']}({student_id})")
    print(f"Batch: {students[student_id]['batch']}")
    calculate_attendance_percentage(student_id)
    terms_average(student_id)
    calculate_average(student_id)
    top_student = None
    top_term = None
    top_average = 0
    for sid, sdata in students.items():
        for term, subjects in sdata['terms'].items():
            if subjects:
                avg = sum(subjects.values()) / len(subjects)
                if avg > top_average:
                    top_average = avg
                    top_student = sid
                    top_term = term
    
    print(f"Top Performer: {students[top_student]['name']} in {top_term} with {top_average:.1f} average")



def get_student_all_details():
    for student_id, student_data in students.items():
        print(f"Student ID: {student_id}")
        print(f"Name: {student_data['name']}")
        print(f"Batch: {student_data['batch']}")
        print("Terms:")
        results = []
        for term, subjects in student_data['terms'].items():
            m = 'pass'
            for mark in subjects.values():
                if mark <= 35:
                    m = 'fail'
                    break
            results.append(m)
            print(f"  {term}:" + m)
        for result in results:
            if result == 'fail':
                print("Overall Result: Fail")
                break
        else:
            print("Overall Result: Pass")
        print("\n") 

def all_functions():
    while True:
        action = input("Enter action (register, attendance, attendance_percentage, add_term, update_mark, average, terms_average, topper, rank, report, details, import, export, exit): ").strip().lower()
        if action == 'register':
            student_id = input("Enter Student ID: ")
            name = input("Enter Name: ")
            batch = input("Enter Batch: ")
            register_students(student_id, name, batch)
        elif action == 'attendance':
            student_id = input("Enter Student ID: ")
            present_days = int(input("Enter Present Days: "))
            total_days = int(input("Enter Total Days: "))
            record_attendance(student_id, present_days, total_days)
        elif action == 'attendance_percentage':
            student_id = input("Enter Student ID: ")
            calculate_attendance_percentage(student_id)
        elif action == 'add_term':
            student_id = input("Enter Student ID: ")
            term_name = input("Enter Term Name: ")
            subject_marks_dict = json.loads(input("Enter Subject Marks as JSON: "))
            add_term_result(student_id, term_name, subject_marks_dict)
        elif action == 'update_mark':
            student_id = input("Enter Student ID: ")
            term = input("Enter Term: ")
            subject = input("Enter Subject: ")
            new_mark = int(input("Enter New Mark: "))
            update_subject_mark(student_id, term, subject, new_mark)
        elif action == 'average':
            student_id = input("Enter Student ID: ")
            calculate_average(student_id)
        elif action == 'terms_average':
            student_id = input("Enter Student ID: ")
            terms_average(student_id)
        elif action == 'topper':
            term = input("Enter Term: ")
            get_topper_by_term(term)
        elif action == 'rank':
            batch = input("Enter Batch: ")
            rank_students_by_overall_average(batch)
        elif action == 'report':
            student_id = input("Enter Student ID: ")
            generate_student_report(student_id)
        elif action == 'details':
            get_student_all_details()
        elif action == 'import':
            filename = input("Enter JSON filename to import: ")
            import_data_from_json(filename)
        elif action == 'export':
            filename = input("Enter JSON filename to export: ")
            export_data_to_json(filename)
        elif action == 'exit':
            print("Exiting...")
            break
        else:
            print("Invalid action. Please try again.")



if __name__ == "__main__":
    all_functions()

