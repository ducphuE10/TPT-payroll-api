from fastapi import Depends
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from jose.exceptions import JWKError
from payroll.config import settings
import logging
from typing import Annotated
from fastapi.security import APIKeyHeader
from payroll.models import PayrollEmployee
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


api_key_header = APIKeyHeader(name="Authorization")
TokenDep = Annotated[str, Depends(api_key_header)]


def get_user_email(authorization, **kwargs):
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        logger.exception(
            f"Malformed authorization header. Scheme: {scheme} Param: {param} Authorization: {authorization}"
        )
        return

    token = authorization.split()[1]

    try:
        data = jwt.decode(token, settings.SECRET_KEY.get_secret_value())
    except (JWKError, JWTError):
        raise Exception("Invalid token")
    return data["email"]


def get_error_message_dict():
    return {
        "SYSTEM_EXCEPTION": {"ERR_SM_99999": "Lỗi hệ thống, vui lòng thử lại sau."},
        "APP_EXCEPTION": {
            "ERR_INVALID_INPUT": "Dữ liệu đầu vào không hợp lệ.",
            "ERR_RESOURCE_NOT_FOUND": "Không tìm thấy tài nguyên.",
            "ERR_RESOURCE_CONFLICT": "Xung đột tài nguyên.",
            "ERR_RESOURCE_ALREADY_EXISTS": "Tài nguyên đã tồn tại.",
            "ERR_FORBIDDEN_ACTION": "Hành động bị cấm.",
            "ERR_USER_WITH_EMAIL_ALREADY_EXISTS": "Người dùng với email đã tồn tại.",
            "ERR_INVALID_USERNAME_OR_PASSWORD": "Tên đăng nhập hoặc mật khẩu không hợp lệ.",
            "ERR_CANNOT_CREATE_ADMIN_USER": "Không thể tạo người dùng quản trị.",
            "ERR_EXIST_DEPEND_EMPLOYEE": "Không thể xóa do tồn tại các nhân viên liên quan",
        },
    }

def check_depend_employee(db_session: Session, *, department_id: int = None, position_id: int = None) -> bool:
    if department_id is not None:
        print("ddddddddddddddd", db_session.query(PayrollEmployee).filter(PayrollEmployee.department_id == department_id).count())
        return db_session.query(PayrollEmployee).filter(PayrollEmployee.department_id == department_id).count() > 0
    if position_id is not None:
        print("ccccccccccccccc", db_session.query(PayrollEmployee).filter(PayrollEmployee.position_id == position_id).count())
        return db_session.query(PayrollEmployee).filter(PayrollEmployee.position_id == position_id).count() > 0
    return False