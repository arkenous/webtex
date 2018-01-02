from django.conf.urls import url
from editor import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^read_file_list/', views.read_file_list, name='read_file_list'),
    url(r'^compile/', views.compile_content, name='compile_content'),
    url(r'^download_files/', views.download_files, name='download_files'),
    url(r'^upload_file/', views.upload_file, name='upload_file'),
    url(r'^delete_file/', views.delete_file, name='delete_file')
]
