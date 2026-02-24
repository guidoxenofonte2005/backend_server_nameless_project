from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from schemas import APIResponse, UserRequest, UserResponse
from database import load_database, engine
from models import BaseModel, User

BaseModel.metadata.create_all(bind=engine)

app = FastAPI()


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
