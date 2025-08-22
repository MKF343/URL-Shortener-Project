import secrets
import string
import sqlalchemy
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

#1.Database Setup
DATABASE_URL = "sqlite:///./urls.db"
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = sqlalchemy.MetaData()

urls_table = sqlalchemy.Table(
    "urls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("short_code", sqlalchemy.String, index=True, unique=True),
    sqlalchemy.Column("originalurl", sqlalchemy.String, index=True),
)

metadata.create_all(engine)


#2.Pydantic Models
class URLBase(BaseModel):
    url: str


class URLInfo(BaseModel):
    originalurl: str
    shorturl: str


#3.FastAPI App Initialization
app = FastAPI()


#4.Helper Functions
def get_db():
    #Dependency to get a database session.
    with Session(engine) as session:
        yield session


def generateshortcode(length: int = 7) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


# 5. API Endpoints
@app.post("/shorten", response_model=URLInfo)
def createShortUrl(request: Request, url_data: URLBase, db: Session = Depends(get_db)):

    #Takes a long URL and creates a short, unique code of it.

    originalurl = url_data.url

    #checking if URL already exists
    existing = db.query(urls_table).filter(urls_table.c.originalurl == originalurl).first()
    if existing:
        short_code = existing.short_code
    else:
        #generate a new unique short code
        while True:
            short_code = generateshortcode()
            if not db.query(urls_table).filter(urls_table.c.short_code == short_code).first():
                break

        #save the new entry
        db.execute(urls_table.insert().values(originalurl=originalurl, short_code=short_code))
        db.commit()

    shorturl = f"{request.url.scheme}://{request.url.netloc}/{short_code}"

    return {"originalurl": originalurl, "shorturl": shorturl}


@app.get("/{short_code}")
def redirectToUrl(short_code: str, db: Session = Depends(get_db)):

    #Looks up the short code and redirects to the original URL.

    entry = db.query(urls_table).filter(urls_table.c.short_code == short_code).first()

    if entry is None:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=entry.originalurl)