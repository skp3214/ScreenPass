from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Movie, Show, Booking

User = get_user_model()

class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {'username': 'testuser', 'password': 'testpass123'}
        self.user = User.objects.create_user(**self.user_data)
        self.movie = Movie.objects.create(title='Test Movie', duration_minutes=120)
        self.show = Show.objects.create(
            movie=self.movie, screen_name='Screen 1', date_time='2025-10-07T10:00:00Z', total_seats=5
        )

    def get_auth_token(self):
        login_url = reverse('login')
        response = self.client.post(login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_signup(self):
        signup_url = reverse('signup')
        signup_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(signup_url, signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_seat_success(self):
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        book_url = reverse('book-seat', kwargs={'id': self.show.id})
        book_data = {'seat_number': 1}
        response = self.client.post(book_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.filter(seat_number=1, status='booked').count(), 1)

    def test_double_booking_prevented(self):
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        book_url = reverse('book-seat', kwargs={'id': self.show.id})
        book_data = {'seat_number': 1}
        self.client.post(book_url, book_data, format='json')  # First booking
        response = self.client.post(book_url, book_data, format='json')  # Second attempt
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Seat already booked', response.data['error'])

    def test_invalid_seat_number(self):
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        book_url = reverse('book-seat', kwargs={'id': self.show.id})
        book_data = {'seat_number': 6}  
        response = self.client.post(book_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid seat number.')

    def test_cancel_own_booking(self):
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        booking = Booking.objects.create(user=self.user, show=self.show, seat_number=1, status='booked')
        cancel_url = reverse('cancel-booking', kwargs={'id': booking.id})
        response = self.client.post(cancel_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

    def test_cannot_cancel_other_booking(self):
        other_user = User.objects.create_user(username='other', password='otherpass')
        booking = Booking.objects.create(user=other_user, show=self.show, seat_number=2, status='booked')
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        cancel_url = reverse('cancel-booking', kwargs={'id': booking.id})
        response = self.client.post(cancel_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_bookings(self):
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        Booking.objects.create(user=self.user, show=self.show, seat_number=3, status='booked')
        my_bookings_url = reverse('my-bookings')
        response = self.client.get(my_bookings_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)