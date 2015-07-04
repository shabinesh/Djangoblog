from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import *
from urllib import urlretrieve
import os
from django.conf import settings
# Create your tests here.

class ModelViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        image_path = "test.jpg"
        urlretrieve("http://ichef.bbci.co.uk/images/ic/480x270/p01lcnfr.jpg", os.path.join("/tmp/", image_path))
        self.user = User.objects.create_user('job', 'jon@test.com', 'pass')
        self.category = Category.objects.create(name='Travel')
        self.article = Article(
            title = "New Title",
            author = self.user,
            body = "Hello world, hope you are good as I am",
            category = self.category,
            publish = True,
        )
        self.article.hero = SimpleUploadedFile(name='test_image.jpg',
                                               content=open(os.path.join('/tmp',image_path), 'rb').read(), content_type='image/jpeg')
        self.article.save()
        
    def test_thumbnail_exists(self):
        resp = self.client.get(settings.MEDIA_URL+self.article.thumbnail.path)
        self.assertTrue(resp.status_code, 200)

    def test_random_articles_non_ajax(self):
        resp = self.client.get(reverse('random-articles'))
        self.assertEqual(resp.status_code, 400)

    def test_random_articles_ajax(self):
        resp = self.client.get(reverse('random-articles'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)

    # def test_top_article_context(self):
    #     resp = self.client.get(reverse('article-list'))
    #     self.assertIn('top_article' in resp.context)
