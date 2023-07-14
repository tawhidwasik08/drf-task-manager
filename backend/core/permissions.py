from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permission class to check if the user has the 'admin' role.

    Inherits from BasePermission class.
    """

    def has_permission(self, request, view):
        """
        Check if the user has the 'admin' role.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view object.

        Returns:
            bool: True if the user has the 'admin' role, False otherwise.
        """
        return request.user.role == 'admin'
    
class IsManager(permissions.BasePermission):
    """
    Permission class to check if the user has the 'manager' role.

    Inherits from BasePermission class.
    """

    def has_permission(self, request, view):
        """
        Check if the user has the 'manager' role.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view object.

        Returns:
            bool: True if the user has the 'manager' role, False otherwise.
        """
        return request.user.role == 'manager'
    
class IsTeamMember(permissions.BasePermission):
    """
    Permission class to check if the user has the 'team_member' role.

    Inherits from BasePermission class.
    """

    def has_permission(self, request, view):
        """
        Check if the user has the 'team_member' role.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view object.

        Returns:
            bool: True if the user has the 'team_member' role, False otherwise.
        """
        return request.user.role == 'team_member'