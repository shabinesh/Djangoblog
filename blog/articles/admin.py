from django.contrib import admin
from articles.models import Article, Category
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    #exclude = ('thumbnail',)
    prepopulated_fields = {"slug": ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
