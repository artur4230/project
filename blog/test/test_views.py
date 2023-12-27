from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Post
from ..serializers import BlogPostListSerializer

User=get_user_model()

client=Client()

class GetALLPostsTest(TestCase):
    def setUp(self):
        author = User.objects.create(username='author #1')
        Post.objects.create(title='Blog Post #1',
                            text='Dummy text #1',
                            author=author)
        Post.objects.create(title='Blog Post #2',
                            text='Dummy text #2',
                            author=author)
        Post.objects.create(title='Blog Post #3',
                            text='Dummy text #3',
                            author=author)
    def test_get_all_posts(self):
        response = client.get(reverse('post-list'))
        posts = Post.objects.all()
        serializer = BlogPostListSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class GetSinglePostTest(TestCase):
    def setUp(self):
        author = User.objects.create(username='test')
        self.post = Post.objects.create(title='Blog Post #1', author=author)
    def test_get_valid_single_post(self):
        response = client.get(
            reverse('post-detail',kwargs={'pk':self.post.pk}))
        post=Post.objects.get(pk=self.post.pk)
        serializer=BlogPostDetailSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_invalid_single_post(self):
        response = client.get(reverse('post-detail',kwargs={'pk':9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
class CreateNewPostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.valid_payload = {
            'title': 'Blog Post #1',
            'text': 'Blog Post Description',
            'author':1,
            }
        self.invalid_payload = {
            'title':'Blog Post #1',
            'author':2.
            }
    def test_create_valid_single_post(self):
        response = client.post(reverse('post-list'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_create_invalid_single_post(self):
        response = client.post(reverse('post-list'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class UpdateSinglePostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.post = Post.objects.create(title='Blog Post #1',
                                        text='Post Description',
                                        author=self.author)
        self.valid_payload={
            'title':'Blog Post #1',
            'text':'Blog Post Description',
            'author':1,
            }
        self.invalid_payload={
            'title':'Blog Post #1',
            'text':None,
            'author':1,
            }
        def test_valid_update_post(self):
            response=client.put(reverse('post-detail',
                                        kwargs={'pk':self.post.pk}),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json')
            self.asserEqual(response.status_code, status.HTTP_200_OK)
        def test_invalid_update_post(self):
            response=client.put(reverse('post-detail',
                                        kwargs={'pk':self.post.pk}),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json')
            self.asserEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class DeleteSinglePostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.post = Post.objects.create(title='Blog Post #1',
                                        text='Post Description',
                                        author=self.author)
    def test_valid_delete_post(self):
        response = client.delete(
            reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_COMMENT)
    def test_invalid_delete_post(self):
        response = client.delete(reverse('post-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
class PublishSinglePostTest(TestCase):
    def setUp(self):
        self.api=APIClient()
        self.author = User.objects.create(username='test', password='test')
        self.post=Post.objects.create(title='Blog Post #1',
                                      text='Post Description',
                                      author=self.author,
                                      is_published=False)
    def test_unauth_publish_post(self):
        response=client.post(reverse('post-publish',args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_publish_post(self):
        self.api.force_authenticate(user=self.author)
        response=self.api.post(reverse('post-publish', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post=Post.objects.get(title='Blog Post #1')
        self.assertEqual(post.is_published,True)
