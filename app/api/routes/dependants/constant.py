IMPORT_DEPENDANTS_EXCEL_MAP = {
    "code": "Mã người phụ thuộc *",
    "name": "HỌ VÀ TÊN *",
    "employee_code": "MÃ NHÂN VIÊN *",
    "date_of_birth": "NĂM SINH *",
    "id_doc_type": "LOẠI GIẤY TỜ *",
    "doc_number": "SỐ GIẤY TỜ *",
    "relationship": "QUAN HỆ *",
    "deduction_from": "KHẤU TRỪ TỪ NGÀY *",
    "deduction_to": "KHẤU TRỪ ĐẾN NGÀY *",
    "mst": "MST *",
}


DTYPES_MAP = {
    "code": str,
    "name": str,
    "employee_code": str,
    "date_of_birth": str,
    "id_doc_type": str,
    "doc_number": str,
    "relationship": str,
    "deduction_from": str,
    "deduction_to": str,
    "mst": str,
}

ID_DOC_TYPE_MAPPING = {
    "CMND": "cmnd",
    "CCCD": "cccd",
    "Giấy khai sinh": "giaykhaisinh",
    "Hộ chiếu": "hochieu",
    "Khác": "other",
}

RELATIONSHIP_MAPPING = {
    "Con cái": "child",
    "Bố mẹ": "parent",
    "Vợ chồng": "couple",
    "Khác": "other",
}
