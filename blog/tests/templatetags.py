from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase

class BlogTemplateTagTests(TestCase):
    fixtures = ['categories']

    def test_get_categories_tag(self):
        out = Template(
                "{% load blog %}"
                "{% get_category %}"
            ).render(Context())
        self.assertIn("First",out)