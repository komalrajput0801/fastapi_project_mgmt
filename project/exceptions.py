from fastapi import status

from core.exceptions import CustomHTTPException


class ProjectAlreadyExists(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Project with this name already exists"
