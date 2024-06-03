from django.db import models
from apps.user.models import User
from django.core.validators import MaxValueValidator



class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Request(models.Model):
    DEGREE_CHOICES = [
        ('magistrate', 'magistrate'),
        ('doctorate', 'doctorate'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='requests', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    is_foreigner = models.BooleanField(default=False)

    diploma = models.FileField(upload_to='diplomas/', blank=True, null=True)
    passport_front = models.FileField(upload_to='passport-front/', blank=True, null=True)
    passport_back = models.FileField(upload_to='passport-back/', blank=True, null=True)
    photo = models.FileField(upload_to='abiturient-photos/', blank=True, null=True)
    type = models.CharField(max_length=255, choices=DEGREE_CHOICES, default=DEGREE_CHOICES[0][0])

    def __str__(self):
        return self.email


class CertificateImage(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='certs')
    image = models.ImageField(upload_to='certificate-images/')

    def __str__(self):
        return f"ID: {self.id} - {self.image.name[:20]}"


class Exam(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='exams', blank=True, null=True)
    abiturient = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='exams')
    exam_photo = models.FileField(upload_to='exam-photos')

    def __str__(self):
        return self.abiturient.email


class ExamGrade(models.Model):
    exam = models.ManyToManyField(Exam, verbose_name='exam_grade')
    grade = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=100)
    grader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_grades')

    def __str__(self):
        return f"{self.exam.abiturient.email} {self.grade}"