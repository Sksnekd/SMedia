from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import UserRegistrationView, UserImageViewSet, PostDetailView
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'UserImage', UserImageViewSet)


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='user-profile-detail'),
    path('profile/', views.ProfileListAPIView.as_view(), name='profile-list'),
    path('api/', include(router.urls)),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)