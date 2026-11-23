from pathlib import Path
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models
from .services import summary, monthly, categories, transactions
from pipelines.etl import process_csv

Base.metadata.create_all(bind=engine)
app = FastAPI(title="FinSight API", version="1.0.0")

@app.get("/health")
def health():
    return {"status":"healthy","service":"FinSight API"}

@app.post("/transactions/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400,"Please upload a CSV file.")
    content = await file.read()
    if len(content) > 10*1024*1024:
        raise HTTPException(413,"Maximum upload size is 10 MB.")
    folder = Path("data/raw"); folder.mkdir(parents=True,exist_ok=True)
    path = folder / Path(file.filename).name
    path.write_bytes(content)
    try:
        result = process_csv(db,str(path))
        return {"filename":path.name,**result}
    except Exception as exc:
        db.rollback()
        raise HTTPException(400,f"CSV processing failed: {exc}")

@app.get("/analytics/summary")
def get_summary(db: Session=Depends(get_db)): return summary(db)

@app.get("/analytics/monthly")
def get_monthly(db: Session=Depends(get_db)): return monthly(db)

@app.get("/analytics/categories")
def get_categories(db: Session=Depends(get_db)): return categories(db)

@app.get("/transactions")
def get_transactions(limit:int=100,db:Session=Depends(get_db)):
    if limit<1 or limit>1000: raise HTTPException(400,"limit must be 1 to 1000")
    return transactions(db,limit)
