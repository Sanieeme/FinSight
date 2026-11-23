import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.etl import process_csv
from backend.app.database import Base, engine, SessionLocal


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--file",default="data/sample/transactions.csv")
    args=parser.parse_args()
    if not Path(args.file).exists(): raise SystemExit(f"File not found: {args.file}")
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        result=process_csv(db,args.file)
        print(f"ETL finished — loaded: {result['loaded']}, rejected: {result['rejected']}, duplicates: {result['duplicates']}")
    finally: db.close()

if __name__=="__main__": main()
