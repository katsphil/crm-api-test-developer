import io
import os

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Customer, User
from .models import User


def generate_photo_file():
    """Helper function to create an image."""
    file = io.BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file


class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_create_customer(self):
        customer = Customer.objects.create(
            name="John", surname="Doe", created_by=self.user
        )
        self.assertEqual(customer.name, "John")
        self.assertEqual(customer.surname, "Doe")
        self.assertEqual(customer.created_by, self.user)


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.assertFalse(user.is_admin)
        self.assertTrue(user.check_password("testpass123"))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(username="admin", password="adminpass123")
        admin.is_admin = True
        admin.save()
        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.is_superuser)


class CustomerAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)
        self.customer = Customer.objects.create(
            name="Jane", surname="Doe", created_by=self.user
        )

    def test_list_customers(self):
        url = reverse("customer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_customer(self):
        url = reverse("customer-list")
        data = {"name": "Alice", "surname": "Smith"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_update_customer(self):
        url = reverse("customer-detail", kwargs={"pk": self.customer.pk})
        data = {"name": "Janet", "surname": "Doe"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "Janet")

    def test_delete_customer(self):
        url = reverse("customer-detail", kwargs={"pk": self.customer.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_upload_customer_photo(self):
        url = reverse("customer-detail", kwargs={"pk": self.customer.pk})

        # Generate a test image file
        photo_file = generate_photo_file()
        photo = SimpleUploadedFile(
            name="test_image.png",
            content=photo_file.getvalue(),
            content_type="image/png",
        )

        data = {"photo": photo}
        response = self.client.patch(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()

        # Check if the photo field is not empty
        self.assertIsNotNone(self.customer.photo)

        # Check if the photo field contains image data
        self.assertTrue(self.customer.photo.file.read())

        # Check if the photo has been written to disk
        self.assertTrue(os.path.exists(self.customer.photo.path))

    def tearDown(self):
        # Clean up any files created during tests
        for customer in Customer.objects.all():
            if customer.photo:
                customer.photo.delete()


class UserAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_admin=True)
        self.normal_user = User.objects.create_user(username='normal', password='normalpass')
        self.url = reverse("user-set-admin-status", kwargs={"pk": self.normal_user.pk})

    def test_list_users(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_user(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user-list")
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "new@example.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_set_admin_status_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.url, {"is_admin": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.normal_user.refresh_from_db()
        self.assertTrue(self.normal_user.is_admin)

    def test_remove_admin_status_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        self.normal_user.is_admin = True
        self.normal_user.save()
        response = self.client.patch(self.url, {"is_admin": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.normal_user.refresh_from_db()
        self.assertFalse(self.normal_user.is_admin)

    def test_set_admin_status_invalid_input(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.url, {"is_admin": "not a boolean"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.normal_user.refresh_from_db()
        self.assertFalse(self.normal_user.is_admin)

    def test_set_admin_status_missing_input(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.normal_user.refresh_from_db()
        self.assertFalse(self.normal_user.is_admin)

    def test_update_user_admin_status_regular_update(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user-detail", kwargs={"pk": self.normal_user.pk})
        response = self.client.patch(url, {"is_admin": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.normal_user.refresh_from_db()
        self.assertTrue(self.normal_user.is_admin)

    def test_set_admin_status_by_non_admin(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.patch(self.url, {"is_admin": True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.normal_user.refresh_from_db()
        self.assertFalse(self.normal_user.is_admin)
