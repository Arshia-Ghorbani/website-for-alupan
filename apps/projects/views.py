from django.views.generic import DetailView, ListView

from .models import Project


class ProjectListView(ListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        qs = Project.objects.published().select_related("sector")
        sector = self.request.GET.get("sector")
        if sector:
            qs = qs.filter(sector__slug=sector)
        return qs


class ProjectDetailView(DetailView):
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return (
            Project.objects.published()
            .select_related("sector")
            .prefetch_related("images", "systems_used")
        )
