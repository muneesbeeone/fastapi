from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from datetime import datetime

from database import Base, engine, get_db
from models import Token

# Initialize FastAPI app
app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Pydantic models for requests and responses
class BookingRequest(BaseModel):
    name: str
    email: str
    phone: str

class TokenResponse(BaseModel):
    token_id: str
    name: str
    booking_time: datetime

# Routes

@app.post("/book-token/", response_model=TokenResponse)
def book_token(request: BookingRequest, db: Session = Depends(get_db)):
    """
    Book a token and save it to the database.
    """
    token_id = str(uuid.uuid4())
    new_token = Token(
        token_id=token_id,
        name=request.name,
        email=request.email,
        phone=request.phone,
    )

    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    return TokenResponse(
        token_id=new_token.token_id,
        name=new_token.name,
        booking_time=new_token.booking_time
    )

@app.get("/tokens/")
def get_all_tokens(db: Session = Depends(get_db)):
    """
    Retrieve all tokens from the database.
    """
    tokens = db.query(Token).all()
    return {"tokens": tokens}

@app.get("/tokens/{token_id}")
def get_token_details(token_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific token by its ID.
    """
    token = db.query(Token).filter(Token.token_id == token_id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return token

@app.delete("/tokens/{token_id}")
def delete_token(token_id: str, db: Session = Depends(get_db)):
    """
    Delete a token by its ID.
    """
    token = db.query(Token).filter(Token.token_id == token_id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    db.delete(token)
    db.commit()
    return {"message": "Token deleted successfully!"}
