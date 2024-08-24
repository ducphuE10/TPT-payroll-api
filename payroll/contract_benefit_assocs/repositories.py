import logging

from payroll.contract_benefit_assocs.schemas import (
    CBAssocCreate,
    CBAssocUpdate,
    CBAssocBase,
)
from payroll.models import PayrollCBAssoc

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /cbassocs/{cbassoc_id}
def retrieve_cbassoc_by_id(*, db_session, cbassoc_id: int) -> PayrollCBAssoc:
    """Returns a cbassoc based on the given id."""
    return (
        db_session.query(PayrollCBAssoc).filter(PayrollCBAssoc.id == cbassoc_id).first()
    )


def retrieve_cbassoc_by_information(
    *, db_session, cbassoc_in: CBAssocBase
) -> PayrollCBAssoc:
    return (
        db_session.query(PayrollCBAssoc)
        .filter(
            PayrollCBAssoc.contract_id == cbassoc_in.contract_id
            and PayrollCBAssoc.benefit_id == cbassoc_in.benefit_id
        )
        .first()
    )


# GET /cbassocs
def retrieve_all_cbassocs(*, db_session) -> PayrollCBAssoc:
    """Returns all cbassocs."""
    query = db_session.query(PayrollCBAssoc)
    count = query.count()
    cbassocs = query.all()
    print(cbassocs)
    return {"count": count, "data": cbassocs}


def retrieve_cbassocs_by_contract_id(*, db_session, contract_id: int) -> PayrollCBAssoc:
    """Returns all schedule_details of a schedule."""
    query = db_session.query(PayrollCBAssoc).filter(
        PayrollCBAssoc.contract_id == contract_id,
    )
    count = query.count()
    cbassocs = query.all()

    return {"count": count, "data": cbassocs}


# POST /cbassocs
def add_cbassoc(*, db_session, cbassoc_in: CBAssocCreate) -> PayrollCBAssoc:
    """Creates a new cbassoc."""
    cbassoc = PayrollCBAssoc(**cbassoc_in.model_dump())
    cbassoc.created_by = "admin"
    db_session.add(cbassoc)

    return cbassoc


def add_cbassoc_with_contract_id(
    *, db_session, cbassoc_in: CBAssocCreate, contract_id: int
) -> PayrollCBAssoc:
    """Creates a new cbassoc."""
    cbassoc = PayrollCBAssoc(**cbassoc_in.model_dump())
    cbassoc.created_by = "admin"
    cbassoc.contract_id = contract_id
    db_session.add(cbassoc)

    return cbassoc


# PUT /cbassocs/{cbassoc_id}
def modify_cbassoc(
    *, db_session, cbassoc_id: int, cbassoc_in: CBAssocUpdate
) -> PayrollCBAssoc:
    """Updates a cbassoc with the given data."""
    query = db_session.query(PayrollCBAssoc).filter(PayrollCBAssoc.id == cbassoc_id)
    update_data = cbassoc_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_cbassoc = query.first()

    return updated_cbassoc


# DELETE /cbassocs/{cbassoc_id}
def remove_cbassoc(*, db_session, cbassoc_id: int):
    """Deletes a cbassoc based on the given id."""
    query = db_session.query(PayrollCBAssoc).filter(PayrollCBAssoc.id == cbassoc_id)
    deleted_cbassoc = query.first()
    query.delete()

    return deleted_cbassoc
