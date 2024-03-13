from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class AccountTests(APITestCase):

    def setUp(self):
        # Create a user for testing login and profile update
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.token = Token.objects.create(user=self.user)
        
        # For authenticated requests, set the authentication header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        #print(f"Created token for testuser: {self.token.key}")
        
    def test_register_user(self):
        """
        Test user registration
        """
        print("\n\n===== Test User Registration =====")
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newuser123', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        print(f"Register user response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_login(self):
        """
        Test user login with username and password
        """
        print("\n\n===== Test User Login =====")
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        print(f"Login response Token: {response.data.get('token', 'No Token Returned')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['token']

        # Access a protected view with the acquired token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # Get the URL for a protected view
        protected_view_url = reverse('order_history')
    
        # Attempt to access the protected view
        response = self.client.get(protected_view_url)
        # Verify successful access to the protected view
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("User successfully logged in and accessed a protected view with the token.")
    
    def test_logout(self):
        """
        Test user logout
        """
        print("\n\n===== Test User Logout =====")
        url = reverse('logout')
        response = self.client.post(url, format='json')
        print(f"Logout response status: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_change_password(self):
        """
        Test password change
        """
        print("\n\n===== Test Change Password =====")
        url = reverse('change_password')
        data = {'old_password': 'testpassword123', 'new_password': 'newpassword456'}
        response = self.client.post(url, data, format='json')
        print("Change password response status: 200 OK")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test logging in with the new password
        self.client.logout()
        print("Testing login with the new password...")
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'newpassword456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        """
        Test updating user profile
        """
        print("\n\n===== Test Update Profile =====")
        url = reverse('update_profile')
        data = {'username': 'updateduser', 'email': 'updateduser@example.com'}
        response = self.client.post(url, data, format='json')
        print(f"Update profile response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        print(f"Updated username: {self.user.username}, email: {self.user.email}")
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_order_history(self):
        """
        Test viewing order history
        """
        print("\n\n===== Test Viewing Order History =====")
        url = reverse('order_history')
        response = self.client.get(url, format='json')
        print(f"Order history response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
