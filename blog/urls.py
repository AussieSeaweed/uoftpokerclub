from django.urls import path

from .views import CategoryDetailView, PostDetailView, CorrespondenceCreateView, CorrespondenceCreateDoneView

urlpatterns = [
    path("categories/", CategoryDetailView.as_view(), name="blog-root"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("correspondences/create", CorrespondenceCreateView.as_view(), name="correspondence-create"),
    path("correspondences/create/done", CorrespondenceCreateDoneView.as_view(), name="correspondence-create-done"),
]
