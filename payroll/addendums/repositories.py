import logging

from payroll.addendums.schemas import AddendumCreate, AddendumUpdate
from payroll.models import PayrollAddendum

log = logging.getLogger(__name__)


def retrieve_addendum_by_id(*, db_session, addendum_id: int) -> PayrollAddendum:
    """Returns a addendum based on the given id."""
    return (
        db_session.query(PayrollAddendum)
        .filter(PayrollAddendum.id == addendum_id)
        .first()
    )


def retrieve_addendum_by_code(*, db_session, addendum_code: str) -> PayrollAddendum:
    """Returns a addendum based on the given code."""
    return (
        db_session.query(PayrollAddendum)
        .filter(PayrollAddendum.code == addendum_code)
        .first()
    )


# def retrieve_employee_active_contract(
#     *, db_session, employee_code: str, current_date: date
# ):
#     return (
#         db_session.query(PayrollAddendum)
#         .filter(
#             and_(
#                 PayrollAddendum.employee_code == employee_code,
#                 PayrollAddendum.start_date <= current_date,
#                 (PayrollAddendum.end_date >= current_date)
#                 | (PayrollAddendum.end_date.is_(None)),
#                 PayrollAddendum.is_current == True,  # noqa
#                 PayrollAddendum.status == "ACTIVE",
#             )
#         )
#         .first()
#     )


# def retrieve_active_contracts(*, db_session, current_date: date):
#     return (
#         db_session.query(PayrollAddendum)
#         .filter(
#             and_(
#                 PayrollAddendum.start_date <= current_date,
#                 (PayrollAddendum.end_date >= current_date)
#                 | (PayrollAddendum.end_date.is_(None)),
#                 PayrollAddendum.is_current == True,  # noqa
#                 PayrollAddendum.status == Status.ACTIVE,
#             )
#         )
#         .all()
#     )


# def retrieve_contract_by_employee_and_period(
#     *, db_session, employee_code: str, from_date: date, to_date: date
# ):
#     return (
#         db_session.query(PayrollAddendum)
#         .filter(
#             PayrollAddendum.employee_code == employee_code,
#             and_(
#                 PayrollAddendum.start_date <= to_date,
#                 or_(
#                     PayrollAddendum.end_date.is_(None),
#                     PayrollAddendum.end_date >= from_date,
#                 ),
#             ),
#         )
#         .first()
#     )


def retrieve_all_addendums(*, db_session) -> PayrollAddendum:
    query = db_session.query(PayrollAddendum)
    count = query.count()
    addendums = query.all()

    return {"count": count, "data": addendums}


def add_addendum(*, db_session, addendum_in: AddendumCreate) -> PayrollAddendum:
    """Creates a new contract."""
    addendum = PayrollAddendum(**addendum_in.model_dump())
    addendum.created_by = "admin"
    db_session.add(addendum)

    return addendum


def modify_addendum(*, db_session, addendum_id: int, addendum_in: AddendumUpdate):
    """Updates a contract with the given data."""
    update_data = addendum_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollAddendum).filter(PayrollAddendum.id == addendum_id)
    query.update(update_data, synchronize_session=False)
    updated_addendum = query.first()

    return updated_addendum


def remove_addendum(*, db_session, addendum_id: int) -> PayrollAddendum:
    """Deletes a contract based on the given id."""
    query = db_session.query(PayrollAddendum).filter(PayrollAddendum.id == addendum_id)
    delete_addendum = query.first()
    query.delete()

    return delete_addendum


def get_addendum_template(*, db_session, addendum_id: int) -> PayrollAddendum:
    """Returns a contract template based on the given code."""
    template = db_session.query(PayrollAddendum).filter_by(id=addendum_id).first()

    return template
