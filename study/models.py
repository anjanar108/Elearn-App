from django.db import models

# Create your models here.
class Student(models.Model):
    fullname=models.CharField(max_length=150)
    username=models.CharField(max_length=150, unique=True)
    password=models.CharField(max_length=50, unique=True)
    gender=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phoneno=models.CharField(max_length=50,unique=True)
    course=models.ForeignKey('Course',on_delete=models.CASCADE,null=True, blank=True)


class Staff(models.Model):
    fullname=models.CharField(max_length=150)
    username=models.CharField(max_length=150, unique=True)
    password=models.CharField(max_length=50, unique=True)
    gender=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    course=models.ForeignKey('Course',on_delete=models.CASCADE,null=True, blank=True)
    

class Course(models.Model):
    name=models.CharField(max_length=150)
    description=models.CharField(max_length=150)
    amount=models.FloatField(max_length=150)

    def __str__(self):
        return self.name

class Event(models.Model):
    name=models.CharField(max_length=150)
    description=models.TextField(max_length=200)
    date=models.DateField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True) 

    def __str__(self):
        return self.name


class Message(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Messages are course-specific
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    

class Question(models.Model):
    text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Associate with course
    is_published = models.BooleanField(default=False)  # Publish flag


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.IntegerField()










