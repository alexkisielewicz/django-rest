from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all() # return all the profiles
        serializer = ProfileSerializer(profiles, many=True, context={'request': request}) # serialize them
        return Response(serializer.data) # serialize data in the response
    

class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404 # "not found"
        
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    
    # method put for profile edit
    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

# DRF permission classes
# AllowAny
# IsAuthenticated
# isAdminUser
# isAuthenticatedOrReadOnly
# BasePermission - to write custom permissions - object level to see if a user is the owner