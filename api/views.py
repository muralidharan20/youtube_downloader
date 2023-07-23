from django.shortcuts import render
from .serializers import YoutubeSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# import youtube_dl
import yt_dlp as youtube_dl
import json
import re

# Create your views here.

class YoutubeDownloadView(APIView):
	def post(self,request,format=None):
		serializers = YoutubeSerializers(data=request.data)
		if serializers.is_valid():
			try:
				video_url = request.data['url']
				regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
				if not re.match(regex,video_url):
					return Response({"error":"Enter the valid URL"},status=status.HTTP_404_NOT_FOUND)
				ydl_opts = {}
				video_audio_streams = []
				ydl = youtube_dl.YoutubeDL()
				meta = ydl.extract_info(video_url, download=False)
				for m in meta['formats']:
					print(m)
					try:
						filesize = m['filesize']
						format_note = m['format_note']
						url = m['url']
						resolution = m['resolution']
						extension = m['ext']
						# if filesize is not None:
						# 	filesize = f'{round(int(filesize) / 1000000,2)} mb'
						if extension == "mp4" and filesize != None:
							filesize = f'{round(int(filesize) / 1000000,2)} mb'
							video_audio_streams.append({"format":format_note,"resolution":resolution,"extension":extension,"filesize":filesize,"url":url})
					except KeyError:
						pass
				seen_values = set()
				result = []
				for d in video_audio_streams:
				    value = d['resolution']
				    if value not in seen_values:
				        seen_values.add(value)
				        result.append(d)
				return Response(result,status=status.HTTP_200_OK)
			except youtube_dl.utils.DownloadError:
				return Response({"error":"URL invalid"},status=status.HTTP_404_NOT_FOUND)
		return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)