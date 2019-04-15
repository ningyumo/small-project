from django.urls import path
from . import views

app_name = "file_upload"
urlpatterns = [
    path("", views.FileListView.as_view(), name="file_list"),
    path("form_upload/", views.FileFormView.as_view(), name="form_upload"),
    path("model_form_upload/", views.FileCreateView.as_view(), name="model_form_upload"),
    path("delete_file/<int:pk>/", views.FileDeleteView.as_view(), name="delete_file"),
    path("download/<file_path>/", views.file_download, name="file_download"),
]