from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from .models import Course, Enrollment, Assignment, Submission
from django.http import JsonResponse 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Course, User, Enrollment

User = get_user_model()

# =========================
# PAGE D'ACCUEIL
# =========================
def home(request):
    return render(request, "appli/home.html")


# =========================
# AUTHENTIFICATION
# =========================
def login_teacher(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_teacher:
            login(request, user)
            return redirect("teacher_dashboard")
        return render(request, "appli/login_teacher.html", {"error": "Nom d'utilisateur ou mot de passe incorrect"})
    return render(request, "appli/login_teacher.html")


def login_student(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_student:
            login(request, user)
            return redirect("student_dashboard")
        return render(request, "appli/login_student.html", {"error": "Nom d'utilisateur ou mot de passe incorrect"})
    return render(request, "appli/login_student.html")


def signup_student(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "appli/signup_student.html", {"error": "Les mots de passe ne correspondent pas"})
        if User.objects.filter(username=username).exists():
            return render(request, "appli/signup_student.html", {"error": "Ce nom d'utilisateur existe déjà"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_student = True
        user.save()
        login(request, user)
        return redirect("student_dashboard")
    return render(request, "appli/signup_student.html")


def signup_teacher(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "appli/signup_teacher.html", {"error": "Les mots de passe ne correspondent pas"})
        if User.objects.filter(username=username).exists():
            return render(request, "appli/signup_teacher.html", {"error": "Ce nom d'utilisateur existe déjà"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_teacher = True
        user.save()
        login(request, user)
        return redirect("teacher_dashboard")
    return render(request, "appli/signup_teacher.html")


def logout_view(request):
    logout(request)
    return redirect("home")


# =========================
# DASHBOARD ÉTUDIANT
# =========================
@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect("home")
    enrollments = Enrollment.objects.filter(student=request.user)
    courses = [e.course for e in enrollments]
    assignments = Assignment.objects.filter(course__in=courses)
    upcoming_assignments = assignments.filter(date_limite__gte=now(), date_limite__lte=now() + timedelta(days=7))
    submissions = Submission.objects.filter(student=request.user)
    context = {
        "courses": courses,
        "assignments": assignments,
        "upcoming_assignments": upcoming_assignments,
        "submissions": submissions,
    }
    return render(request, "appli/student_dashboard.html", context)


# =========================
# DASHBOARD PROFESSEUR
# =========================
@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return redirect("home")
    courses = Course.objects.filter(teacher=request.user)
    assignments = Assignment.objects.filter(course__teacher=request.user).order_by('-date_creation')
    submissions = Submission.objects.filter(assignment__course__teacher=request.user).order_by('-date_soumission')[:5]
    context = {
        "courses": courses,
        "assignments": assignments,
        "submissions": submissions,
    }
    return render(request, "appli/teacher_dashboard.html", context)


# =========================
# PROFILS
# =========================
@login_required
def profile_student(request):
    if not request.user.is_student:
        return redirect("home")
    return render(request, "appli/profile_student.html")


@login_required
def student_profile_print(request):
    if not request.user.is_student:
        return redirect("home")
    enrollments = Enrollment.objects.filter(student=request.user)
    courses = [e.course for e in enrollments]
    submissions = Submission.objects.filter(student=request.user)
    return render(request, "appli/print_profile.html", {
        "student": request.user,
        "courses": courses,
        "submissions": submissions,
    })


@login_required
def profile_teacher(request):
    if not request.user.is_teacher:
        return redirect("home")
    return render(request, "appli/profile_teacher.html")


# =========================
# COURS ÉTUDIANT
# =========================
@login_required
def courses_student(request):
    if not request.user.is_student:
        return redirect("home")
    enrollments = Enrollment.objects.filter(student=request.user)
    courses = [e.course for e in enrollments]
    return render(request, "appli/courses_student.html", {"courses": courses})


@login_required
def assignments_student(request, course_id):
    if not request.user.is_student:
        return redirect("home")
    course = get_object_or_404(Course, id=course_id)
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return redirect("courses_student")
    assignments = Assignment.objects.filter(course=course)
    return render(request, "appli/assignments_student.html", {"course": course, "assignments": assignments})


@login_required
def grades_student(request):
    if not request.user.is_student:
        return redirect("home")
    submissions = Submission.objects.filter(student=request.user)
    return render(request, "appli/grades_student.html", {"submissions": submissions})


# =========================
# COURS PROFESSEUR
# =========================
@login_required
def courses_teacher(request):
    if not request.user.is_teacher:
        return redirect("home")
    courses = Course.objects.filter(teacher=request.user)
    return render(request, "appli/courses_teacher.html", {"courses": courses})




@login_required
def course_add_teacher(request):
    if request.method == "POST":
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        course = Course.objects.create(teacher=request.user, titre=titre, description=description)
        students = User.objects.filter(is_student=True)
        enrollments = Enrollment.objects.filter(course=course)
        return render(request, 'appli/course_add_teacher.html', {
            'created_course': course,
            'students': students,
            'enrollments': enrollments
        })

    # GET classique
    students = User.objects.filter(is_student=True)
    return render(request, 'appli/course_add_teacher.html', {'students': students})


@login_required
def course_detail_teacher(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollments = Enrollment.objects.filter(course=course)
    assignments = Assignment.objects.filter(course=course)
    return render(request, "appli/course_detail_teacher.html", {
        "course": course,
        "enrollments": enrollments,
        "assignments": assignments,
    })


# =========================
# DEVOIRS PROFESSEUR
# =========================
@login_required
def assignments_teacher(request):
    if not request.user.is_teacher:
        return redirect("home")
    assignments = Assignment.objects.filter(course__teacher=request.user)
    return render(request, "appli/assignments_teacher.html", {"assignments": assignments})


@login_required
def assignment_add_teacher(request):
    if not request.user.is_teacher:
        return redirect("home")
    
    courses = Course.objects.filter(teacher=request.user)
    
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        date_limite = request.POST.get('date_limite')
        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        Assignment.objects.create(course=course, titre=titre, description=description, date_limite=date_limite)
        return redirect('assignments_teacher')
    
    return render(request, 'appli/assignment_add_teacher.html', {'courses': courses})


@login_required
def assignment_detail_teacher(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, course__teacher=request.user)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, "appli/assignment_detail_teacher.html", {
        "assignment": assignment,
        "submissions": submissions,
    })


# =========================
# SOUMISSIONS PROFESSEUR
# =========================
@login_required
def submissions_teacher(request):
    if not request.user.is_teacher:
        return redirect("home")
    submissions = Submission.objects.filter(assignment__course__teacher=request.user)
    return render(request, "appli/submissions_teacher.html", {"submissions": submissions})


@login_required
def submission_detail_teacher(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, assignment__course__teacher=request.user)
    return render(request, "appli/submission_detail_teacher.html", {"submission": submission})


# =========================
# AJOUT D'ÉTUDIANT À UN COURS
# =========================
@login_required
def add_student_to_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = User.objects.filter(is_student=True)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(User, id=student_id, is_student=True)

        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        if created:
            return JsonResponse({'success': True, 'student_name': student.username})
        else:
            return JsonResponse({'success': False, 'error': 'Cet étudiant est déjà inscrit.'})

    return render(request, "appli/add_student.html", {"course": course, "students": students})
# =========================
# CRÉER UN DEVOIR RAPIDEMENT DEPUIS LE DÉTAIL D'UN COURS
# =========================
@login_required
def create_assignment(request, course_id):
    if not request.user.is_teacher:
        return redirect("home")
    
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    
    if request.method == "POST":
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        date_limite = request.POST.get('date_limite')
        Assignment.objects.create(course=course, titre=titre, description=description, date_limite=date_limite)
        return redirect('course_detail_teacher', course_id=course.id)
    
    return render(request, 'appli/create_assignment.html', {'course': course})
