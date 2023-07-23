from django.urls import path
from .views import YoutubeDownloadView

urlpatterns = [
	path('download_youtube_video/',YoutubeDownloadView.as_view())
]