from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from articles.models import Article
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest

class TopArticleMixin(ContextMixin):
    def get_top_article(self):
        a = Article.objects.order_by('?')[:1]
        if a:
            return {'top_article': a[0]}
        else:
            return {'top_article': None}

class ArticleListView(ListView, TopArticleMixin):
    model = Article
    paginate_by = 10
    context_object_name = "articles"

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context.update(self.get_top_article())
        return context

class JsonMixin:
    def convert_context_to_json(self, context):
        l = context[self.context_object_name]
        if type(l) is not list: l = [l]
        serialized = serializers.serialize('json', l)
        return serialized
    
    def render_to_response(self, context):
        return JsonResponse(self.convert_context_to_json(context), status=200, safe=False)

class ArticleListViewJson(JsonMixin, ArticleListView):
    pass
            
class RandomArticles(View):
    def get(self, request):
        if request.is_ajax():
            a = Article.objects.order_by('?')[:4]
            return JsonResponse(serializers.serialize('json', a, fields=('title', 'slug', 'thumbnail')), status=200, safe=False)
        else:
            return HttpResponseBadRequest()
        
class ArticleDetailView(DetailView, TopArticleMixin):
    model = Article
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context.update(self.get_top_article())
        return context

class ArticleDetailViewJson(JsonMixin, ArticleDetailView):
    pass
