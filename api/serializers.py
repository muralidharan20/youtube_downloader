from rest_framework import serializers

class YoutubeSerializers(serializers.Serializer):
	url = serializers.URLField()
	class Meta:
		fiels = ['url']