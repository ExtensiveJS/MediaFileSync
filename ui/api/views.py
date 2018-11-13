from MediaFileSync.models import Settings, Media
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SettingsSerializer, MediaSerializer


#class SettingsViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows Settings to be viewed or edited.
#    """
#    queryset = Settings.objects.all()
#    serializer_class = SettingsSerializer

class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    def post(self, request, pk):
        sett = Settings.objects.all()[:1].get()
        sett.radarr_enabled = request.POST.get('radarr_enabled')
        sett.radarr_path = request.POST.get('radarr_path')
        sett.radarr_apikey = request.POST.get('radarr_apikey')
        sett.sonarr_enabled = request.POST.get('sonarr_enabled')
        sett.sonarr_path = request.POST.get('sonarr_path')
        sett.lidarr_enabled = request.POST.get('lidarr_enabled')
        sett.lidarr_path = request.POST.get('lidarr_path')
        sett.save()
        return Response("Ok")

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    def post(self, request, pk):
        mid = request.POST.get('media_id')
        med = Media.objects.all()[:mid].get()
        med.media_source = request.POST.get('media_source')
        med.media_source_id = request.POST.get('media_source_id')
        med.media_lastUpd = request.POST.get('media_lastUpd')
        med.save()
        return Response("Ok")