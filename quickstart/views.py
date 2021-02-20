from django.contrib.auth.models import User
from rest_framework import generics, renderers
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from quickstart.models import Snippet
from quickstart.permissions import IsOwnerOrReadOnly
from quickstart.serializers import UserSerializer, SnippetSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse(UserList.name, request=request, format=format),
        'snippets': reverse(SnippetList.name, request=request, format=format),
    })


class SnippetHighlight(generics.GenericAPIView):
    name = 'snippet-highlight'
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs) -> Response:
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserList(generics.ListAPIView):
    name = 'user-list'
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveAPIView):
    name = 'user-detail'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SnippetList(generics.ListCreateAPIView):
    """
    List all code snippets, or create a new snippet.
    """
    name = 'snippet-list'
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve update or delete a code snippet
    """
    name = 'snippet-detail'
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
