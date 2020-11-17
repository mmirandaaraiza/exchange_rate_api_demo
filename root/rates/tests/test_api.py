from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.


class RateAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234')

    def test_unauthenticated_get_returns_401(self):
        response = self.client.get('/api/rates/')
        self.assertEqual(response.status_code, 401)

    def test_authenticated_get_returns_200(self):
        jwt_response = self.client.post('/api/token/', data={'username': 'testuser', 'password': '1234'})
        token = jwt_response.json()['access']

        response = self.client.get('/api/rates/', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
