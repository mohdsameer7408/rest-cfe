# from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Blog
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


class BlogApiTestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='bob', email='bob@gmail.com')
        user_obj.set_password('bob12345')
        user_obj.save()

        Blog.objects.create(
            author=user_obj,
            title='my awesome title',
            description='some description'
        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_blog(self):
        blog_count = Blog.objects.count()
        self.assertEqual(blog_count, 1)

    def test_get_list(self):
        data = {}
        url = reverse('blog-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {
            'title': 'my awesome title',
            'description': 'some description'
        }
        url = reverse('blog-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        blog = Blog.objects.first()
        data = {}
        url = blog.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        blog = Blog.objects.first()
        data = {
            'title': 'my awesome title',
            'description': 'some description'
        }
        url = blog.get_api_url()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        blog = Blog.objects.first()
        data = {
            'title': 'my awesome title 2',
            'description': 'some description 2'
        }
        url = blog.get_api_url()
        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item_with_user(self):
        data = {
            'title': 'my awesome title',
            'description': 'some description'
        }
        url = reverse('blog-list')
        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        user = User.objects.create(username='elka', email='elka@gmail.com')
        blog = Blog.objects.create(
            author=user,
            title='my awesome title',
            description='some description'
        )
        url = blog.get_api_url()

        data = {
            'title': 'my awesome title (updated)',
            'description': 'some description'
        }

        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username': 'bob',
            'password': 'bob12345'
        }
        url = reverse('api-login')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data.get('token')
        if token is not None:
            blog = Blog.objects.first()
            url = blog.get_api_url()
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

            data = {
                'title': 'my awesome title (updated)',
                'description': 'some description'
            }

            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
