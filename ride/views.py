from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# from .models import Ride
from .serializers import *
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class RideListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({})
        # rides = Ride.objects.all()
        # serializer = RideSerializer(rides, many=True)
        # return Response(serializer.data)



class Userdetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_id = request.user.id

            user = get_object_or_404(User, id=user_id)

            serializer = UserSerializer(user)

            return Response(serializer.data)
            
        except Exception as e:
            print(e)
            return None



def ride_view(request):
    return render(request, 'index.html')

