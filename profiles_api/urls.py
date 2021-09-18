from django.conf.urls import url, include
from profiles_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'hello-list', views.HelloViewSet, base_name='list')
router.register(r'profile', views.UserProfileViewSet, base_name='profile')
router.register(r'feed', views.UserFeedViewSets, base_name='feed')

urlpatterns = [

    url(r'hello/', views.TestApi.as_view()),
    url(r'login/', views.UserLoginApiView.as_view(), name="login"),
    url(r'', include(router.urls))
]
