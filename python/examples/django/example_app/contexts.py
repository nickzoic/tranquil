from tranquil.contexts import BaseContext
from tranquil.django.contexts import DjangoModelContext

from example_app.models import *


class SchoolContext(DjangoModelContext):
    model = School


class SubjectContext(DjangoModelContext):
    model = Subject


class CourseContext(DjangoModelContext):
    model = Course


class StudentContext(DjangoModelContext):
    model = Student


class RootContext(BaseContext):

    def action_school(self):
        return SchoolContext(self.request)

    def action_subject(self):
        return SubjectContext()

    def action_course(self):
        return CourseContext()

    def action_student(self):
        return StudentContext()
