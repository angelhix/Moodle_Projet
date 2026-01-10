from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# =========================
# UTILISATEUR PERSONNALISÉ
# =========================
class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# =========================
# COURS
# =========================
class Course(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        limit_choices_to={'is_teacher': True}
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


# =========================
# INSCRIPTION DES ÉTUDIANTS
# =========================
class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'is_student': True}
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        default=1  # ID du cours par défaut
    )
    date_inscription = models.DateTimeField(auto_now_add=True)


# =========================
# DEVOIRS / ASSIGNMENTS
# =========================
class Assignment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments',
        default=1  # ID du cours par défaut pour faciliter la migration
    )
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.titre} ({self.course.titre})"


# =========================
# SOUMISSIONS / NOTES
# =========================
class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
        limit_choices_to={'is_student': True}
    )
    fichier = models.FileField(
        upload_to='submissions/',
        blank=True,
        null=True
    )
    note = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.titre}"
