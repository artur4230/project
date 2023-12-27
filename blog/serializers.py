from rest_framework import serializers, viewsets, routers
from .models import Comment
from .core.views import CommentViewSet

class CommentSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=200)
    created_date = serializers.DateTimeField()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'created_date')
class BlogPostListSerializer(serializers.ModelSerializer):
    preview_text=serializers.SerializerMethodField()

    def get_preview_text(self,post):
        return post.get_text_preview()
    class Meta:
        model = Post
        fields=('title','author','created_date','preview_text')

'''class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()'''
    
class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostListSerializer
    queryset=Post.objects.all()

router=routers.DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns=[
    path('', include(router.urls)),
    ]
