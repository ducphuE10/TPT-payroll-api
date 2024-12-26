from fastapi import Request
from sqlalchemy.orm import sessionmaker
from app.db.core import engine


async def create_db_session(request: Request, call_next):
    try:
        session = sessionmaker(bind=engine)
        request.state.db = session()
        response = await call_next(request)
    except Exception as e:
        raise e from None
    finally:
        request.state.db.close()

    return response
