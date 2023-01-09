"""princetonpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.admin import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django_ses.views import SESEventWebhookView

from homepage.views import Home, JitsiPage
from meetings.views import meetings_list, meeting_page, next_meeting_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    re_path(r"^newsletter/", include("newsletter.urls")),
    path("signup/", TemplateView.as_view(template_name="signup.html")),
    path("", cache_page(120)(Home.as_view())),
    path("jitsi/", cache_page(120)(JitsiPage.as_view())),
    path("meetings/", meetings_list),
    path("meeting/<int:pk>/", meeting_page),
    path("meeting/", meeting_page),
    path("next-meeting/", next_meeting_page),
    url(
        r"^ses/event-webhook/$",
        SESEventWebhookView.as_view(),
        name="handle-event-webhook",
    ),
]

urlpatterns += staticfiles_urlpatterns()

# if settings.LOCAL_ENV:
#     NGINX_PAGES = settings.BASE_DIR / 'pages'
#     urlpatterns += re_path(r'^$', views.serve, kwargs={'path': 'index.html'}),
