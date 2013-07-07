from django.conf.urls import url, patterns

from .views import (home_view, project_list, project_detail,
                    backlog_list, backlog_detail, story_list, story_detail,
                    project_move_backlog, org_move_backlog,
                    move_story, org_list, org_detail)

urlpatterns = patterns(
    '',

    url(r'^api-token-auth/',
        'rest_framework.authtoken.views.obtain_auth_token'),

    # views
    url(r'^projects/$',
        project_list, name="api_project_list"),

    url(r'^projects/(?P<project_id>[\w]+)/$',
        project_detail, name="api_project_detail"),

    url(r'^organizations/$',
        org_list, name="api_org_list"),

    url(r'^organizations/(?P<org_id>[\w]+)/$',
        org_detail, name="api_org_detail"),

    url(r'^projects/(?P<project_id>[\w]+)/backlogs/$',
        backlog_list, name="api_backlog_list"),

    url(r'^projects/(?P<project_id>[\w]+)/backlogs/(?P<backlog_id>[\w]+)/$',
        backlog_detail, name="api_backlog_detail"),

    url(r'^projects/(?P<project_id>[\w]+)/backlogs/'
        r'(?P<backlog_id>[\w]+)/stories/$',
        story_list, name="api_stories"),

    url(r'^projects/(?P<project_id>[\w]+)/backlogs/(?P<backlog_id>[\w]+)/'
        r'stories/(?P<story_id>[\w]+)/$',
        story_detail, name="api_story_detail"),

    url(r'^$', home_view, name="api_home"),

    url(r'/_move_story/$',
        move_story, name="api_move_story"),

    url(r'^projects/(?P<project_id>[\w]+)/_order_backlog/$',
        project_move_backlog, name="api_project_move_backlog"),

    url(r'^orgs/(?P<org_id>[\w]+)/_order_backlog/$',
        org_move_backlog, name="api_org_move_backlog"),
)
