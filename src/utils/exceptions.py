class UserRoleActionError(Exception):
    """Exception raised when there is an error adding a role to a user."""

    def __init__(self, message: str = "Failed to add role to user.") -> None:
        self.message = message
        super().__init__(self.message)


class RoleNotAssigned(Exception):
    """Exception raised when role not assigned to user"""

    def __init__(self, message: str = "Role not assigned to user.") -> None:
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    """Exception raised when entity not found."""

    def __init__(self, message: str = "Entity not found.") -> None:
        self.message = message
        super().__init__(self.message)


class AlreadyExistError(Exception):
    """Exception raised when entity already exist"""

    def __init__(self, message: str = "Entity is exist.") -> None:
        self.message = message
        super().__init__(self.message)


class PermissionDeniedException(Exception):
    """Exception raised when your user don't have permission"""

    def __init__(
        self,
        message: str = "You don't have permission to access this resource.",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class UnauthorisedException(Exception):
    """Exception raised when you not authorized to resource"""

    def __init__(
        self,
        message: str = "Unauthorized action.",
    ) -> None:
        self.message = message
        super().__init__(self.message)
