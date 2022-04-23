from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mlrd.config import SECRET_KEY
from mlrd.database import get_db
from mlrd.models import Response
from mlrd.auth.models import User, UserCreate, UserRead
from mlrd.auth.services import create_user

router = APIRouter()


@router.post("/signup", response_model=Response[UserRead])
async def signup_user(
    user_in: UserCreate,
    db_session: Session = Depends(get_db),
    secret: str = SECRET_KEY
):
    user = await create_user(db_session=db_session, user_in=user_in, secret=secret)
    return Response[UserRead](data=user)
