from django.db import models
from datetime import date
from django.db.models.deletion import CASCADE

from django.db.models.enums import IntegerChoices
from django.db.models.fields import AutoField, CharField, IntegerField
# Create your models here.

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
)

DEPARTMENT = (
    ('Computer Science', 'Computer Science'),
    ('Information Technology', 'Information Technology'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Artifical Inteligence', 'Artifical Inteligence')
)

# Model for Student Data


class Teacher(models.Model):

    __tablename__ = 'Teacher'

    job_id = IntegerField(primary_key=True, unique=True)
    f_name = models.CharField(max_length=45, null=False)
    l_name = models.CharField(max_length=45, null=False)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=20, choices=GENDER)

    def __str__(self):
        return f'{self.f_name} {self.l_name}'
    

class Department(models.Model):

    __tablename__ = 'Department'

    dep_id = models.AutoField(primary_key=True)
    dep_name = models.CharField(max_length=50, choices=DEPARTMENT, null=False)
    hod = models.ForeignKey(Teacher, on_delete=CASCADE)
    desc = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.dep_name}'

    def __init__(self: models.Model, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id = self.dep_id  

class Students(models.Model):
    
    __tablename__ = 'Student'

    prn_no = models.IntegerField(primary_key=True, unique=True)
    paswrd = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    mobile = models.CharField(max_length=10) # Personal number
    f_name = models.CharField(max_length=45, null=False) # First name
    l_name = models.CharField(max_length=45, null=False) # Last name
    bday = models.DateField(null=False) # Birthday
    gender = models.CharField(max_length=20, choices=GENDER)
    depart = models.ForeignKey(Department, on_delete=CASCADE)
    comment = models.CharField(max_length=255, null=True, blank=True) # Free text
    created_at = models.DateTimeField(editable=False, auto_now_add=True, auto_now=False, null=True, blank=True) 
    updated_at = models.DateTimeField(editable=False, auto_now_add=False, auto_now=True, null=True, blank=True) 
	
    def __str__(self):
        return '{}, {} ({})'.format(self.f_name, self.l_name, self.prn_no)
	
    def __init__(self: models.Model, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = f'{self.f_name} {self.l_name}'


class Subject(models.Model):

    __tablename__ = 'Subject'

    subject_id = models.BigAutoField(primary_key=True)
    subject = models.CharField(max_length=40)
    dep_id = models.ForeignKey(Department, on_delete=CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=CASCADE)
    desc = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.subject}'

class Lecture(models.Model):

    __tablename__ = 'Lectures'

    lecture_id = models.BigAutoField(primary_key=True)
    on_date = models.DateField(auto_now=False, auto_now_add=False,)
    subject = models.ForeignKey(Subject, on_delete=CASCADE)
    desc = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.lecture_id}'

    def __init__(self: models.Model.__init__, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher= self.subject.teacher


class Attendence(models.Model):

    __tablename__ = 'Attendence'

    lecture = models.ForeignKey(Lecture, on_delete=CASCADE)
    student = models.ForeignKey(Students, on_delete=CASCADE)
    join_at = models.DateTimeField(auto_now=True)
    attendence = models.BooleanField(default=True)
    remarks = models.TextField(max_length=50)

    def __init__(self: models.Model.__init__, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject= self.lecture.subject
        self.teacher= self.lecture.subject.teacher





