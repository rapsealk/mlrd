from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mlrd.config import SECRET_KEY
from mlrd.database import get_db
from mlrd.models import Response
from mlrd.auth.schema.user import UserCreate, UserRead
from mlrd.auth.service import UserService

router = APIRouter()


@router.post("/signup", response_model=Response[UserRead])
async def signup_user(
    user_in: UserCreate,
    db_session: Session = Depends(get_db),
    secret: str = SECRET_KEY
):
    service = UserService()
    user = await service.create_user(db_session=db_session, user_in=user_in, secret=secret)
    return Response[UserRead](data=user)
