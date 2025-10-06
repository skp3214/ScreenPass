from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Show, Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    show = ShowSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        
class BookingCreateSerializer(serializers.Serializer):
    seat_number = serializers.IntegerField(min_value=1)