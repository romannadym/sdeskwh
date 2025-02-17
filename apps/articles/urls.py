from django.urls import path
from articles.views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', ArticleListView, name = 'articles'),
    path('<int:pk>/', ArticleDetailView, name = 'article-detail'),
]
