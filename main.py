from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import engine, load_database
from models import BaseModel, User
from schemas import APIResponse, UserRequest, UserResponse

BaseModel.metadata.create_all(bind=engine)

app = FastAPI()


@app.api_route("/health", methods=["GET", "HEAD"])
async def healthCheck():
    return {"status": "awake"}


@app.post("/signup")
def signup(
    body: UserRequest, database: Session = Depends(load_database)
) -> APIResponse[UserResponse]:
    if database.query(User).filter(User.email == body.email):
        raise HTTPException(status_code=400, detail="Email already in use")

    newUser: User = User(email=body.email, password=body.password)

    database.add(newUser)
    database.commit()
    database.refresh(newUser)

    return APIResponse(success=True, data=UserResponse(token="11111"))


@app.post("/login")
def login(
    body: UserRequest, database: Session = Depends(load_database)
) -> APIResponse[UserResponse]:
    user: User = database.query(User).filter(User.email == body.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return APIResponse(success=True, data=UserResponse(token="11111"))
