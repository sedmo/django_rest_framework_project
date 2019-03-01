from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers, viewsets

# we're going to replace the SnippetList, SnippetDetail and SnippetHighlight
#  view classes. We can remove the three views, and again replace them with 
# a single class.
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



# Creating an endpoint for the root of our API
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

# Refactoring to use ViewSets
#  let's refactor our UserList and UserDetail views into a single UserViewSet. 
# We can remove the two views, and replace them with a single class:

from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



# * Old way with just mixins and generic api view
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from django.http import Http404 
# from rest_framework.views import APIView
# from rest_framework import mixins
# from rest_framework import generics

# # Django’s generic views... were developed as a shortcut for common usage patterns... 
# # They take certain common idioms and patterns found in view development and
# #  abstract them so that you can quickly write common views of data without having to repeat yourself.
# class SnippetList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request. *args, **kwargs) 

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)



# # Old way without mixins
# # //from rest_framework.response import Response
# # //from rest_framework import status
# # * One of the big wins of using class-based views 
# # * is that it allows us to easily compose reusable 
# # * bits of behaviour
# # class SnippetList(APIView):
# #     """
# #     List all snippets, or create a new snippet.
# #     """
# #     def get(self, request, format=None):
# #         snippets = Snippet.objects.all()
# #         serializer = SnippetSerializer(snippets, many=True)
# #         return Response(serializer.data)

# #     def post(self, request, format=None):
# #         serializer = SnippetSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # class SnippetDetail(APIView):
# #     """
# #     Retrieve, update or delete a snippet instance.
# #     """
# #     def get_object(self, pk):
# #         try:
# #             return Snippet.objects.get(pk=pk)
# #         except Snippet.DoesNotExist:
# #             raise Http404

# #     def get(self, request, pk, format=None):
# #         snippet = self.get_object(pk)
# #         serializer = SnippetSerializer(snippet)
# #         return Response(serializer.data)

# #     def put(self, request, pk, format=None):
# #         snippet = self.get_object(pk)
# #         serializer = SnippetSerializer(snippet, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #     def delete(self, request, pk, format=None):
# #         snippet = self.get_object(pk)
# #         snippet.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT

# # from django.views.decorators.csrf import csrf_exempt
# # from rest_framework import status
# # from rest_framework.decorators import api_view
# # from rest_framework.parsers import JSONParser
# # from rest_framework.renderers import JSONRenderer
# # from rest_framework.response import Response

# # from snippets.models import Snippet
# # from snippets.serializers import SnippetSerializer

# # # * Requests and responses handle content type for us

# # # @api_view = decorator for working with function based views.
# # # use @api_view to make sure you receive Request instances
# # # in your view, and adding context to Response objects
# # # so that content negotiation can be performed.Also handles
# # # errors from parsing bad input in the request.data
# # @api_view(['GET', 'POST']) # By default it is only GET
# # def snippet_list(request, format=None):
# #     """

# #     List all code snippets, or create a new snippet.

# #     """
# #     if request.method == 'GET':
# #         snippets = Snippet.objects.all()
# #         serializer = SnippetSerializer(snippets, many=True)
# #         return Response(serializer.data)

# #     elif request.method == 'POST':
# #         serializer = SnippetSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data,
# #             status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, 
# #         status=status.HTTP_400_BAD_REQUEST)
        
# # @api_view(['GET', 'PUT', 'DELETE'])
# # def snippet_detail(request, pk, format=None):
# #     """
# #     Retrieve, update or delete a code snippet.

# #     """
# #     try:
# #         snippet = Snippet.objects.get(pk=pk)
# #     except Snippet.DoesNotExist:
# #         return Response(status=status.HTTP_404_NOT_FOUND)

# #     if request.method == 'GET':
# #         serializer = SnippetSerializer(snippet)
# #         return Response(serializer.data)

# #     elif request.method == 'PUT':
# #         # ! No longer necessary with response object
# #         # //data = JSONParser().parse(request)
# #         # * SnippetSerializer with 2 args = update
# #         serializer = SnippetSerializer(snippet, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #     elif request.method == 'DELETE':
# #         snippet.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)

# # Using read only views for user representation
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
# # Creating an endpoint for the highlighted snippets
# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)
# Using generic class-based views
# Using the mixin classes we've rewritten the views to use slightly less code than before, 
# but we can go one step further. REST framework provides a set of already mixed-in generic 
# views that we can use to trim down our views.py module even more.
# class SnippetList(generics.ListCreateAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     # # Associating Snippets with Users
#     # .perform_create() allows us to modify how the instance save is managed, and handle 
#     # any information that is implicit in the incoming request or requested URL.
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                       IsOwnerOrReadOnly,)
# #     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer