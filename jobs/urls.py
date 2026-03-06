from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('register/', views.register),
    path('choose-role/', views.choose_role),
    path('recruiter/', views.recruiter_dashboard),
    path('jobs/', views.job_list),
    path('apply/<int:job_id>/', views.apply_job),
    path('applicants/<int:job_id>/', views.view_applicants),
    path('delete-job/<int:job_id>/', views.delete_job),
    path('application/<int:app_id>/<str:action>/', views.update_application_status),
    path('my-applications/', views.my_applications),
    path('about/', views.about_page),
    path('send-message/<int:application_id>/', views.send_message),
    path('messages/', views.messages_page),
    path('logout/', views.logout_view),
]