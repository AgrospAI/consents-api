from rest_framework import permissions


class ConsentPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ["create", "delete_response"]:
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        if view.action == "destroy":
            return obj.solicitor == request.user

        if view.action == "destroy_response":
            return obj.dataset.owner == request.user

        return True
