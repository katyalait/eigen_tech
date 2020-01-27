from django.urls import path
from .views import FilteredWordView, UploadFileView

urlpatterns = [
    path('', FilteredWordView.as_view(), name='home'),
    path('document/', UploadFileView.as_view(), name='upload_document'),
]
