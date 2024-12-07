import logging
from fastapi import File, HTTPException, UploadFile, status
import pandas as pd
from io import BytesIO
from pydantic import ValidationError

from payroll.dependants.constant import (
    DTYPES_MAP,
    ID_DOC_TYPE_MAPPING,
    IMPORT_DEPENDANTS_EXCEL_MAP,
    RELATIONSHIP_MAPPING,
)
from payroll.dependants.repositories import (
    add_dependant,
    modify_dependant,
    remove_dependant,
    retrieve_all_dependants,
    retrieve_dependant_by_code,
    retrieve_dependant_by_id,
    search_dependants_by_partial_name,
    retrieve_all_dependants_by_employee_id,
)
from payroll.employees.services import get_employee_by_code
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollDependant
from payroll.dependants.schemas import (
    DependantCreate,
    DependantImport,
    DependantUpdate,
)
from payroll.utils.functions import (
    check_exist_person_by_mst,
)

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_dependant_by_id(*, db_session, dependant_id: int):
    """Check if dependant exists in the database."""
    return bool(
        retrieve_dependant_by_id(db_session=db_session, dependant_id=dependant_id)
    )


def check_exist_dependant_by_code(*, db_session, dependant_code: str):
    """Check if dependant exists in the database."""
    return bool(
        retrieve_dependant_by_code(db_session=db_session, dependant_code=dependant_code)
    )


def validate_create_dependant(*, db_session, dependant_in: DependantCreate):
    if check_exist_dependant_by_code(
        db_session=db_session, dependant_code=dependant_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "dependant")

    if check_exist_person_by_mst(db_session=db_session, mst=dependant_in.mst):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")
    return True


def validate_update_dependant(
    *, db_session, dependant_id: int, dependant_in: DependantUpdate
):
    if dependant_in.mst and check_exist_person_by_mst(
        db_session=db_session,
        mst=dependant_in.mst,
        exclude_id=dependant_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")
    return True


# GET /dependants/{dependant_id}
def get_dependant_by_id(*, db_session, dependant_id: int):
    """Returns a dependant based on the given id."""
    if not check_exist_dependant_by_id(
        db_session=db_session, dependant_id=dependant_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    return retrieve_dependant_by_id(db_session=db_session, dependant_id=dependant_id)


# GET /dependants
def get_all_dependants(*, db_session):
    """Returns all dependants."""
    list_dependants = retrieve_all_dependants(db_session=db_session)
    if not list_dependants["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    return list_dependants


def get_all_dependants_by_employee_id(*, db_session, employee_id: int):
    """Returns all dependants."""
    list_dependants = retrieve_all_dependants_by_employee_id(
        db_session=db_session, employee_id=employee_id
    )
    if not list_dependants["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    return list_dependants


# POST /dependants
def create_dependant(*, db_session, dependant_in: DependantCreate):
    """Creates a new dependant."""
    if validate_create_dependant(db_session=db_session, dependant_in=dependant_in):
        try:
            dependant = add_dependant(db_session=db_session, dependant_in=dependant_in)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return dependant


# PUT /dependants/{dependant_id}
def update_dependant(*, db_session, dependant_id: int, dependant_in: DependantUpdate):
    """Updates a dependant with the given data."""
    if not check_exist_dependant_by_id(
        db_session=db_session, dependant_id=dependant_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    if validate_update_dependant(
        db_session=db_session, dependant_id=dependant_id, dependant_in=dependant_in
    ):
        try:
            dependant = modify_dependant(
                db_session=db_session,
                dependant_id=dependant_id,
                dependant_in=dependant_in,
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return dependant


# DELETE /dependants/{dependant_id}
def delete_dependant(*, db_session, dependant_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_dependant_by_id(
        db_session=db_session, dependant_id=dependant_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    try:
        removed_dependant = remove_dependant(
            db_session=db_session, dependant_id=dependant_id
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return removed_dependant


def create_dependant_by_xlsx(*, db_session, dependant_in: DependantImport):
    """Creates a new dependant."""
    try:
        if check_exist_dependant_by_code(
            db_session=db_session, dependant_code=dependant_in.code
        ):
            raise AppException(ErrorMessages.ResourceAlreadyExists, "dependant")
        if dependant_in.employee_code:
            employee = get_employee_by_code(
                db_session=db_session, employee_code=dependant_in.employee_code
            )
        employee_id = employee.id

        dependant_data = dependant_in.model_dump(exclude={"employee_code"})
        dependant_data["employee_id"] = employee_id

        dependant_create = DependantCreate(**dependant_data)

        dependant = add_dependant(db_session=db_session, dependant_in=dependant_create)

        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return dependant


def update_dependant_by_xlsx(
    *, db_session, dependant_db: PayrollDependant, dependant_in: DependantImport
):
    """Updates a employee with the given data."""
    dependant_data = dependant_db.dict()
    update_data = dependant_in.model_dump(exclude_unset=True)

    for field in dependant_data:
        if field in update_data:
            setattr(dependant_data, field, update_data[field])
    if dependant_in.employee_code:
        employee = get_employee_by_code(
            db_session=db_session, employee_code=dependant_in.employee_code
        )
        dependant_db.employee_id = employee.id

    db_session.commit()
    return dependant_db


def search_dependant_by_name(*, db_session, name: str) -> PayrollDependant:
    dependants = search_dependants_by_partial_name(db_session=db_session, name=name)
    return dependants


def upsert_dependant(db_session, dependant_in: DependantImport, update_on_exists: bool):
    """Creates or updates an employee based on the code."""
    dependant_db = retrieve_dependant_by_code(
        db_session=db_session, dependant_code=dependant_in.code
    )
    if dependant_db:
        if not update_on_exists:
            return dependant_db
        dependant_update = DependantImport(
            **dependant_in.model_dump(exclude_unset=True)
        )
        update_dependant_by_xlsx(
            db_session=db_session,
            dependant_db=dependant_db,
            dependant_in=dependant_update,
        )
    else:
        create_dependant_by_xlsx(db_session=db_session, dependant_in=dependant_in)
    return dependant_db


def upload_dependants_XLSX(
    *, db_session, file: UploadFile = File(...), update_on_exists: bool = False
):
    data = BytesIO(file.file.read())

    dtype_map = {v: str for v in IMPORT_DEPENDANTS_EXCEL_MAP.values()}

    _data = pd.read_excel(data, dtype=dtype_map)
    df = pd.DataFrame(
        _data,
        columns=list(IMPORT_DEPENDANTS_EXCEL_MAP.values()),
    )

    df.dropna(subset=["Mã người phụ thuộc *"], inplace=True)
    df = df.rename(columns={v: k for k, v in IMPORT_DEPENDANTS_EXCEL_MAP.items()})

    df = df.astype(DTYPES_MAP)
    date_columns = ["date_of_birth", "deduction_from", "deduction_to"]

    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    depedants_data = []
    errors = []
    for index, row in df.iterrows():
        try:
            if pd.isna(row["code"]):
                log.warn(f"Skipping row {index + 2} due to missing 'Code'")
                continue

            depedant_data = row.to_dict()
            for key, value in depedant_data.items():
                if value == "nan" or value is pd.NaT:
                    depedant_data[key] = None

            depedant_data["id_doc_type"] = ID_DOC_TYPE_MAPPING.get(
                depedant_data.get("id_doc_type"), "other"
            )
            depedant_data["relationship"] = RELATIONSHIP_MAPPING.get(
                depedant_data.get("relationship"), "other"
            )
            depedant = DependantImport.model_validate(depedant_data)
            depedants_data.append(depedant)

        except ValidationError as e:
            errors.append(
                {"row": index + 2, "errors": e.errors()}
            )  # +2 to account for header and 0-indexing
        except TypeError as e:
            errors.append({"row": index + 2, "errors": [{"msg": str(e)}]})

    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors},
        )
    # Insert all valid records into the database
    for depedant_data in depedants_data:
        upsert_dependant(
            db_session=db_session,
            dependant_in=depedant_data,
            update_on_exists=update_on_exists,
        )

    return {"message": "Người phụ thuộc đã được thêm thành công từ tệp Excel"}
