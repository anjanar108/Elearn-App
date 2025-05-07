from django.urls import path
from .import views

urlpatterns = [
    path("",views.home, name='home'),
    path("about/",views.about,name='about'),
    path("courses/",views.courses,name='courses'),
    path("contact/",views.contact,name='contact'),
    path("register-student/",views.register_student,name='register_student'),
    path("login-student/",views.login_student,name='login_student'),
    path("register-staff/",views.register_staff,name='register_staff'),
    path("login-staff/",views.login_staff,name='login_staff'),
    path("dashboard-student/",views.dashboard_student,name='dashboard_student'),
    path("dashboard-staff/",views.dashboard_staff,name='dashboard_staff'),

    path("logout/",views.logout_user,name='logout'),
    path("send-message/",views.send_message_to_students,name='send_message_to_students'),
    # path("view_sent_messages/",views.view_sent_messages,name='view_sent_messages'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),



    path('start_exam/', views.start_exam, name='start_exam'),
    path('publish_exam/', views.publish_exam, name='publish_exam'),
    path('attempt_exam/', views.attempt_exam, name='attempt_exam'),
    path('submit_exam/', views.submit_exam, name='submit_exam'),


] 
