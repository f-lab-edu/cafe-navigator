from django.test import TestCase, Client
import json
import logging
import statistics


class RegisterAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/user/signup"
    
    def test_register(self):
        # 성공
        response = self.client.post(
            self.url,
            {
                "username": "teststaff1",
                "password": "1234",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)