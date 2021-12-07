from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.template import RequestContext

# Create your views here.

class Links():
    def __init__(self, user):
        self.profile = '../../' + user + '/profile/'
        self.attendence = '../../' + user + '/attendence/'
        self.lectures = '../../' + user + '/new/'
        self.home = '../../' + user + '/home/'
        self.edit_profile = '../../' + user + '/profile-edit/'
        self.subjects = '../../' + user + '/subjects/'
        self.dashboard = '../../' + user + '/dashboard/'
        self.name = Students.objects.get(prn_no=user).name

class Links2():
    def __init__(self, user):
        self.profile = './' + user + '/profile'
        self.attendence = './' + user + '/attendence'
        self.lectures = './' + user + '/lectures'
        self.home = './' + user + '/home'
        self.edit_profile = './' + user + '/profile-edit/'

def home_view(request):
    return render(request, 'index.html')

def login_view(request):
    link = '../index/'
    return render(request, 'login-page.html', {'link':link})
    
def login(request):
    user = request.POST.get("user", '')
    pwd = request.POST.get("paswrd", '')
    if user and pwd:
        try:
            c0 = Students.objects.filter(prn_no=user,paswrd=pwd)
        except:
            messages.success(request, "Something wrong with your username or password")
            return render(request, 'login-page.html')   

        for student in Students.objects.all():
            if student.f_name == user:
                break
            return render(request, 'index.html', context={'link': Links2(user), 'student': student})
        else:
            messages.success(request, "Something wrong with your username or password")
            return render(request, 'login-page.html')
    else:
        messages.success(request, "Username or password missing")
        return render(request, 'login-page.html')


def register_view(request):
    return render(request, 'signup.html', context={'form': StudentForm()})

def register(request):
    
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "User Has Been Successfully Created!")
            return redirect('../login/')

    else:
        messages.success(request, "There is problem with your application")
        return redirect('../signup/')

def view_profile(request, user):
    log_user = Students.objects.get(prn_no = int(user))    
    return render(request, 'profile.html', context={'link': Links(user), 'user': log_user})

def edit_profile(request, user):

    user_obj = Students.objects.get(prn_no = user)

    if request.method == "POST":
        user_obj.paswrd = request.POST.get('password','')
        user_obj.email = request.POST.get('email','')
        user_obj.mobile = request.POST.get('mobile','')# Personal number
        user_obj.f_name = request.POST.get('f_name','')# First name
        user_obj.l_name = request.POST.get('l_name','')# Last name
        #user_obj.gender = request.POST.get('gender','')
        #user_obj.depart = request.POST.get('depart','')
        user_obj.comment = request.POST.get('comment', '')

        user_obj.save()
        messages.success(request, "Edit Student Info Successfully!")
        return redirect('../profile')
    else:    
        return render(request, 'index.html', context={'link': Links(user), 'user': user_obj})

def view_lecture(request, user):
    dep_id = Students.objects.get(prn_no=user).depart.id
    subjects = Subject.objects.filter(dep_id=dep_id)

    lectures = []

    for subject in subjects:
        add_lectures = Lecture.objects.filter(subject=subject.subject_id)
        for one in add_lectures:
            lectures.append(one)

    return render(request, 'lectures.html', context={'link': Links(user), 'lectures': lectures})

def view_attendence(request, user):
    attend = Attendence.objects.filter(student = user)
    #attend = list(attend2)
    link = Links(user)
    return render(request, 'attendence.html', context= {'attend': attend.reverse(), 'link':link})

def mark_attendence(request, user):
    lec_id = request.POST.get('id')
    attend = Attendence(lecture= Lecture.objects.get(lecture_id=lec_id) , student= Students.objects.get(prn_no=user))
    attend.save()
    return redirect('https://meet.google.com')

def view_subjects(request,user):
    subjects = Subject.objects.filter(dep_id=Students.objects.get(prn_no=user).depart)
    return render(request, 'subjects.html', context={'subjects': subjects, 'link': Links(user)})   

def dashboard(request, user):
    return HttpResponse("coming soon")

def error(request, exception):
    return render(request, "error.html")


def handler404(request, *args, **argv):
    response = render(request, 'error.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'error.html')
    response.status_code = 500
    return response