from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.permissions import AllowAny
from ext_news.serializers import NewsSerializer, SetNewsSerializer
from ext_news.models import News
from utils.decorators import permission


class Post(ListCreateAPIView):
    queryset = News.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = NewsSerializer


class PostUpd(APIView):
    queryset = News.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = NewsSerializer

    def get_object(self, id):
        try:
            return News.objects.get(id=id)
        except News.DoesNotExist:
            raise Http404

    def get(self, request, id):
        news = self.get_object(id)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, id):
        news = self.get_object(id)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        news = self.get_object(id)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ModeratorCheckNewsAPIView(APIView):
    queryset = News.objects.none()
    permission_classes = [AllowAny, ]
    serializer_class = SetNewsSerializer
    
    def post(self, request, *args, **kwargs):
        news = News.objects.get(id=request.data.get('id'))
        serializer = self.serializer_class(news, data = request.data)
        check = request.data.get('status')
        news.is_checked = check
        news.save()
        if serializer.is_valid():
            return Response(data={"is_checked": "{}".format(str(check))}, status=status.HTTP_200_OK)
        else:
            return Response(data={"News": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
