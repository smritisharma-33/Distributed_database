from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, BusService, HotelService, HotelBooking, BusBooking
from .serializers import UserSerializer, BusSerializer, HotelSerializer, HotelBookingSerializer, HotelBookingInfoSerializer, UpdateStatusSerializer, BusBookingSerializer
from rest_framework import status
import requests
import json

class UpdateStatus(object):

    def __init__(self, db_name_1, db_name_2):
        self.db_name_1 = db_name_1
        self.db_name_2 = db_name_2

class UserList(APIView):

    def get(self, request, format = None):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)

class GetUser(APIView):

    def get_object(self, email):
        return User.objects.filter(email = email)

    def get(self, request, format = None):
        user = self.get_object(request.data.get('email'))
        if not user:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(user, many = True)
            return Response(serializer.data)

class InsertUser(APIView):

    def get_object(self, email):
        return User.objects.filter(email = email)

    def post(self, request, format = None):
        user = self.get_object(request.data.get('email'))
        if not user:
            try:
                new_user = User(email = request.data.get('email'),
                                password = request.data.get('password'),
                                token = request.data.get('token'),
                                type = request.data.get('type'))

                new_user.full_clean()
                new_user.save()
                return Response(status = status.HTTP_201_CREATED)
            except Exception as e:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class UpdateUser(APIView):

    def get_object(self, email):
        return User.objects.filter(email = email)

    def post(self, request, format = None):
        user = self.get_object(request.data.get('email'))
        if not user:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            user = user[0]
            try:
                if request.data.get('token') != None:
                    user.token = request.data.get('token')
                if request.data.get('password') != None:
                    user.password = request.data.get('password')
                if request.data.get('type') != None:
                    user.type = request.data.get('type')
                user.full_clean()
                user.save()

                if request.data.get('db_addr_1') != None:
                    DATA = {}
                    UP = {'db_addr_1': False, 'db_addr_2': False}
                    for item in request.data:
                        DATA[item] = request.data.get(item)
                    db_addr_1 = DATA['db_addr_1']
                    db_addr_2 = DATA['db_addr_2']
                    del DATA['db_addr_1']
                    del DATA['db_addr_2']

                    try:
                        r1 = requests.post(db_addr_1, data = DATA)
                        if r1.status_code == 200:
                            UP['db_addr_1'] = True
                    except:
                        pass

                    try:
                        r2 = requests.post(db_addr_2, data = DATA)
                        if r2.status_code == 200:
                            UP['db_addr_2'] = True
                    except:
                        pass

                    serializer = UpdateStatusSerializer(UP)
                    return Response(serializer.data, status = status.HTTP_200_OK)

                else:
                    return Response(status = status.HTTP_200_OK)

            except:
                return Response(status = status.HTTP_400_BAD_REQUEST)

class BusServiceList(APIView):

    def get(self, request, format = None):
        services = BusService.objects.all()
        serializer = BusSerializer(services, many = True)
        return Response(serializer.data)

class BusServiceListEmail(APIView):

    def post(self, request, format = None):
        services = BusService.objects.filter(provider__contains = list([request.data.get('email')]))
        serializer = BusSerializer(services, many = True)
        return Response(serializer.data)

class NewBusService(APIView):

    def get_object(self, id):
        return BusService.objects.filter(id = id)

    def post(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        if not service:
            try:
                new_service = BusService(   id = request.data.get('id'),
                                            name = request.data.get('name'),
                                            provider = list([request.data.get('provider')]))
                new_service.full_clean()
                new_service.save()
                return Response(status = status.HTTP_201_CREATED)
            except Exception as e:
                print('EXCEPTION THROW')
                print(e)
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class UpdateBusService(APIView):

    def get_object(self, id):
        return BusService.objects.filter(id = id)

    def post(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        print('HERE')
        print(service.count())
        if not service:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            try:
                if request.data.get('provider') != None and request.data.get('provider_code') == None:
                    return Response(status = status.HTTP_400_BAD_REQUEST)
                if request.data.get('route') != None and request.data.get('route_code') == None:
                    return Response(status = status.HTTP_400_BAD_REQUEST)
                if request.data.get('timing') != None and request.data.get('timing_code') == None:
                    return Response(status = status.HTTP_400_BAD_REQUEST)
                if request.data.get('boarding_point') != None and request.data.get('boarding_code') == None:
                    return Response(status = status.HTTP_400_BAD_REQUEST)

                service = service[0]
                if request.data.get('name') != None:
                    service.name = request.data.get('name')
                if request.data.get('price') != None:
                    service.price = int(request.data.get('price'))
                if request.data.get('bus_number') != None:
                    service.bus_number = request.data.get('bus_number')
                if request.data.get('seats') != None:
                    service.seats = request.data.get('seats')
                if request.data.get('is_ready') != None:
                    service.is_ready = request.data.get('is_ready')
                if request.data.get('provider') != None and request.data.get('provider_code') == 'ADD':
                    service.provider.append(request.data.get('provider'))
                if request.data.get('route') != None and request.data.get('route_code') == 'ADD':
                    service.route.append(request.data.get('route'))
                if request.data.get('timing') != None and request.data.get('timing_code') == 'ADD':
                    service.timing.append(request.data.get('timing'))
                if request.data.get('boarding_point') != None and request.data.get('boarding_code') == 'ADD':
                    service.boarding_point.append(request.data.get('boarding_point'))
                if request.data.get('provider') != None and request.data.get('provider_code') == 'REMOVE':
                    service.provider.remove(request.data.get('provider'))
                if request.data.get('route') != None and request.data.get('route_code') == 'REMOVE':
                    service.route.remove(service.route[int(request.data.get('route'))])
                if request.data.get('timing') != None and request.data.get('timing_code') == 'REMOVE':
                    service.timing.remove(service.timing[int(request.data.get('timing'))])
                if request.data.get('boarding_point') != None and request.data.get('boarding_code') == 'REMOVE':
                    service.boarding_point.remove(service.boarding_point[int(request.data.get('boarding_point'))])
                service.full_clean()
                service.save()

                if request.data.get('db_addr_1') != None:
                    DATA = {}
                    UP = {'db_addr_1': False, 'db_addr_2': False}
                    for item in request.data:
                        DATA[item] = request.data.get(item)
                    db_addr_1 = DATA['db_addr_1']
                    db_addr_2 = DATA['db_addr_2']
                    del DATA['db_addr_1']
                    del DATA['db_addr_2']

                    try:
                        r1 = requests.post(db_addr_1, data = DATA)
                        if r1.status_code == 200:
                            UP['db_addr_1'] = True
                    except:
                        pass

                    try:
                        r2 = requests.post(db_addr_2, data = DATA)
                        if r2.status_code == 200:
                            UP['db_addr_2'] = True
                    except:
                        pass

                    serializer = UpdateStatusSerializer(UP)
                    return Response(serializer.data, status = status.HTTP_200_OK)

                else:
                    return Response(status = status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return Response(status = status.HTTP_400_BAD_REQUEST)

class GetBusService(APIView):

    def get_object(self, id):
        return BusService.objects.filter(id = id)

    def get(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        if not service:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            serializer = BusSerializer(service, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)

class DeleteBusService(APIView):

    def get_object(self, id):
        return BusService.objects.filter(id = id)

    def post(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        if not service:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            service = service[0]
            service.delete()

            if request.data.get('db_addr_1') != None:
                DATA = {}
                UP = {'db_addr_1': False, 'db_addr_2': False}
                for item in request.data:
                    DATA[item] = request.data.get(item)
                db_addr_1 = DATA['db_addr_1']
                db_addr_2 = DATA['db_addr_2']
                del DATA['db_addr_1']
                del DATA['db_addr_2']

                try:
                    r1 = requests.post(db_addr_1, data = DATA)
                    if r1.status_code == 200:
                        UP['db_addr_1'] = True
                except Exception as e:
                    pass

                try:
                    r2 = requests.post(db_addr_2, data = DATA)
                    if r2.status_code == 200:
                        UP['db_addr_2'] = True
                except Exception as e:
                    pass

                serializer = UpdateStatusSerializer(UP)
                return Response(serializer.data, status = status.HTTP_200_OK)

            else:
                return Response(status = status.HTTP_200_OK)


class HotelServiceList(APIView):

    def get(self, request, format = None):
        services = HotelService.objects.all()
        serializer = HotelSerializer(services, many = True)
        return Response(serializer.data)

class NewHotelService(APIView):

    def get_object(self, id):
        return HotelService.objects.filter(id = id)

    def post(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        if not service:
            try:
                new_service = HotelService( id = request.data.get('id'),
                                            name = request.data.get('name'),
                                            provider = list([request.data.get('provider')]))
                new_service.full_clean()
                new_service.save()
                return Response(status = status.HTTP_201_CREATED)
            except Exception as e:
                print('EXCEPTION THROW')
                print(e)
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class UpdateHotelService(APIView):

    def get_object(self, id):
        return HotelService.objects.filter(id = id)

    def post(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        if not service:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            try:
                if request.data.get('provider') != None and request.data.get('provider_code') == None:
                    return Response(status = status.HTTP_400_BAD_REQUEST)

                service = service[0]
                if request.data.get('name') != None:
                    service.name = request.data.get('name')
                if request.data.get('price') != None:
                    service.price = int(request.data.get('price'))
                if request.data.get('city') != None:
                    service.city = request.data.get('city')
                if request.data.get('area') != None:
                    service.area = request.data.get('area')
                if request.data.get('address') != None:
                    service.address = request.data.get('address')
                if request.data.get('rooms') != None:
                    service.rooms = request.data.get('rooms')
                if request.data.get('description') != None:
                    service.description = request.data.get('description')
                if request.data.get('is_ready') != None:
                    service.is_ready = request.data.get('is_ready')
                if request.data.get('check_in') != None:
                    service.check_in = request.data.get('check_in')
                if request.data.get('check_out') != None:
                    service.check_out = request.data.get('check_out')
                if request.data.get('provider') != None and request.data.get('provider_code') == 'ADD':
                    service.provider.append(request.data.get('provider'))
                if request.data.get('provider') != None and request.data.get('provider_code') == 'REMOVE':
                    service.provider.remove(request.data.get('provider'))

                service.full_clean()
                service.save()

                if request.data.get('db_addr_1') != None:
                    DATA = {}
                    UP = {'db_addr_1': False, 'db_addr_2': False}
                    for item in request.data:
                        DATA[item] = request.data.get(item)
                    db_addr_1 = DATA['db_addr_1']
                    db_addr_2 = DATA['db_addr_2']
                    del DATA['db_addr_1']
                    del DATA['db_addr_2']

                    try:
                        r1 = requests.post(db_addr_1, data = DATA)
                        if r1.status_code == 200:
                            UP['db_addr_1'] = True
                    except:
                        pass

                    try:
                        r2 = requests.post(db_addr_2, data = DATA)
                        if r2.status_code == 200:
                            UP['db_addr_2'] = True
                    except:
                        pass

                    serializer = UpdateStatusSerializer(UP)
                    return Response(serializer.data, status = status.HTTP_200_OK)

                else:
                    return Response(status = status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return Response(status = status.HTTP_400_BAD_REQUEST)

class GetHotelService(APIView):

    def get_object(self, id):
        return HotelService.objects.filter(id = id)

    def get(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        if not service:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            serializer = HotelSerializer(service, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)

class HotelServiceListEmail(APIView):

    def post(self, request, format = None):
        services = HotelService.objects.filter(provider__contains = list([request.data.get('email')]))
        serializer = HotelSerializer(services, many = True)
        return Response(serializer.data)

class GetHotelByCity(APIView):

    def post(self, request, format = None):
        if request.data.get('area') == None or request.data.get('area') == '':
            services = HotelService.objects.filter(city = request.data.get('city'), is_ready = True)
        else:
            services = HotelService.objects.filter(city = request.data.get('city'), area = request.data.get('area'), is_ready = True)
        serializer = HotelSerializer(services, many = True)
        return Response(serializer.data)

class DeleteHotelService(APIView):

    def get_object(self, id):
        return HotelService.objects.filter(id = id)

    def post(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        if not service:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            service = service[0]
            service.delete()
            if request.data.get('db_addr_1') != None:
                DATA = {}
                UP = {'db_addr_1': False, 'db_addr_2': False}
                for item in request.data:
                    DATA[item] = request.data.get(item)
                db_addr_1 = DATA['db_addr_1']
                db_addr_2 = DATA['db_addr_2']
                del DATA['db_addr_1']
                del DATA['db_addr_2']

                try:
                    r1 = requests.post(db_addr_1, data = DATA)
                    if r1.status_code == 200:
                        UP['db_addr_1'] = True
                except:
                    pass

                try:
                    r2 = requests.post(db_addr_2, data = DATA)
                    if r2.status_code == 200:
                        UP['db_addr_2'] = True
                except:
                    pass

                serializer = UpdateStatusSerializer(UP)
                return Response(serializer.data, status = status.HTTP_200_OK)

            else:
                return Response(status = status.HTTP_200_OK)

class HotelBookingList(APIView):

    def get(self, request, format = None):
        services = HotelBooking.objects.all()
        serializer = HotelBookingSerializer(services, many = True)
        return Response(serializer.data)

class HotelBookingByHotel(APIView):

    def get_object(self, service_id, in_date, out_date):
        queryset = HotelBooking.objects.filter(service_id = service_id, in_date__lt = out_date, out_date__gt = in_date)
        return queryset

    def post(self, request, format = None):
        bookings = self.get_object(service_id = request.data.get('service_id'), in_date = request.data.get('in_date'), out_date = request.data.get('out_date'))
        serializer = HotelBookingSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class NewHotelBooking(APIView):

    def post(self, request, format = None):
        booking = HotelBooking.objects.filter(id = request.data.get('id'))
        if not booking:
            try:
                new_booking = HotelBooking( id = request.data.get('id'),
                                            service_id = request.data.get('service_id'),
                                            email = request.data.get('email'),
                                            in_date = request.data.get('in_date'),
                                            out_date = request.data.get('out_date'),
                                            booking_date = request.data.get('booking_date'),
                                            rooms = request.data.get('rooms'),
                                            bill = request.data.get('bill'))
                new_booking.full_clean()
                new_booking.save()
                return Response(status = status.HTTP_201_CREATED)
            except:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class GetHotelBookingByUser(APIView):

    def get(self, request, email, format = None):
        bookings = HotelBooking.objects.filter(email = email)
        serializer = HotelBookingInfoSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class GetHotelBookingById(APIView):

    def get(self, request, id, format = None):
        bookings = HotelBooking.objects.filter(id = id)
        serializer = HotelBookingSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class DeleteHotelBooking(APIView):

    def post(self, request, format = None):
        booking = HotelBooking.objects.get(id = request.data.get('id'))
        booking.delete()

        if request.data.get('db_addr_1') != None:
            DATA = {}
            UP = {'db_addr_1': False, 'db_addr_2': False}
            for item in request.data:
                DATA[item] = request.data.get(item)
            db_addr_1 = DATA['db_addr_1']
            db_addr_2 = DATA['db_addr_2']
            del DATA['db_addr_1']
            del DATA['db_addr_2']

            try:
                r1 = requests.post(db_addr_1, data = DATA)
                if r1.status_code == 200:
                    UP['db_addr_1'] = True
            except:
                pass

            try:
                r2 = requests.post(db_addr_2, data = DATA)
                if r2.status_code == 200:
                    UP['db_addr_2'] = True
            except:
                pass

            serializer = UpdateStatusSerializer(UP)
            return Response(serializer.data, status = status.HTTP_200_OK)

        else:
            return Response(status = status.HTTP_200_OK)

class HotelBookingsByDate(APIView):

    def get_object(self, service_id, date):
        queryset = HotelBooking.objects.filter(service_id = service_id, in_date__lte = date, out_date__gt = date)
        return queryset

    def post(self, request):
        bookings = self.get_object(request.data.get('id'), request.data.get('date'))
        serializer = HotelBookingSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class StatusView(APIView):

    def get(self, request):
        return Response(status = status.HTTP_200_OK)

# class GetHotelByCity(APIView):
#
#     def get_object(self, city, area = None):
#         if area == None or area == '':
#             return HotelBooking.objects.filter(city = city.upper())
#         else:
#             return HotelBooking.objects.filter(city = city.upper(), area = area.upper())
#
#     def get(self, request, format = None):
#         queryset = self.get_object(request.data.get('city'), request.data.get('area'))
#         serializer = HotelBookingSerializer(queryset, many = True)
#         return Response(serializer.data, status = status.HTTP_200_OK)

class GetBusByCity(APIView):

    def post(self, request, format = None):
        services = BusService.objects.filter(route__contains = [request.data.get('From'), request.data.get('To')], is_ready=True)
        S = []
        for service in services:
            idx1 = service.route.index(request.data.get('From'))
            idx2 = idx1
            for i in range(idx1 + 1, len(service.route)):
                if service.route[i] == request.data.get('To'):
                    idx2 = i
                    break
            if idx2 > idx1:
                S.append(service)
        serializer = BusSerializer(S, many = True)
        return Response(serializer.data)

class BusBookingByBus(APIView):

    def get_object(self, service_id, TravelDate):
        queryset = BusBooking.objects.filter(service_id = service_id, TravelDate = TravelDate)
        return queryset

    def post(self, request, format = None):
        bookings = self.get_object(service_id = request.data.get('service_id'), TravelDate = request.data.get('TravelDate'))
        serializer = BusBookingSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class NewBusBooking(APIView):

    def post(self, request, format = None):
        booking = BusBooking.objects.filter(id = request.data.get('id'))
        if not booking:
            try:
                new_booking = BusBooking(   id = request.data.get('id'),
                                            service_id = request.data.get('service_id'),
                                            email = request.data.get('email'),
                                            From = request.data.get('From'),
                                            To = request.data.get('To'),
                                            TravelDate = request.data.get('TravelDate'),
                                            booking_date = request.data.get('booking_date'),
                                            seats = request.data.get('seats'),
                                            bill = request.data.get('bill'))
                new_booking.full_clean()
                new_booking.save()

                return Response(status = status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class GetBusBookingById(APIView):

    def get(self, request, id, format = None):
        bookings = BusBooking.objects.filter(id = id)
        serializer = BusBookingSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class DeleteBusBooking(APIView):

    def post(self, request, format = None):
        booking = BusBooking.objects.get(id = request.data.get('id'))
        booking.delete()

        if request.data.get('db_addr_1') != None:
            DATA = {}
            UP = {'db_addr_1': False, 'db_addr_2': False}
            for item in request.data:
                DATA[item] = request.data.get(item)
            db_addr_1 = DATA['db_addr_1']
            db_addr_2 = DATA['db_addr_2']
            del DATA['db_addr_1']
            del DATA['db_addr_2']

            try:
                r1 = requests.post(db_addr_1, data = DATA)
                if r1.status_code == 200:
                    UP['db_addr_1'] = True
            except:
                pass

            try:
                r2 = requests.post(db_addr_2, data = DATA)
                if r2.status_code == 200:
                    UP['db_addr_2'] = True
            except:
                pass

            serializer = UpdateStatusSerializer(UP)
            return Response(serializer.data, status = status.HTTP_200_OK)

        else:
            return Response(status = status.HTTP_200_OK)

class GetBusBookingByUser(APIView):

    def get(self, request, email, format = None):
        bookings = BusBooking.objects.filter(email = email)
        serializer = BusBookingSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class BusBookingsByDate(APIView):

    def get_object(self, service_id, date):
        queryset = BusBooking.objects.filter(service_id = service_id, TravelDate = date)
        return queryset

    def post(self, request):
        bookings = self.get_object(request.data.get('id'), request.data.get('date'))
        serializer = BusBookingSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
