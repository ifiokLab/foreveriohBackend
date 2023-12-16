from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from .serializers import *
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class LoginView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        print('user:',user)

        if user:
            print('hello')
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'auth_token': token.key, 
            }
            print(user_data)
            return Response({'success': True, 'message': 'Login successful', 'user': user_data})
        else:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logged out successfully'})

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MyUserSerializer(data=request.data)
        print('hello')
        print(request.data)
        if serializer.is_valid():
            print('valid..')
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            login(request, user)
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return Response({'success': True, 'message': 'Signup successful', 'user': user_data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'Signup failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
class CreateMemorialView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print('hello:',request.data)
        print('user:',self.request.user)
        print(request.headers)
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('user:',user)
        serializer = DeceasedSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)  # Assuming you are using authentication and have a user associated with the request
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMemorialsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Fetch memorials for the current user
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        memorials = Deceased.objects.filter(user=user)
        # Serialize the memorials
        serializer = MemorialSerializer(memorials, many=True)
        
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class DeleteMemorialView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, memorial_id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        try:
            # Ensure the memorial exists
            memorial = Deceased.objects.get(id=memorial_id, user=user)
        except Deceased.DoesNotExist:
            return Response({'detail': 'Memorial not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the memorial
        memorial.delete()

        return Response({'detail': 'Memorial deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



class EditMemorialView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, memorial_id):
        # Fetch the memorial object
        memorial = get_object_or_404(Deceased, pk=memorial_id)
        
        # Serialize the memorial
        serializer = MemorialSerializer(memorial)
        return Response(serializer.data)

    def put(self, request, memorial_id):
        # Fetch the memorial object
        memorial = get_object_or_404(Deceased, pk=memorial_id)

        # Update the memorial with new data from the request
        serializer = MemorialSerializer(memorial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MemorialListView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization', '')
        print('auth_header')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        memorials = Deceased.objects.all()
        #serializer = MemorialSerializer(memorials, many=True)
        #print('serializer.data:',serializer.data)
        all_memorials = []
        for memorial in memorials:
            memorial_data = {
                'id': memorial.id,
                'creatorId': memorial.user.id,
                'user': f"{memorial.user.first_name} {memorial.user.last_name}",
                'first_name': memorial.first_name,
                'last_name': memorial.last_name,
                'city': memorial.city,
                'relationship_type': memorial.relationship_type,
                'audience': memorial.audience,
                'date_of_birth': memorial.date_of_birth,
                'date_of_death': memorial.date_of_death,
                'date_of_death': memorial.date_of_death,
                'cover_photo': memorial.cover_photo.url,
                'heart': memorial.heart.count(),
                'share': memorial.share.count(),
                'isLiked':'true' if user in memorial.heart.all() else 'false',
                'tributeCount':Tribute.objects.filter(deceased__id = memorial.id).count(),
                
            }
            all_memorials.append(memorial_data)
            print(all_memorials)
        return Response({'all_memorials':all_memorials}, status=status.HTTP_200_OK)



class AddTributeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        deceasedId = request.data['deceasedId']
        deceased= Deceased.objects.get(id = deceasedId)
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        serializer = TributeSerializer(data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save(user=user,deceased = deceased)  # Assuming you are using authentication and have a user associated with the request
            tributes = Tribute.objects.filter(deceased=deceased)
            all_tributes = []
            for tribute in tributes:
                tribute_data = {
                    'id': tribute.id,
                    'user': f"{tribute.user.first_name} {tribute.user.last_name}",
                    'text': tribute.text,
                    'likes': tribute.likes.count(),
                    'heart': tribute.heart.count(),
                    'time_since_comment': tribute.get_time_since_comment(),
                    'tributeCount':tributes.count(),
                }
                all_tributes.append(tribute_data)
            print('tribute_serializer:',all_tributes)
            return Response({'all_tributes': all_tributes}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TributeListView(APIView):
    def get(self, request,deceased_id):
        tributes = Tribute.objects.filter(deceased__id=deceased_id)
        all_tributes = []
        for tribute in tributes:
            tribute_data = {
                'id': tribute.id,
                'user': f"{tribute.user.first_name} {tribute.user.last_name}",
                'text': tribute.text,
                'likes': tribute.likes.count(),
                'heart': tribute.heart.count(),
                'time_since_comment': tribute.get_time_since_comment(),
                'tributeCount':tributes.count(),
            }
            all_tributes.append(tribute_data)
        return Response({'all_tributes': all_tributes}, status=status.HTTP_200_OK)


class HeartDeceasedView(APIView):
    def post(self, request, deceased_id, *args, **kwargs):
        # Assuming you have authentication in place
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        # Get the Deceased object
        deceased = get_object_or_404(Deceased, id=deceased_id)

        # Check if the user has already liked, and toggle the like
        if user in deceased.heart.all():
            deceased.heart.remove(user)
            print('removed:',deceased.heart.count())
        else:
            deceased.heart.add(user)
            print('added:',deceased.heart.count())
        
        # Save the changes
        deceased.save()

        return Response({'message': 'Like toggled successfully'}, status=status.HTTP_200_OK)