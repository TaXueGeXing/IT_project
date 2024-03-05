from django.test import TestCase, Client
from django.urls import reverse
from Transaction.models import Order
from django.contrib.auth.models import User
from django.utils import timezone

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create sample Order objects
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Order.objects.create(BuyerID=self.user, SellerID=self.user, ProductID=None, Time=timezone.now())

    def test_view_order_history(self):
        # Log in as the user
        self.client.login(username='testuser', password='testpassword')
        # Access the view
        response = self.client.get(reverse('view_order_history'))
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Check if the orders are retrieved and displayed correctly
        self.assertQuerysetEqual(
            response.context['orders'],
            Order.objects.filter(BuyerID=self.user),
            transform=lambda x: x
        )

    def test_edit_profile(self):
        # Log in as the user
        self.client.login(username='testuser', password='testpassword')
        # Access the view with POST data
        response = self.client.post(reverse('edit_profile'), {'username': 'newusername', 'email': 'newemail@example.com'})
        # Check if the user profile is updated
        self.assertEqual(response.status_code, 302)  # Check if redirecting to account page after edit
        # Fetch the user object from the database
        updated_user = User.objects.get(username='newusername')
        # Check if the user profile is updated correctly
        self.assertEqual(updated_user.email, 'newemail@example.com')

# Add more test cases as needed
