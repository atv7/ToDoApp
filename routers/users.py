from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .auth import get_current_user, verify_password, get_password_hash
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from fastapi import APIRouter, Depends, Request, Form
from starlette.responses import RedirectResponse
from starlette import status
import sys
sys.path.append('..')


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/edit-user-password", response_class=HTMLResponse)
async def edit_user_view(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse('edit-user-password.html', {"request": request, "user": user})


@router.post("/edit-user-password", response_class=HTMLResponse)
async def user_password_change(request: Request, username: str = Form(...),
                               password: str = Form(...),
                               password2: str = Form(...),
                               db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    user_data = db.query(models.Users).filter(
        models.Users.username == username).first()

    msg = 'Invalid username or password'

    if user_data:
        if username == user_data.username and verify_password(password, user_data.hashed_password):
            user_data.hashed_password = get_password_hash(password2)
            db.add(user_data)
            db.commit()
            msg = 'Password updated'

    return templates.TemplateResponse("edit-user-password.html",
                                      {"request": request, "msg": msg, "user": user})
