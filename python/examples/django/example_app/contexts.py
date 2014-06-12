from tranquil.contexts import BaseContext
from tranquil.django.contexts import DjangoModelContext

from example_app.models import *


class SchoolContext(DjangoModelContext):
    model = School


class SubjectContext(DjangoModelContext):
    model = Subject


class StudentContext(DjangoModelContext):
    model = Student


class RootContext(BaseContext):

    def action_school(self):
        return SchoolContext(self)

    def action_subject(self):
        return SubjectContext(self)

    def action_student(self):
        return StudentContext(self)
