from pathlib import Path
from datetime import date,timedelta
import random
import pandas as pd

random.seed(42)
rows=[]
start=date(2025,1,1)
expenses={"Groceries":["Supermarket","Food shopping"],"Transport":["Fuel","Taxi fare"],
          "Housing":["Rent","Electricity"],"Entertainment":["Restaurant","Streaming"],
          "Health":["Pharmacy","Medical"],"Shopping":["Clothing","Household items"]}
for i in range(420):
    day=start+timedelta(days=random.randint(0,364))
    if random.random()<.22:
        amount=round(random.uniform(8000,32000),2)
        kind="income"; category=random.choice(["Salary","Freelance"]); desc="Monthly income"
    else:
        category=random.choice(list(expenses)); desc=random.choice(expenses[category])
        amount=round(random.uniform(35,2200),2); kind="expense"
    rows.append({"transaction_date":day.isoformat(),"description":desc,"amount":amount,
        "transaction_type":kind,"category":category,"account":random.choice(["Main Account","Savings Account"]),
        "user_email":random.choice(["demo.user@example.com","smallbiz@example.com"])})
out=Path("data/sample/transactions.csv"); out.parent.mkdir(parents=True,exist_ok=True)
pd.DataFrame(rows).sort_values("transaction_date").to_csv(out,index=False)
print(f"Generated {len(rows)} synthetic transactions: {out}")
