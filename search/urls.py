from django.contrib import admin
from django.urls import path, include
from . import views
from . import api

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    # path('api/files/', views.FileUploadView.as_view()),
    # path('api/all-files/', views.all_files),
    path('search/', views.search_view, name="search"),

    # API #
    # path('api/files/', api.file_list, name='file_list'),
    # path('api/files/<int:id>', api.file, name='file'),


    # class base API #
    path('api/v2/files/', api.FileListAPI.as_view(), name='FileListAPI'),
    path('api/v2/files/add', api.BookAddAPI.as_view(), name='BookAddAPI'),
    path('api/v2/QA/', api.GenericAPIView.as_view(), name='GenericAPIView'),
    path('api/v2/files/<int:id>', api.FileRetrieveAPI.as_view(), name='FileRetrieveAPI'),
    # path('api/v2/files/<int:id>', api.FileOperationAPI.as_view(), name='FileOperationAPI'),

]
