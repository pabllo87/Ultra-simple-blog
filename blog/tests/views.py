from blog.models import Comment, Post
from django.test import TestCase

class BlogViewTests(TestCase):
    fixtures = ['categories','posts']

    def test_view_category_list(self):
        response = self.client.get('/lists/first/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("First", response.content)

    def test_view_non_existent_category(self):
        response = self.client.get('/lists/no_such_category/')
        self.assertEqual(response.status_code, 404)
        
    def test_view_category_list_posts(self):
        response = self.client.get('/lists/first/')
        self.assertIn('<div class="post">', response.content)
        
    def test_view_category_list_without_posts(self):
        response = self.client.get('/lists/second/')
        self.assertNotIn('<div class="post">', response.content)
        
    def test_view_post(self):
        response = self.client.get('/first-post/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("First", response.content)
        
    def test_view_not_existent_post(self):
        response = self.client.get('/no_such_posts/')
        self.assertEqual(response.status_code, 404)
        
    def test_view_can_handle_comment_vis_POST(self):
        post = Post.objects.get(pk=1)
        post_data = {'name': "John", 'content' : "Cool", 'post' : post}

        post_url = '/%s/' % (post.slug, )
        response = self.client.post(post_url, data=post_data)

        comment_in_db = Comment.objects.get(post=post)

        self.assertEquals(comment_in_db.name, post_data['name'])
        self.assertEquals(comment_in_db.content, post_data['content'])

        self.assertRedirects(response, post_url)        
