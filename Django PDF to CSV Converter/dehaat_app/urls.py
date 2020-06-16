from dehaat_app import views
from django.urls import path

# Defines all the dehaat_app urlpatterns
# input: Routed from dehaat_first/urls.py --> Routes to input view
# download: Routed from output.html on the button click --> Routes to download view to send CSV file as HttpResponse
urlpatterns = [

    path('', views.input, name = "input"),
    path('download/<str:output_file_path>', views.download, name = "download")

]
