from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ allow update own profiles """

    def has_object_permission(self, request, view, obj):
        """ checks user permission """

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """ Allows users to update their own status """

    def has_object_permission(self, request, view, obj):
        """ check if user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
