from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Movie, Show, Booking
from .serializers import (UserSerializer, MovieSerializer, ShowSerializer, 
                          BookingSerializer, BookingCreateSerializer)
from django.contrib.auth.models import User
# Create your views here.

class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    

class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    
class ShowListView(ListAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Show.objects.filter(movie_id=movie_id)

class MyBookingsView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, status='booked').order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def book_seat(request, id):
    serializer = BookingCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    seat_number = serializer.validated_data['seat_number']
    show = get_object_or_404(Show, id=id)
    
    if seat_number < 1 or seat_number > show.total_seats:
        return Response({"error": "Invalid seat number."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      with transaction.atomic():
          existing_booked = Booking.objects.select_for_update().filter(
                show=show, seat_number=seat_number, status='booked'
            ).first()
          if existing_booked:
              return Response({"error": "Seat already booked."}, status=status.HTTP_400_BAD_REQUEST)
          booking = Booking.objects.create(
              user = request.user,
              show = show,
              seat_number = seat_number,
                status = 'booked'
          )
          booking_serializer = BookingSerializer(booking)
          return Response(booking_serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request,id):
    booking = get_object_or_404(Booking, id=id)
    if booking.user != request.user:
        return Response({"error": "You can only cancel your own bookings."}, status=status.HTTP_403_FORBIDDEN)
    
    if booking.status == 'cancelled':
        return Response({"error": "Booking is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        booking.status = 'cancelled'
        booking.save()
        return Response({"message": "Booking cancelled successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    