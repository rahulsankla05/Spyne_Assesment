from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/discussions/", response_model=schemas.Discussion)
def create_discussion(discussion: schemas.DiscussionCreate, db: Session = Depends(get_db)):
    # Assuming user_id is obtained from authentication/authorization
    user_id = 1  # This should be replaced with actual user id
    return crud.create_discussion(db=db, discussion=discussion, user_id=user_id)

@app.get("/discussions/", response_model=List[schemas.Discussion])
def read_discussions(tag: str = None, text: str = None, db: Session = Depends(get_db)):
    if tag:
        return crud.get_discussions_by_tag(db, tag=tag)
    if text:
        return crud.get_disc
