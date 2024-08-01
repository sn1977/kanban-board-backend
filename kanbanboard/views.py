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
  """
  View for user login.

  This view handles the authentication of users and generates an authentication token for the user.
  The token can be used for subsequent authenticated requests.

  Inherits from ObtainAuthToken class.

  Methods:
    post(request, *args, **kwargs): Handles the POST request for user login.

  Attributes:
    serializer_class: The serializer class used for validating user credentials.
  """

  def post(self, request, *args, **kwargs):
    """
    Handle HTTP POST requests.

    This method is responsible for creating a new user token and returning the user's information along with the token.

    Args:
      request (HttpRequest): The HTTP request object.
      *args: Variable length argument list.
      **kwargs: Arbitrary keyword arguments.

    Returns:
      Response: The HTTP response containing the user's information and token.

    Raises:
      ValidationError: If the serializer data is invalid.

    """
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
  """
  A view for retrieving a list of tickets created by the authenticated user.

  This view requires token authentication and only allows access to authenticated users.

  Methods:
  - get(request, format=None): Retrieves a list of tickets created by the authenticated user.

  Attributes:
  - authentication_classes: A list of authentication classes used for this view.
  - permission_classes: A list of permission classes used for this view.
  """

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    """
    Retrieves a list of tickets created by the authenticated user.

    Args:
    - request: The HTTP request object.
    - format: The requested format for the response data (default: None).

    Returns:
    - A Response object containing the serialized data of the retrieved tickets.
    """
    tickets = Ticket.objects.filter(created_by=request.user)
    serializer = TicketListSerializer(tickets, many=True)
    return Response(serializer.data)
      

class TicketCreateView(APIView):
  """
  API view for creating a new ticket.

  Requires token authentication and user authentication.

  Methods:
  - post: Handles the POST request to create a new ticket.
  """

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    """
    Handles the POST request to create a new ticket.

    Args:
    - request: The HTTP request object.
    - format: The format of the response data (default: None).

    Returns:
    - If the serializer is valid, returns a response with the serialized data and status code 201 (HTTP_CREATED).
    - If the serializer is not valid, returns a response with the serializer errors and status code 400 (HTTP_BAD_REQUEST).
    """

    print(request.data)  # Debug-Log für empfangene Daten
    serializer = TicketCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)  # Debug-Log für Fehlerdetails
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class TicketDetailView(APIView):
  """
  A view for retrieving, updating, and deleting a ticket.

  Methods:
  - get_object(pk): Retrieves a ticket object based on the provided primary key.
  - get(request, pk, format=None): Retrieves the serialized data of a ticket.
  - put(request, pk, format=None): Updates a ticket with the provided data.
  - delete(request, pk, format=None): Deletes a ticket.
  """

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get_object(self, pk):
    """
    Retrieves a ticket object based on the provided primary key.

    Parameters:
    - pk (int): The primary key of the ticket.

    Returns:
    - Ticket: The ticket object.

    Raises:
    - Http404: If the ticket with the provided primary key does not exist.
    """
    try:
      return Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):
    """
    Retrieves the serialized data of a ticket.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - pk (int): The primary key of the ticket.
    - format (str, optional): The format of the response data. Defaults to None.

    Returns:
    - Response: The serialized data of the ticket.

    Raises:
    - Http404: If the ticket with the provided primary key does not exist.
    """
    ticket = self.get_object(pk)
    serializer = TicketCreateSerializer(ticket)
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    """
    Updates a ticket with the provided data.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - pk (int): The primary key of the ticket.
    - format (str, optional): The format of the request data. Defaults to None.

    Returns:
    - Response: The serialized data of the updated ticket if the update is successful.
      Otherwise, returns the serializer errors with a status of 400 (Bad Request).

    Raises:
    - Http404: If the ticket with the provided primary key does not exist.
    """
    ticket = self.get_object(pk)
    serializer = TicketCreateSerializer(ticket, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    """
    Deletes a ticket.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - pk (int): The primary key of the ticket.
    - format (str, optional): The format of the response data. Defaults to None.

    Returns:
    - Response: A response with a status of 204 (No Content) if the deletion is successful.
    """
    ticket = self.get_object(pk)
    ticket.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
