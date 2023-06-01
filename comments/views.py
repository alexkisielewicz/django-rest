from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

# use generiv view not to repeat same classes and methods for different api endpoints
# we dont have to write get method and create replaces post method
# context is a part of generic request by default
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    # only comment owner can perform crud isownerorreadonly
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
    # request is passed in context object by default