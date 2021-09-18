from rest_framework import serializers
from . import models


class CustomSerializer(serializers.Serializer):
    """ serializes a name field for testing our api Views"""
    name = serializers.CharField(max_length=255)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ProfileSerializer(serializers.ModelSerializer):
    """ serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name', 'id', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """ overrides the create function """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserFeed
        fields = ('id', 'user_profile', 'status_text', 'create_on')
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }
