from django.db.models import F
from django.views.generic import DetailView, ListView

from .models import Article


class ArticleListView(ListView):
    template_name = "news/article_list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        return Article.objects.published().select_related("category", "author")


class ArticleDetailView(DetailView):
    template_name = "news/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.published().select_related("category", "author")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # F() expression: atomic increment, no read-modify-write race.
        Article.objects.filter(pk=obj.pk).update(view_count=F("view_count") + 1)
        return obj
