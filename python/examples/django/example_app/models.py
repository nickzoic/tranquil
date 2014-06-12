from django.db import models


class School(models.Model):
    name = models.CharField(max_length=256)


class Subject(models.Model):
    school = models.ForeignKey(School)
    name = models.CharField(max_length=256)


class Course(models.Model):
    name = models.CharField(max_length=256)
    subjects = models.ManyToManyField(Subject, related_name='courses')


class Student(models.Model):
    name = models.CharField(max_length=256)
    courses = models.ManyToManyField(Course, related_name='students')


class Enrol(models.Model):
    subject = models.ForeignKey(Subject)
    student = models.ForeignKey(Student)
    year = models.IntegerField()

