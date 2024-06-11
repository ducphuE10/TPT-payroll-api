from payroll.utils import get_error_message_dict

json_data = get_error_message_dict()


class BaseMessage:
    """Base class for error messages."""

    code: str
    text: str


class ErrorMessages:
    """Define specific error messages as subclasses of BaseMessage."""

    class ErrSM99999(BaseMessage):
        code = "ERR_SM_99999"
        text = json_data["SYSTEM_EXCEPTION"][code]

    class InvalidInput(BaseMessage):
        code = "ERR_INVALID_INPUT"
        text = json_data["APP_EXCEPTION"][code]

    class ResourceNotFound(BaseMessage):
        code = "ERR_RESOURCE_NOT_FOUND"
        text = json_data["APP_EXCEPTION"][code]

    class ResourceConflict(BaseMessage):
        code = "ERR_RESOURCE_CONFLICT"
        text = json_data["APP_EXCEPTION"][code]

    class ResourceAlreadyExists(BaseMessage):
        code = "ERR_RESOURCE_ALREADY_EXISTS"
        text = json_data["APP_EXCEPTION"][code]

    class ForbiddenAction(BaseMessage):
        code = "ERR_FORBIDDEN_ACTION"
        text = json_data["APP_EXCEPTION"][code]

    class UserWithEmailAlreadyExists(BaseMessage):
        code = "ERR_USER_WITH_EMAIL_ALREADY_EXISTS"
        text = json_data["APP_EXCEPTION"][code]

    class InvalidUsernameOrPassword(BaseMessage):
        code = "ERR_INVALID_USERNAME_OR_PASSWORD"
        text = json_data["APP_EXCEPTION"][code]

    class CannotCreateAdminUser(BaseMessage):
        code = "ERR_CANNOT_CREATE_ADMIN_USER"
        text = json_data["APP_EXCEPTION"][code]
