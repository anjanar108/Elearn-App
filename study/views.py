from django.shortcuts import render, redirect,get_object_or_404
from study.models import Student,Staff, Course,Event,Message,Question,StudentAnswer
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth import logout


# Create your views here.
def home(request):
    course=Course.objects.all()
    staff=Staff.objects.all()
    event=Event.objects.all()
    return render(request, 'index.html', {'course': course, 'staff': staff,'event':event})

# hello

def about(request):
    staff=Staff.objects.all()
    return render(request,'about.html',{'staff':staff})


def courses(request):
    course=Course.objects.all()
    return render(request,'courses.html',{'course':course})


def contact(request):
    return render(request,'contact.html')

# def dashboard_student(request):
#     if 'student_id' in request.session:
#         fullname = request.session.get('fullname')
#         student_id = request.session['student_id']
#         student = Student.objects.get(id=student_id)
#         course_name = student.course.name
#         event=Event.objects.all()
#         messages = Message.objects.filter(course=student.course).order_by("-created_at")
#         if Questions.objects.exists():
#           return render(request, 'dashboard_student.html', {'exam_available': True})
#         return render(request, 'dashboard_student.html', {'exam_available': False})
        
#     return render(request, 'dashboard_student.html', {'fullname': fullname,'event':event,'course_name':course_name,'messages':messages})


def dashboard_student(request):
    if 'student_id' in request.session:
        # Retrieve student details
        student_id = request.session['student_id']
        student = Student.objects.get(id=student_id)
        fullname = student.fullname
        course_name = student.course.name

        # Fetch all events and messages for the student's course
        event = Event.objects.all()
        messages = Message.objects.filter(course=student.course).order_by("-created_at")

        # Check if there are published questions for the student's course
        exam_available = Question.objects.filter(course=student.course, is_published=True).exists()

        # Pass necessary context to the template
        context = {
            'fullname': fullname,
            'event': event,
            'course_name': course_name,
            'messages': messages,
            'exam_available': exam_available,
        }
        return render(request, 'dashboard_student.html', context)

    # Redirect to login if session is not found
    return redirect('login')


def dashboard_staff(request):
    if 'staff_id' in request.session:
        fullname = request.session.get('fullname')
        staff_id = request.session['staff_id']
        staff = Staff.objects.get(id=staff_id)
        course_name = staff.course.name
        event=Event.objects.all()
    return render(request, 'dashboard_staff.html', {'fullname': fullname,'event':event,'course_name':course_name,})


# def dashboard(request):
#     if 'student_id' in request.session :
#         username = request.session.get('username')
#         return render(request,'dashboard.html',{'username':username})
#     else:
#         return redirect('login_student')


def register_student(request):
    if request.method=='POST':
        fullname=request.POST['fullname']
        username=request.POST['username']
        password=request.POST['password']
        gender=request.POST['gender']
        email=request.POST['email']
        phoneno=request.POST['phoneno']
        course=request.POST['course']
        course = Course.objects.get(id=request.POST['course'])
        Student.objects.create(fullname=fullname,username=username,password=make_password(password),email=email,phoneno=phoneno,gender=gender,course=course)
        return redirect('login_student')
    courses = Course.objects.all()
    return render(request,'register.html', {'courses':courses})


def login_student(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        student= Student.objects.get(username=username)
        if check_password(password,student.password):
            request.session['student_id']=student.id
            request.session['fullname']=student.fullname   
        if student:
            return redirect('dashboard_student')
        else:
            messages.error(request,'invalid details')
    return render(request,'login.html') 


def register_staff(request):
    if request.method=='POST':
        fullname=request.POST['fullname']
        username=request.POST['username']
        password=request.POST['password']
        gender=request.POST['gender']
        email=request.POST['email']
        course=request.POST['course']
        course = Course.objects.get(id=request.POST['course'])
        Staff.objects.create(fullname=fullname,username=username,password=make_password(password),gender=gender,email=email,course=course)
        course = Course.objects.get(id=request.POST['course'])
        return redirect('login_staff')
    courses = Course.objects.all()
    return render(request,'register_staff.html',{'courses':courses})

def login_staff(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        staff= Staff.objects.get(username=username)
        if check_password(password,staff.password):
            request.session['staff_id']=staff.id
            request.session['fullname']=staff.fullname   
        if staff:
            return redirect('dashboard_staff')
        else:
            messages.error(request,'invalid details')
    return render(request,'login_staff.html') 

    
def logout_user(request):
    logout(request)
    return redirect('home')


# messages = Message.objects.filter(course=student.course).order_by("-created_at")    
# messages = Message.objects.filter(course=student.course).order_by("-created_at")


def send_message_to_students(request):
    if 'staff_id' not in request.session:
        return redirect('login_staff') 
    fullname = request.session.get('fullname')
    staff_id = request.session['staff_id']
    staff = Staff.objects.get(id=staff_id)
    course = staff.course  
    message=Message.objects.filter(staff=staff).order_by('-id') 
    if request.method == 'POST':
        content = request.POST['content'] 
        Message.objects.create(staff=staff, course=course, content=content)
        messages.success(request, 'Message sent')
        return redirect('send_message_to_students')  
    return render(request, 'send_message.html', {'staff': staff,'course': course,'fullname':fullname,'message':message})



def delete_message(request, message_id):
    if 'staff_id' not in request.session:
        return redirect('login_staff') 
    staff_id = request.session['staff_id']
    message = Message.objects.get(id=message_id, staff_id=staff_id)
    message.delete()
    messages.success(request, 'Message deleted')
    return redirect('send_message_to_students')

def start_exam(request):
    if request.method == 'POST':
        question1 = request.POST['question1']
        option1_1 = request.POST['option1_1']
        option1_2 = request.POST['option1_2']
        option1_3 = request.POST['option1_3']
        option1_4 = request.POST['option1_4']
        correct1 = request.POST['correct1']

        # Get the staff's course
        staff_id = request.session.get('staff_id')
        staff = Staff.objects.get(id=staff_id)
        course = staff.course

        # Save the question and link to course
        Question.objects.create(
            text=question1,
            option1=option1_1,
            option2=option1_2,
            option3=option1_3,
            option4=option1_4,
            correct_option=int(correct1),
            course=course,
            is_published=True  # Automatically publish the exam
        )


    
        messages.success(request, 'Exam published successfully!')
        return redirect('dashboard_staff')  # Redirect to staff dashboard

    return render(request, 'start_exam.html')



def publish_exam(request):
    messages.success(request, 'Exam published successfully!')
    return redirect('dashboard_staff')



def attempt_exam(request):
    # Ensure the user is logged in as a student
    if 'student_id' in request.session:
        student_id = request.session.get('student_id')
        student = get_object_or_404(Student, id=student_id)

        # Fetch questions related to the student's course and ensure they are published
        questions = Question.objects.filter(course=student.course, is_published=True)

        if request.method == 'POST':
            # Iterate through the questions and record answers
            for question in questions:
                selected_option = request.POST.get(f'question_{question.id}')
                if selected_option:  # Ensure an option is selected
                    try:
                        StudentAnswer.objects.create(
                            student=student,
                            question=question,
                            selected_option=int(selected_option)
                        )
                    except ValueError:
                        messages.error(request, f"Invalid option selected for question {question.id}")
                        return render(request, 'attempt_exam.html', {'questions': questions})

            messages.success(request, 'Exam submitted successfully!')
            return redirect('dashboard_student')

        return render(request, 'attempt_exam.html', {'questions': questions})

    # Redirect to login page if the user is not authenticated
    messages.error(request, 'You must be logged in to attempt the exam.')
    return redirect('login')


def submit_exam(request):
    if request.method == 'POST':
        for question in Question.objects.all():
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option:
                StudentAnswer.objects.create(
                    question=question,
                    selected_option=int(selected_option)
                )
        messages.success(request, 'Your answers have been submitted successfully!')
        return redirect('dashboard_student')
    return redirect('dashboard_student')








