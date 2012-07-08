import os
from django.conf import settings
from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase

class FlatpageTemplateTagTests(TestCase):
    fixtures = ['sample_flatpages']
    urls = 'flatpages.tests.urls'

    def setUp(self):
        self.old_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        flatpage_middleware_class = 'flatpages.middleware.FlatpageFallbackMiddleware'
        if flatpage_middleware_class not in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += (flatpage_middleware_class,)
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            os.path.join(
                os.path.dirname(__file__),
                'templates'
            ),
        )

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS

    def test_get_flatpages_tag(self):
        "The flatpage template tag retrives unregistered prefixed flatpages by default"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages as flatpages %}"
                "{% for page in flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context())
        self.assertIn("A Flatpage,A Nested Flatpage,", out)

    def test_get_flatpages_with_prefix(self):
        "The flatpage template tag retrives unregistered prefixed flatpages by default"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages '/location/' as location_flatpages %}"
                "{% for page in location_flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context())
        self.assertIn("A Nested Flatpage,", out)

    def test_get_flatpages_with_variable_prefix(self):
        "The prefix for the flatpage template tag can be a template variable"
        out = Template(
                "{% load flatpages %}"
                "{% get_flatpages location_prefix as location_flatpages %}"
                "{% for page in location_flatpages %}"
                "{{ page.title }},"
                "{% endfor %}"
            ).render(Context({
                'location_prefix': '/location/'
            }))
        self.assertIn("A Nested Flatpage,", out)

    def test_parsing_errors(self):
        "There are various ways that the flatpages template tag won't parse"
        render = lambda t: Template(t).render(Context())

        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages as %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages cheesecake flatpages %}")
        self.assertRaises(TemplateSyntaxError, render,
                          "{% load flatpages %}{% get_flatpages as flatpages asdf%}")

