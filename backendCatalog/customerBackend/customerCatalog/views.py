from django.shortcuts import render
from .models import User
from .serializer import UserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .customer_producer import RabbitMQProducer

customerProducer = RabbitMQProducer(exchange_name="customerCatalog")

@api_view(['POST'])
def addUser(request) :
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        customerProducer.publish("user_created",serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUsers(request) :
    users = User.objects.all()
    serializer = UserSerializer(users,many = True)
    return Response(serializer.data)

@api_view(['GET','PUT'])
def userDetail(request, id) :
    try:
        user = User.objects.get(pk = id)
    except :
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    email = user.email
    if request.method == 'PUT':
        serializer = UserSerializer(user, data= request.data)
        if serializer.is_valid():
            try : 
                serializer.save()
                customerProducer.publish("user_updated",{**serializer.data,"old-email":email})
                return Response(serializer.data)
            except Exception as e:
                return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, id) :
    try:
        user = User.objects.get(pk = id)
    except :
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    email = user.email
    user.delete()
    customerProducer.publish("user_deleted",{"email":email})
    return Response("User deleted")
