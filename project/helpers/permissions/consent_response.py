from rest_framework import permissions


class ConsentResponsePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == "create":
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        if view.action == "destroy":
            return obj.consent.solicitor == request.user

        return True
