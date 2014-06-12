from django.test import TestCase
from django.core.urlresolvers import reverse
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

    def test_schools_list(self):

       res = self._api_test(['subject', 'count'])
       print res


