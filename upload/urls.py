from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
     path('admin/', admin.site.urls),
    path('', views.FileUpload, name='upload_file'),
    path('download/', views.DownloadFile, name='download_output'),
    path('plot/', views.ShowPlot, name='show_plot'),
    ]

