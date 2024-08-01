from django.http import Http404
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from kanbanboard.models import Ticket
from kanbanboard.serializers import TicketCreateSerializer, TicketListSerializer

# Create your views here.


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "password": user.password,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "groups": user.groups.values_list("name", flat=True),
            }
        )


class TicketListView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
       
        tickets = Ticket.objects.filter(created_by=request.user)
        serializer = TicketListSerializer(tickets, many=True)
        return Response(serializer.data)
      
      
# class TicketCreateView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         serializer = TicketCreateSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print(request.data)  # Debug-Log für empfangene Daten
        serializer = TicketCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Debug-Log für Fehlerdetails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class TicketDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ticket = self.get_object(pk)
        serializer = TicketCreateSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        ticket = self.get_object(pk)
        serializer = TicketCreateSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

    def delete(self, request, pk, format=None):
        ticket = self.get_object(pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  