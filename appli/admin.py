from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Course, Assignment, Submission, Enrollment

# =========================
# Formulaires pour User
# =========================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "is_student", "is_teacher")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "is_student", "is_teacher", "password")


# =========================
# User Admin
# =========================
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("username", "email", "is_student", "is_teacher", "is_staff", "is_superuser")
    list_filter = ("is_student", "is_teacher", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_student", "is_teacher", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_student", "is_teacher"),
        }),
    )
    search_fields = ("username", "email")
    ordering = ("username",)


# =========================
# Inline pour les inscriptions
# =========================
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    readonly_fields = ("date_inscription",)


# =========================
# Course Admin
# =========================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("titre", "teacher", "date_creation")
    search_fields = ("titre", "teacher__username")
    inlines = [EnrollmentInline]  # Affiche les étudiants inscrits


# =========================
# Assignment Admin
# =========================
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("titre", "course", "date_creation", "date_limite")
    search_fields = ("titre", "course__titre")


# =========================
# Submission Admin
# =========================
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "note", "date_soumission")
    search_fields = ("assignment__titre", "student__username")


# =========================
# Enregistrer User Admin
# =========================
admin.site.register(User, UserAdmin)
