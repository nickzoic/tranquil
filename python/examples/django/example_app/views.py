from tranquil.contexts import BaseContext
from tranquil.django.contexts import DjangoModelContext
from tranquil.django import context_class_to_view

from example_app.models import *


class SchoolContext(DjangoModelContext):
    model = School


class SubjectContext(DjangoModelContext):
    model = Subject


class CourseContext(DjangoModelContext):
    model = Course


class StudentContext(DjangoModelContext):
    model = Student


# XXX this is a stupidly manual way to do it
# but it'll do for now

class RootContext(BaseContext):

    def action_school(self):
        return SchoolContext(self.request)

    def action_subject(self):
        return SubjectContext(self.request)

    def action_course(self):
        return CourseContext(self.request)

    def action_student(self):
        return StudentContext(self.request)


api_view = context_class_to_view(RootContext)
