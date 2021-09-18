from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from . import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class TestApi(APIView):
    """ Test API """
    serializer_class = serializers.CustomSerializer

    def get(self, req, format=None):
        """ returns a list of object"""
        api_view = ['This is demo']
        return Response({

            'message': 'this is GET req',
            'api_view': api_view
        })

    def post(self, req):
        """ post req """
        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            msg = f'hello {name}'
            return Response({
                'message': msg
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, req, pk=None):
        """ updating object """
        return Response({
            'method': 'PUT'
        })

    def patch(self, req, pk=None):
        """ partial object object """
        return Response({
            'method': 'Patch'
        })

    def delete(self, req, pk=None):
        """ updating object """
        return Response({
            'method': 'delete'
        })


class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.CustomSerializer

    def list(self, req):
        """ GET for list of objects"""
        a_view = [

            'List one',

        ]
        return Response({

            'message': f'GET view set list {a_view}'
        })

    def create(self, req):
        """ create a new hello message"""

        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            return Response({
                'message': f' Hello {name}'
            })
        return Response(

            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, instance, validated_data):
        """ to handle the update of user account """
        if 'password' in validated_data:
            password = validated_data['password']
            validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ actual api to GET/POST/PUT/DELETE users"""

    serializer_class = serializers.ProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    """ creates user auth tokens """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserFeedViewSets(viewsets.ModelViewSet):
    """ CRUD on feed items """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.FeedSerializer
    queryset = models.UserFeed.objects.all()
    permission_classes = (

        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """ sets user profile to the logged in user """
        serializer.save(user_profile=self.request.user)
