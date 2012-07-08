# -*- coding: utf-8 *-*
from django.test import TestCase
from blog.models import Category, Post, Comment


class CategoryModelTest(TestCase):
    def test_creating_a_new_category_and_saving_it_to_the_database(self):
        # start by createing a new Category object
        category = Category()
        category.name = "First"
        category.slug = "first"

        # check we can save it to the database
        category.save()

        # now check we can find it in the database again
        all_category_in_database = Category.objects.all()
        self.assertEquals(len(all_category_in_database), 1)
        only_category_in_database = all_category_in_database[0]
        self.assertEquals(only_category_in_database, category)

        # and check that it's saved its two attributes: name and slug
        self.assertEquals(only_category_in_database.name, category.name)
        self.assertEquals(only_category_in_database.slug, category.slug)
        
class PostModelTest(TestCase):
    def test_creating_a_new_post_and_saving_it_to_the_database(self):
        # start by create one Category
        category = Category()
        category.name = "First"
        category.slug = "first"
        category.save()
        
        # create new post
        post = Post()
        post.category = category
        post.title = "First post"
        post.content = "Content"
        post.visable = True
        
        # check we can save it
        post.save()
        
        # check slug
        self.assertEquals(post.slug, "first-post")
        
        # now check we can find it in the database
        all_post_in_database = Post.objects.all()
        self.assertEquals(len(all_post_in_database), 1)
        only_post_in_database = all_post_in_database[0]
        self.assertEquals(only_post_in_database, post)
        
        # check that it's saved all attributes: category, title, content, visable and generate slug
        self.assertEquals(only_post_in_database.category, category)
        self.assertEquals(only_post_in_database.title, post.title)
        self.assertEquals(only_post_in_database.content, post.content)
        self.assertEquals(only_post_in_database.visable, post.visable)
        self.assertEquals(only_post_in_database.slug, post.slug)
        
    def test_unique_slug_generate(self):
        # start by create one Category
        category = Category()
        category.name = "First"
        category.slug = "first"
        category.save()
        
        # create new posts
        post1 = Post(category=category, title="First post", content="Content", visable=True)
        post1.save()
        
        post2 = Post(category=category, title="First post", content="Content", visable=True)
        post2.save()
        
        # check posts then it's the same title
        self.assertEquals(post1.title, post2.title)
        # and different slug
        self.assertNotEquals(post1.slug, post2.slug)
        

class CommentModelTest(TestCase):
    def test_creating_a_new_comment_and_saving_it_to_the_database(self):
        # start by create one Category and one post
        category = Category()
        category.name = "First"
        category.slug = "first"
        category.save()
        
        # create new post
        post = Post()
        post.category = category
        post.title = "First post"
        post.content = "Content"
        post.visable = True
        post.save()
        
        # create one comment
        comment = Comment()
        comment.name = "John"
        comment.content = "This is cool"
        comment.post = post
        
        # check save
        comment.save()
        
        # now check we can find it in the database
        all_comment_in_database = Comment.objects.all()
        self.assertEquals(len(all_comment_in_database), 1)
        only_comment_in_database = all_comment_in_database[0]
        self.assertEquals(only_comment_in_database, comment)
        
        # and check that it's saved its two attributes: name and content
        self.assertEquals(only_comment_in_database.name, comment.name)
        self.assertEquals(only_comment_in_database.content, comment.content)
    
    