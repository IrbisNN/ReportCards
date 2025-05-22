from .models import Student, Teacher, Parent

class Role:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

def get_role_list():
    return [Role('Student'), Role('Teacher'), Role('Parent')]
    
def get_role_choices():
    return [(role.name, role.name) for role in get_role_list()]

def save_role(role, account):
    if role == 'Student':
        exist = Student.objects.filter(account=account).exists()
        if exist:
            return 'Student already exist'
        newStudent = Student()
        newStudent.account = account
        newStudent.save()
        return 'Student saved successfully'
    elif role == 'Teacher':
        exist = Teacher.objects.filter(account=account).exists()
        if exist:
            return 'Teacher already exist'
        newStudent = Teacher()
        newStudent.account = account
        newStudent.save()
        return 'Teacher saved successfully'
    elif role == 'Parent':
        exist = Parent.objects.filter(account=account).exists()
        if exist:
            return 'Parent already exist'
        newStudent = Parent()
        newStudent.account = account
        newStudent.save()
        return 'Parent saved successfully'
    return 'Invalid role'