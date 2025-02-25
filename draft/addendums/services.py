# from docx import Document

from app.addendums.repositories import (
    add_addendum,
    modify_addendum,
    remove_addendum,
    retrieve_addendum_by_code,
    retrieve_addendum_by_id,
    retrieve_all_addendums,
)
from app.addendums.schemas import AddendumCreate, AddendumUpdate
from app.exception import AppException, ErrorMessages

# from payroll.storage.services import read_file_from_minio


# def get_employee_active_contract(
#     *,
#     db_session,
#     employee_code: str,
#     current_date: date,
# ) -> Optional[PayrollContract]:
#     active_contract = retrieve_employee_active_contract(
#         db_session=db_session, employee_code=employee_code, current_date=current_date
#     )

#     if not active_contract:
#         raise AppException(ErrorMessages.ResourceNotFound(), "contract")

#     return active_contract


# def get_active_contract_benefits(
#     *,
#     db_session,
#     current_date: date,
# ) -> Optional[PayrollContract]:
#     active_contracts = retrieve_active_contracts(
#         db_session=db_session, current_date=current_date
#     )
#     count = 0
#     benefit_list = []
#     for contract in active_contracts:
#         benefit = BenefitRead(
#             id=contract.id,
#             meal_benefit=contract.meal_benefit,
#             transportation_benefit=contract.transportation_benefit,
#             housing_benefit=contract.housing_benefit,
#             toxic_benefit=contract.toxic_benefit,
#             phone_benefit=contract.phone_benefit,
#             attendant_benefit=contract.attendant_benefit,
#             employee=contract.employee,
#         )
#         count += 1
#         benefit_list.append(benefit)
#     return BenefitsRead(count=count, data=benefit_list)


def get_addendum_by_id(*, db_session, addendum_id: int):
    """Returns a contract based on the given id."""
    addendum = retrieve_addendum_by_id(db_session=db_session, addendum_id=addendum_id)

    if not addendum:
        raise AppException(ErrorMessages.ResourceNotFound(), "addendum")

    return addendum


def get_addendum_by_code(*, db_session, addendum_code: str):
    """Returns a contract based on the given id."""
    addendum = retrieve_addendum_by_code(
        db_session=db_session, addendum_code=addendum_code
    )

    if not addendum:
        raise AppException(ErrorMessages.ResourceNotFound(), "addendum")

    return addendum


def get_all_addendums(*, db_session):
    list_addendums = retrieve_all_addendums(db_session=db_session)
    if not list_addendums:
        raise AppException(ErrorMessages.ResourceNotFound(), "addendum")

    return list_addendums


def create_addendum(*, db_session, addendum_in: AddendumCreate):
    """Creates a new contract."""
    try:
        if get_addendum_by_code(db_session=db_session, addendum_code=addendum_in.code):
            raise AppException(ErrorMessages.ResourceAlreadyExists, "addendum")
        addendum = add_addendum(
            db_session=db_session, create_data=addendum_in.model_dump()
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return addendum


# def create_contract_with_benefits(
#     *,
#     db_session,
#     contract_in: ContractCreate,
#     benefits_list_in: Optional[List[BenefitCreate]] = None,
# ):
#     """Creates a new contract with benefits."""
#     if bool(get_contract_by_code(db_session=db_session, code=contract_in.code)):
#         raise AppException(ErrorMessages.ResourceAlreadyExists(), "contract")
#     # def create(*, db_session, create_data: dict)
#     try:
#         contract = create(db_session=db_session, contract_in=contract_in)

#         contract = retrieve_contract_by_code(
#             db_session=db_session, contract_code=contract_in.code
#         )
#         contract_with_benefits = None
#         if benefits_list_in:
#             from payroll.contract_benefit_assocs.services import create_multi_cbassocs

#             contract_with_benefits = create_multi_cbassocs(
#                 db_session=db_session,
#                 contract_id=contract.id,
#                 cbassoc_list_in=benefits_list_in,
#             )
#             return {"contract_in": contract, "benefits_list_in": contract_with_benefits}
#         db_session.commit()
#     except AppException as e:
#         db_session.rollback()
#         raise AppException(ErrorMessages.ErrSM99999(), str(e))
#     return {"contract_in": contract}


def update_addendum(*, db_session, addendum_id: int, addendum_in: AddendumUpdate):
    """Updates a contract with the given data."""
    try:
        if not get_addendum_by_id(db_session=db_session, addendum_id=addendum_id):
            raise AppException(ErrorMessages.ResourceNotFound(), "addendum")
        addendum = modify_addendum(
            db_session=db_session, addendum_id=addendum_id, addendum_in=addendum_in
        )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return addendum


# def update_contract_with_benefits(
#     *,
#     db_session,
#     contract_id: int,
#     contract_in: Optional[ContractUpdate] = None,
#     cbassoc_list_in: Optional[List[CBAssocsUpdate]] = None,
# ):
#     try:
#         if contract_in:
#             contract = update(
#                 db_session=db_session, id=contract_id, contract_in=contract_in
#             )

#         if cbassoc_list_in:
#             from payroll.contract_benefit_assocs.services import update_multi_cbassocs

#             contract_with_benefits = update_multi_cbassocs(
#                 db_session=db_session,
#                 cbassoc_list_in=cbassoc_list_in,
#                 contract_id=contract.id,
#             )
#         db_session.commit()
#     except AppException as e:
#         db_session.rollback()
#         raise AppException(ErrorMessages.ErrSM99999(), str(e))

#     return contract_with_benefits


def delete_addendum(*, db_session, addendum_id: int):
    """Deletes a contract based on the given id."""
    try:
        if not get_addendum_by_id(db_session=db_session, addendum_id=addendum_id):
            raise AppException(ErrorMessages.ResourceNotFound(), "addendum")
        addendum = remove_addendum(db_session=db_session, addendum_id=addendum_id)
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return addendum


# def generate_contract_docx(*, db_session, id: int) -> io.BytesIO:
#     """Generate a contract docx file based on the given data and template."""

#     contract_data = get_contract_by_id(db_session=db_session, id=id)

#     if not contract_data:
#         raise AppException(ErrorMessages.ResourceNotFound())

#     template_path = get_contractType_template(
#         db_session=db_session, code=contract_data.type_code
#     )
#     template_stream = read_file_from_minio(template_path)

#     doc = Document(template_stream)

#     # Create a temporary directory to store the generated contract
#     for paragraph in doc.paragraphs:
#         paragraph.text = paragraph.text.replace("{{contract_name}}", contract_data.name)
#         paragraph.text = paragraph.text.replace(
#             "{{employee_name}}", contract_data.employee.name
#         )

#     # Load the template
#     file_stream = io.BytesIO()
#     doc.save(file_stream)
#     file_stream.seek(0)  # Move the pointer to the beginning of the stream

#     return file_stream
