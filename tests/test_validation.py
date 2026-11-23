import pandas as pd
from pipelines.validation import validate_transactions

def test_valid_and_invalid_rows():
    frame=pd.DataFrame([
        {"transaction_date":"2025-01-01","description":"Pay","amount":"1000","transaction_type":"income","category":"Salary","account":"Main","user_email":"a@example.com"},
        {"transaction_date":"bad","description":"Bad","amount":"-4","transaction_type":"other","category":"","account":"Main","user_email":"bad"}
    ])
    clean,rejected=validate_transactions(frame)
    assert len(clean)==1
    assert len(rejected)==1

def test_duplicate_rows_removed():
    row={"transaction_date":"2025-01-01","description":"Pay","amount":"1000","transaction_type":"income","category":"Salary","account":"Main","user_email":"a@example.com"}
    clean,_=validate_transactions(pd.DataFrame([row,row]))
    assert len(clean)==1
