"""bugbo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from bugboapi.views import register_user, login_user, BugTypeView, BugView, BugStatusView, TagView, BugPriorityView, ProjectView, ProjectUserView, BugTagView, EmployeeView, UserTypeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bugtypes', BugTypeView, 'bugtype')
router.register(r'bugs', BugView, 'bug')
router.register(r'bugstatuses', BugStatusView, 'bugstatus')
router.register(r'tags', TagView, 'tag')
router.register(r'bugpriorities', BugPriorityView, 'bugpriority')
router.register(r'projects', ProjectView, 'project')
router.register(r'projectusers', ProjectUserView, 'projectuser')
router.register(r'bugtags', BugTagView, 'bugtag')
router.register(r'employees', EmployeeView, 'employee')
router.register(r'usertypes', UserTypeView, 'usertype')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
