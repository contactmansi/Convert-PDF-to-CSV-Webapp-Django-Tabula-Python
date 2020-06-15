from dehaat_app import views
from django.urls import path

urlpatterns = [
    path('', views.input, name = "input"),
    path('download/<str:output_file_path>', views.download, name = "download")

]
