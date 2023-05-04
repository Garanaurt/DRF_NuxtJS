from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PostSerializer, TagSerializer, RegisterSerializer, UserSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import generics
from taggit.models import Tag
from rest_framework import filters




class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.PageNumberPagination

class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'created_at'



class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:3]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })
    
class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args,  **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })
    

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)