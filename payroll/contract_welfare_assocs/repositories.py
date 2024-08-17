import logging

from payroll.contract_welfare_assocs.schemas import (
    CWAssocCreate,
    CWAssocUpdate,
    CWAssocBase,
)
from payroll.models import PayrollCWAssoc

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /cwassocs/{cwassoc_id}
def retrieve_cwassoc_by_id(*, db_session, cwassoc_id: int) -> PayrollCWAssoc:
    """Returns a cwassoc based on the given id."""
    return (
        db_session.query(PayrollCWAssoc).filter(PayrollCWAssoc.id == cwassoc_id).first()
    )


def retrieve_cwassoc_by_information(
    *, db_session, cwassoc_in: CWAssocBase
) -> PayrollCWAssoc:
    return (
        db_session.query(PayrollCWAssoc)
        .filter(
            PayrollCWAssoc.contract_id == cwassoc_in.contract_id
            and PayrollCWAssoc.welfare_id == cwassoc_in.welfare_id
        )
        .first()
    )


# GET /cwassocs
def retrieve_all_cwassocs(*, db_session) -> PayrollCWAssoc:
    """Returns all cwassocs."""
    query = db_session.query(PayrollCWAssoc)
    count = query.count()
    cwassocs = query.all()
    print(cwassocs)
    return {"count": count, "data": cwassocs}


# POST /cwassocs
def add_cwassoc(*, db_session, cwassoc_in: CWAssocCreate) -> PayrollCWAssoc:
    """Creates a new cwassoc."""
    cwassoc = PayrollCWAssoc(**cwassoc_in.model_dump())
    cwassoc.created_by = "admin"
    db_session.add(cwassoc)

    return cwassoc


# PUT /cwassocs/{cwassoc_id}
def modify_cwassoc(
    *, db_session, cwassoc_id: int, cwassoc_in: CWAssocUpdate
) -> PayrollCWAssoc:
    """Updates a cwassoc with the given data."""
    query = db_session.query(PayrollCWAssoc).filter(PayrollCWAssoc.id == cwassoc_id)
    update_data = cwassoc_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_cwassoc = query.first()

    return updated_cwassoc


# DELETE /cwassocs/{cwassoc_id}
def remove_cwassoc(*, db_session, cwassoc_id: int):
    """Deletes a cwassoc based on the given id."""
    query = db_session.query(PayrollCWAssoc).filter(PayrollCWAssoc.id == cwassoc_id)
    deleted_cwassoc = query.first()
    query.delete()

    return deleted_cwassoc
