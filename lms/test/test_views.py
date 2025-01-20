from django.test import TestCase, Client

class CourseAPITestCase(TestCase):
    def test_get_courses(self):
        client = Client()
        response = client.get('/api/get_courses/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)