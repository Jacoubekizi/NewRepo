from .models import *

def validate_desires(data):

    list_desires = []
    student_desires = data
    desires = Dseires.objects.all()

    for student_desire in student_desires:
        for desire in desires:
            if student_desire == desire.desire:
                print(student_desire)
                list_desires.append(desire.id)

    return list_desires


def finale_average(data):
    Id_number = data['idnumber']
    username = data['username']
    final_avg = 0.0

    for student in Students_University.objects.all():
        if student.Id_Number == int(Id_number) and student.username == username:
            if not student.exam:
                final_avg = student.average
            else:
                final_avg = (float(student.exam) * 0.3) + (float(student.average) * 0.7)
            break
    return final_avg

def student(data):
    Id_number = data['idnumber']
    username = data['username']
    print(type(Id_number), type(username))
    id = 0
    for student in Students_University.objects.all():
        print(student.username == username)
        if student.Id_Number == int(Id_number) and student.username == username:
            id = student.id
            print(id)
            break
    return id