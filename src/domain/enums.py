from enum import StrEnum

class PermissionValues(StrEnum):
    """
    Permission values for user roles.
    """
    read = "read"
    write = "write"
    update = "update"
    delete = "delete"
