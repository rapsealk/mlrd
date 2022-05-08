from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from mlrd.database import get_db
from mlrd.auth.schema.user import UserCreate, UserRead
from mlrd.auth.service import UserService
from mlrd.auth.tasks import publish_user_signup_event

router = APIRouter()


@router.post("/signup", response_model=UserRead)
async def signup_user(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db_session: Session = Depends(get_db)
):
    service = UserService(session=db_session)
    try:
        user = await service.signup(user_in=user_in)
        background_tasks.add_task(publish_user_signup_event, routing_key="", user=user)
        return user
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": e._message()}]
        )


@router.post("/signin", response_model=UserRead)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db)
):
    """사용자 인증(Authentication) 과정을 수행합니다.

    사용자는 username(str)과 password(str)를 입력합니다. username은 아래의 형태를 모두 허용합니다.
    * (1) 이메일: piono623@naver.com
    * (2) 사용자 이름: rapsealk

    Args:
        :param :py:class:`fastapi.security.OAuth2PasswordRequestForm` form_data: `username`과 `password` 등의 인증 요청 정보를 담은 객체

    Returns:
        :returns: :py:class:`mlrd.auth.schema.user.UserRead`
    """
    service = UserService(session=db_session)
    if user := await service.signin(email=form_data.username, password=form_data.password):
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=[{"msg": f"The user with this username({form_data.username}) does not exists or password does not match."}]
    )
