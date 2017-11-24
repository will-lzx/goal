"""goal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from weixin.views import *

urlpatterns = [
    url(r'^wx/$', wx, name='wx'),
    url(r'^create1/$', create1, name='create1'),
    url(r'^create2/(?P<goal_type>.+)/(?P<open_id>.+)/$', create2, name='create2'),
    url(r'^create3/(?P<goal_id>.+)/(?P<open_id>.+)/$', create3, name='create3'),

    url(r'^createsuccess/$', createsuccess, name='createsuccess'),


    url(r'^history/$', history, name='history'),
    url(r'^others/$', others, name='others'),
    url(r'^ranking/$', ranking, name='ranking'),

    url(r'^save_goal/$', save_goal, name='save_goal'),
    url(r'^goaldetail/(?P<goal_id>.+)/$', goaldetail, name='goaldetail'),

    url(r'^operate_audience/$', operate_audience, name='operate_audience'),

    url(r'^goinglog/(?P<goal_id>.+)/$', goinglog, name='goinglog'),
    url(r'^goal_action/$', goal_action, name='goal_action'),
    url(r'^save_history/$', save_history, name='save_history'),

    url(r'^image/(?P<history_id>.+)/(?P<index>.+)/$', pil_image, name="image"),

]
