from fastapi import status
from payroll.utils.functions import get_error_message_dict

json_data = get_error_message_dict()


class BaseMessage:
    """Base class for error messages."""

    code: str
    text: str
    http_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class ErrorMessages:
    """Define specific error messages as subclasses of BaseMessage."""

    class ErrSM99999(BaseMessage):
        code = "ERR_SM_99999"
        text = json_data["SYSTEM_EXCEPTION"][code]
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    class InvalidInput(BaseMessage):
        code = "ERR_INVALID_INPUT"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_400_BAD_REQUEST

    class ResourceNotFound(BaseMessage):
        code = "ERR_RESOURCE_NOT_FOUND"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_404_NOT_FOUND

    class ResourceConflict(BaseMessage):
        code = "ERR_RESOURCE_CONFLICT"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_409_CONFLICT

    class ResourceAlreadyExists(BaseMessage):
        code = "ERR_RESOURCE_ALREADY_EXISTS"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_409_CONFLICT

    class ForbiddenAction(BaseMessage):
        code = "ERR_FORBIDDEN_ACTION"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_403_FORBIDDEN

    class UserWithEmailAlreadyExists(BaseMessage):
        code = "ERR_USER_WITH_EMAIL_ALREADY_EXISTS"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_409_CONFLICT

    class InvalidUsernameOrPassword(BaseMessage):
        code = "ERR_INVALID_USERNAME_OR_PASSWORD"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_401_UNAUTHORIZED

    class CannotCreateAdminUser(BaseMessage):
        code = "ERR_CANNOT_CREATE_ADMIN_USER"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_403_FORBIDDEN

    class ExistDependEmployee(BaseMessage):
        code = "ERR_EXIST_DEPEND_EMPLOYEE"
        text = json_data["APP_EXCEPTION"][code]
        http_status = status.HTTP_400_BAD_REQUEST