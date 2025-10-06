from django.urls import path
from .views import SignupView, LoginView, MovieListView, ShowListView, book_seat, cancel_booking,MyBookingsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/shows/', ShowListView.as_view(), name='show-list'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
    path('bookings/<int:id>/cancel/', cancel_booking, name='cancel-booking'),
    path('shows/<int:id>/book/', book_seat, name='book-seat'),
]
