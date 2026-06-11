from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import RecruiterProfile
from .serializers import UserSerializer, RegisterSerializer, RecruiterProfileSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecruiterProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            profile = request.user.recruiter_profile
            serializer = RecruiterProfileSerializer(profile)
            return Response(serializer.data)
        except RecruiterProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=404)
    
    def post(self, request):
        if request.user.user_type != 'recruiter':
            return Response({'detail': 'Only recruiters can create this profile'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = RecruiterProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            profile = request.user.recruiter_profile
            serializer = RecruiterProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RecruiterProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=404)