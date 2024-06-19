from rest_framework import serializers
from .models import User, BusService, HotelService, HotelBooking, BusBooking

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('password', 'email', 'type', 'token', 'activated', )

class BusSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusService
        fields = ('id', 'name', 'route', 'timing', 'price', 'bus_number', 'is_ready', 'provider', 'seats', 'boarding_point', )

class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelService
        fields = ('id', 'name', 'city', 'area', 'check_in', 'check_out', 'price', 'is_ready', 'provider', 'rooms', 'address', 'description', )

class HotelBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelBooking
        fields = ('id', 'service_id', 'email', 'in_date', 'out_date', 'booking_date', 'rooms', 'bill', )

class HotelBookingInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelBooking
        fields = ('id', 'service_id', 'in_date', 'out_date', 'rooms', )

class UpdateStatusSerializer(serializers.Serializer):

    db_addr_1 = serializers.BooleanField()
    db_addr_2 = serializers.BooleanField()

class BusBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusBooking
        fields = ('id', 'service_id', 'email', 'From', 'To', 'booking_date', 'seats', 'bill', 'TravelDate', )
