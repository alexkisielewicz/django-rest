from django.db.models import Count
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    # thanks to annotate we can add additional fields to queryset
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True), # double underscore to show relation
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True) 
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile' 
    ]
    
    ordering_fields = [
        'post_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True), # double underscore to show relation
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True) 
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
