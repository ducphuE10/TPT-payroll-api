# from typing import Union

# from payroll.attendances.schemas import AttendanceCreate, AttendanceUpdate
# from payroll.exception.app_exception import AppException
# from payroll.exception.error_message import ErrorMessages


# # validate that only one of 'work' or 'leave' attributes can be set, not both
# def check_work_or_leave_set(
#     obj: Union["AttendanceUpdate", "AttendanceCreate"],
# ) -> Union["AttendanceUpdate", "AttendanceCreate"]:
#     work_set = any([obj.work_hours is not None, obj.overtime is not None])
#     leave_set = [
#         obj.holiday is not None,
#         obj.afm is not None,
#         obj.wait4work is not None,
#     ]

#     if work_set and any(leave_set):
#         """Only one of 'work' or 'leave' attributes can be set, not both."""
#         raise AppException(ErrorMessages.WorkLeaveState())
#     if not work_set and not any(leave_set):
#         """At least one of 'work' or 'leave' attributes must be set."""
#         raise AppException(ErrorMessages.WorkLeaveState())
#     if sum(leave_set) > 1:
#         """Only one attribute within 'leave' set can be set at a time."""
#         raise AppException(ErrorMessages.WorkLeaveState())

#     return obj
