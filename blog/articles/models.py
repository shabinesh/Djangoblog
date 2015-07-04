from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from cStringIO import StringIO # python3 it's io.StringIO
from django.conf import settings
import os

article_thumbs = 'article_images/'

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 20, unique=True)
    
class Article(models.Model):
    title = models.CharField(verbose_name="Title", max_length=60)
    author = models.ForeignKey(User, related_name='articles')
    body = models.TextField()
    category = models.ForeignKey(Category, related_name='articles')
    hero = models.ImageField(upload_to='article_images/')
    thumbnail = models.ImageField(upload_to=article_thumbs, null=True, blank=True)
    opt_img = models.ImageField(upload_to='article_images/', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    publish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def gen_thumbnail(self, outpath=None):
        if outpath is None:
            outpath = os.path.join(settings.MEDIA_ROOT, article_thumbs)
        if self.hero:
            try:
                inp = StringIO(self.hero.read())
                nam, ext = self.hero.name.split('.')
                outfile = "{}_thumb.{}".format(nam, 'png')
                img = Image.open(inp)
                img.thumbnail((200, 200))
                img.save(os.path.join(outpath, outfile), 'PNG')
                self.thumbnail = os.path.join(article_thumbs, outfile)
            except IOError, e:
                print("Failed to create thumbnail", e) #TODO: fix it with logging
                return

    def save(self):
        self.gen_thumbnail()
        super(Article, self).save()

    def __unicode__(self):
        return "{} - [{}]".format(self.title, 'Published' if self.publish else 'Unpublished')
