from django.urls import path
from . import views

urlpatterns = [
    # =====================
    # HOME
    # =====================
    path("", views.home, name="home"),

    # =====================
    # AUTHENTIFICATION
    # =====================
    path("login/etudiant/", views.login_student, name="login_student"),
    path("login/professeur/", views.login_teacher, name="login_teacher"),
    path("logout/", views.logout_view, name="logout"),

    # =====================
    # DASHBOARDS
    # =====================
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),

    # =====================
    # ÉTUDIANT
    # =====================
    path("student/cours/", views.courses_student, name="courses_student"),
    path("student/cours/<int:course_id>/devoirs/", views.assignments_student, name="assignments_student"),
    path("student/notes/", views.grades_student, name="grades_student"),
    path("student/profil/", views.profile_student, name="profile_student"),
    path("student/profil/print/", views.student_profile_print, name="student_profile_print"),

    # =====================
    # PROFESSEUR - PROFIL
    # =====================
    path("teacher/profile/", views.profile_teacher, name="profile_teacher"),

    # =====================
    # PROFESSEUR - COURS
    # =====================
    path("teacher/courses/", views.courses_teacher, name="courses_teacher"),
    path("teacher/courses/add/", views.course_add_teacher, name="course_add_teacher"),
    path("teacher/courses/<int:course_id>/", views.course_detail_teacher, name="courses_teacher_detail"),
    path("teacher/courses/<int:course_id>/add-student/", views.add_student_to_course, name="add_student_to_course"),

    # =====================
    # PROFESSEUR - DEVOIRS / ASSIGNMENTS
    # =====================
    path("teacher/assignments/", views.assignments_teacher, name="assignments_teacher"),
    path("teacher/assignments/add/", views.assignment_add_teacher, name="assignment_add_teacher"),
    path("teacher/assignments/<int:assignment_id>/", views.assignment_detail_teacher, name="assignment_detail_teacher"),
    path("teacher/courses/<int:course_id>/create-assignment/", views.create_assignment, name="create_assignment"),

    # =====================
    # PROFESSEUR - SOUMISSIONS
    # =====================
    path("teacher/submissions/", views.submissions_teacher, name="submissions_teacher"),
    path("teacher/submissions/<int:submission_id>/", views.submission_detail_teacher, name="submissions_teacher_detail"),
]
