from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _

from .models import Project, Backlog
from .forms import ProjectCreationForm, ProjectEditionForm


class ProjectList(generic.ListView):
    template_name = "backlog/project_list.html"
    queryset = Project.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        return context
project_list = login_required(ProjectList.as_view())


class ProjectMixin(object):
    """
    Mixin to fetch a project by a view.
    """
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project,
                                         pk=kwargs['project_id'])
        return super(ProjectMixin, self).dispatch(request, *args, **kwargs)


class ProjectDetail(ProjectMixin, generic.DetailView):
    template_name = "backlog/project_detail.html"

    def get_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context
project_detail = login_required(ProjectDetail.as_view())


class ProjectCreate(generic.CreateView):
    template_name = "backlog/project_form.html"
    model = Project
    form_class = ProjectCreationForm

    def form_valid(self, form):
        super(ProjectCreate, self).form_valid(form)
        messages.success(self.request,
                         _("Your project was successfully created."))
        return redirect(reverse("project_list"))
project_create = login_required(ProjectCreate.as_view())


class ProjectEdit(ProjectMixin, generic.UpdateView):
    template_name = "backlog/project_form.html"
    form_class = ProjectEditionForm

    def get_object(self):
        return self.project

    def form_valid(self, form):
        project = form.save()
        messages.success(self.request,
                         _("Your project was successfully updated."))
        return redirect(project.get_absolute_url())
project_edit = login_required(ProjectEdit.as_view())


class ProjectDelete(ProjectMixin, generic.DeleteView):
    template_name = "backlog/project_confirm_delete.html"
    form_class = ProjectEditionForm

    def get_object(self):
        return self.project

    def delete(self, request, *args, **kwargs):
        self.project.delete()
        messages.success(request,
                         _("Project successfully deleted."))
        return redirect(reverse('project_list'))
project_delete = login_required(ProjectDelete.as_view())


class BacklogMixin(object):
    """
    Mixin to fetch a project and backlog by a view.
    """
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project,
                                         pk=kwargs['project_id'])
        self.backlog = get_object_or_404(Backlog,
                                         pk=kwargs['backlog_id'])
        return super(BacklogMixin, self).dispatch(request, *args, **kwargs)


class BacklogDetail(BacklogMixin, generic.DetailView):
    template_name = "backlog/backlog_detail.html"

    def get_object(self):
        return self.backlog

    def get_context_data(self, **kwargs):
        context = super(BacklogDetail, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['backlog'] = self.backlog
        return context
backlog_detail = login_required(BacklogDetail.as_view())