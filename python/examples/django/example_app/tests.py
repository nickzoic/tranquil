from django.test import TestCase
from django.core.urlresolvers import reverse
from tranquil.django.contexts import DjangoModelContext
import example_app.views
import json


api_view_url = reverse(example_app.views.api_view)

class SomeTests(TestCase):

    def _api_test(self, req):
        response = self.client.post(
            api_view_url,
            json.dumps(req),
            'application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        return json.loads(response.content)

    def test_subject_count(self):

       res = self._api_test(['subject', 'count'])
       self.assertEqual(res, 4)

    def test_subject_filter_count(self):
       res = self._api_test(['subject', [ 'filter', { 'school__id': 1 } ], 'count'])
       self.assertEqual(res, 2)

    def test_action_group(self):
        res = self._api_test(
            { 'subject_count': [ 'subject', 'count' ],
              'student_count': [ 'student', 'count' ]
            }
        )
        self.assertEqual(res, { 'subject_count': 4, 'student_count': 1 })

    def test_students(self):
        res = self._api_test(['student'])
        self.assertEqual(res[0]['name'], 'Nick')

    def test_meta(self):
        res = self._api_test(['student', 'meta'])
        self.assertEqual(res['desc'], example_app.views.StudentContext.__doc__)
        self.assertEqual(res['actions']['meta']['desc'], DjangoModelContext.action_meta.__doc__)
