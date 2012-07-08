from blog.forms import CommentForm
from django.test import TestCase

class CommentFormTests(TestCase):
    fixtures = ['categories','posts']
    
    def setUp(self):
        self.form_data = {
            'name': "John",
            'content': "This is a test",
            'post': 1
        }

    def test_comment_form(self):
        self.assertTrue(CommentForm(data=dict(**self.form_data)).is_valid())
