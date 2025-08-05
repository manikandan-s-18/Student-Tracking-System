import json

students = {}

def import_data_from_json(filename):
    global students
    with open(filename, 'r') as file:
        students = json.load(file)


def export_data_to_json(filename):
    with open(filename, 'w') as file:
        json.dump(students, file, indent=4)


def register_students(student_id, name, batch):
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
    if str(student_id) in students:
        students[str(student_id)]['attendance']['present_days'] += present_days
        students[str(student_id)]['attendance']['total_days'] += total_days
        print("recorded... "+str(student_id))


def calculate_attendance_percentage(student_id):
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
    if str(student_id) in students:
        students[str(student_id)]['terms'][term_name] = subject_marks_dict
        print("added")
    else:
        print("Student not found.")

    
def update_subject_mark(student_id, term, subject, new_mark):
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
    if str(student_id) in students:
        terms = students[str(student_id)]['terms']
        for term, subjects in terms.items():
            total_marks = sum(subjects.values())
            average = total_marks / len(subjects) 
            print(f"{term} Average: {average: .2f}")
    else:
        print("student not found")


def get_topper_by_term(term):
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


if __name__ == "__main__":
    import_data_from_json('data.json')
    n=(input("Enter Student Register No:"))
    generate_student_report(n)
    export_data_to_json('data.json')

