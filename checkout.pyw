import json
import os
from JSONFile import JSONFile
from pprint import pprint
from easygui import *

# with open("students.json", "r+") as student_file:
#     with open("checkout.json", "r+") as checkout_file:
student_file = JSONFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json"))
checkout_file = JSONFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkout.json"))
students = student_file.read_file()
checkouts = checkout_file.read_file()
# def load_data():
#     global students, checkouts
#     students = json.load(student_file)
#     checkouts = json.load(checkout_file)
# load_data()
pprint(students)
pprint(checkouts)
while True:
    c = choicebox("Pick a choice.", "Camera Checkout", ["Checkout", "Check in", "Add student", "Import students", "See what's checked out", "Remove student"])
    print(c)
    if (c == "Checkout"):
        camera = enterbox("Scan the camera.")
        student = enterbox("Scan the student's ID.")
        try:
            this_shouldnt_work = checkouts[camera]
            msgbox("That camera has already been checked out to %s." % this_shouldnt_work)
            continue
        except KeyError:
            # this is good
            checkouts[camera] = student
            checkout_file.write_to_file(checkouts)
        student_name = "Unknown student"
        for s in students:
            if s["id"] == student:
                student_name = s["name"]
                break
        msgbox("%s checked out to %s" % (camera, student_name))
    elif (c == "Check in"):
        camera = enterbox("Scan the camera.")                
        student_name = "Unknown student"
        for s in students:
            if s["id"] == checkouts[camera]:
                student_name = s["name"]
                break
        try:
            del checkouts[camera]
        except KeyError:
            msgbox("That camera hasn't been checked out yet.")
            continue
        
        checkout_file.write_to_file(checkouts)
        msgbox("%s has been checked in from %s." % (camera, student_name))
    elif (c == "Add student"):
        name = enterbox("Student's name")
        email = enterbox("Student's email")
        id = enterbox("Scan student's id.")
        for s in students:
            if s["id"] == id:
                msgbox("That student already exists.")
                break
        else:
            students.append({"name": name, "id": id, "email": email})
            student_file.write_to_file(students)
            msgbox("%s added." % name)
    elif (c == "Import students"):
        pass
    elif (c == "See what's checked out"):
        checks = []
        name = "Unknown student"
        email = "Unkown email"
        for c, s in checkouts.items():
            for st in students:
                if st["id"] == s:
                    name = st["name"]
                    email = st["email"]
                    break
            checks.append("%s\t%s\t%s" % (c, name, email))
        if len(checks) == 0:
            checks.append("There are no cameras checked out.")
        msgbox("\n".join(checks), "Checkouts")
    elif (c == "Remove student"):
        if len(students) == 0:
            msgbox("There are no students to delete.")
            continue
        id = enterbox("Scan student's id.")
        for i in range(len(students)):
            s = students[i]
            if s["id"] == id:
                cam_checkedout = []
                for cam, stu in checkouts.items():
                    if stu == id:
                        msgbox("Warning: Camera %s is still checked out to %s (%s)." % (cam, s["name"], stu))
                        cam_checkedout.append(cam)
                if ynbox("Are you sure you want to delete %s?" % s["name"]):
                    for c in cam_checkedout:
                        del checkouts[cam]
                    del students[i]
                    student_file.write_to_file(students)
                else:
                    msgbox("Deletion canceled.")
        else:
            msgbox("That student doesn't exist.")
    elif (c is None):
        break
checkout_file.close_file()
student_file.close_file()
