from django.shortcuts import render

from tranquil.contexts import BaseContext
from tranquil.request import process_request
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


# Can also use the contexts to enforce business rules on the
# views.

def index_view(request, school_id=None):

    actions={
        "schools": ["school"],
        "courses": ["course"],
    }
    if school_id: actions['subjects'] = [ "subject", [ "filter", { "school__id": school_id } ] ]
    if request.user.is_authenticated(): actions["profile"] = [ "profile" ]

    template_data = process_request(actions, RootContext(request))
    return render(request, 'index.html', template_data)
