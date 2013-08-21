
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http.response import (HttpResponseForbidden)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views import generic


from rest_framework.response import Response
from rest_framework.decorators import (api_view, throttle_classes,
                                       parser_classes)
from rest_framework.parsers import JSONParser

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


from ..backlog.views import NoCacheMixin

from models import (StoryMap, Story, Theme, Phase)


class StoryMapMixin(NoCacheMixin):
    admin_only = False
    """
    Mixin to fetch a organization by a view.
    """
    def dispatch(self, request, *args, **kwargs):
        self.story_map = get_object_or_404(StoryMap,
                                           pk=kwargs['storymap_id'])

        if self.admin_only and not self.story_map.can_admin(request.user):
            if self.story_map.can_read(request.user):
                return HttpResponseForbidden(_("Not authorized"))
            else:
                raise Http404
        self.request = request
        self.pre_dispatch()
        return super(StoryMapMixin, self).dispatch(request, *args, **kwargs)

    def pre_dispatch(self):
        pass


class StoryMapDetail(StoryMapMixin, generic.DetailView):
    template_name = "storymap/storymap_detail.html"

    def get_object(self):
        return self.story_map

    def get_context_data(self, **kwargs):
        context = super(StoryMapDetail, self).get_context_data(**kwargs)
        context['storymap'] = self.story_map
        context['themes'] = self.story_map.themes.all()
        context['phases'] = self.story_map.phases.all()
        return context
storymap_detail = login_required(StoryMapDetail.as_view())


def get_or_errors(dic, value, errors=[]):
    if value not in dic:
        errors.append("Missing value '{0}' in content".format(value))
        return None
    return dic.get(value)


TARGETS = {
    'story': (Story, False),
    'theme': (Theme, True),
    'phase': (Phase, True),
}

CREATE = "create"
DELETE = "delete"
UPDATE = "update"

@api_view(["POST"])
@parser_classes((JSONParser,))
@transaction.commit_on_success
def story_map_action(request, story_map_id):
    story_map = get_object_or_404(StoryMap, pk=story_map_id)
    if not story_map.can_read(request.user):
        if story_map.can_write(request.user):
            return Response("You are not admin of this story map", status=403)
        # verify access rights on story project
        raise Http404
    errors = []
    target = get_or_errors(request.DATA, 'target', errors)
    action = get_or_errors(request.DATA, 'action', errors)
    content = request.DATA.get('content', dict())
    target_id = request.DATA.get('id', None)
    model_class = TARGETS[target][0]
    if TARGETS[target][1]:
        content['story_map'] = story_map
    if errors:
        return Response({
            'errors': errors
        }, content_type="application/json", status=400)
    try:
        if action == CREATE:
            obj = model_class.objects.create(**content)
            target_id = obj.pk
        elif action == UPDATE:
            obj = model_class.objects.get(pk=target_id)
            for k, v in content.items():
                setattr(obj, k, v)
            obj.save()
        elif action == DELETE:
            obj = model_class.objects.get(pk=target_id)
            obj.delete()
    except ObjectDoesNotExist:
        return Response({
            'errors': [
                'Unable to find {0} with id {1}'.format(target, target_id)
            ]
        }, content_type="application/json", status=400)
    return Response({
        'id': target_id,
        'ok': True
    }, content_type="application/json", status=200)