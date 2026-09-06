from django.views.generic import DetailView, ListView

from .models import System, SystemCategory


class SystemListView(ListView):
    template_name = "systems/system_list.html"
    context_object_name = "systems"
    paginate_by = 12

    def get_queryset(self):
        return (
            System.objects.published()
            .select_related("category")
            .order_by("category__sort_order", "sort_order")
        )


class SystemCategoryView(SystemListView):
    template_name = "systems/system_category.html"

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs["slug"])


class SystemDetailView(DetailView):
    template_name = "systems/system_detail.html"
    context_object_name = "system"

    def get_queryset(self):
        return System.objects.published().select_related("category").prefetch_related("images")
