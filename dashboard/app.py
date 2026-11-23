from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
import plotly.express as px
from backend.app.database import Base,engine,SessionLocal
from backend.app.services import summary,monthly,categories,transactions
from pipelines.etl import process_csv

Base.metadata.create_all(bind=engine)
st.set_page_config(page_title="FinSight",page_icon="📊",layout="wide")
st.title("📊 FinSight")
st.caption("Financial Data Intelligence Platform · Turn transactions into useful insights")

with st.sidebar:
    st.header("Import data")
    upload = st.file_uploader("Upload transaction CSV",type=["csv"])
    if upload and st.button("Process transactions",type="primary"):
        folder=Path("data/raw"); folder.mkdir(parents=True,exist_ok=True)
        path=folder/Path(upload.name).name
        path.write_bytes(upload.getvalue())
        db=SessionLocal()
        try:
            result=process_csv(db,str(path))
            st.success(f"Loaded {result['loaded']} · Rejected {result['rejected']} · Duplicates {result['duplicates']}")
        except Exception as e:
            db.rollback(); st.error(str(e))
        finally: db.close()
    st.info("Demo data only. Do not upload sensitive bank statements.")

db=SessionLocal()
try:
    totals=summary(db); months=monthly(db); cats=categories(db); tx=transactions(db,300)
finally: db.close()

if totals["transaction_count"]==0:
    st.warning("No data loaded yet. Run `python scripts/generate_sample_data.py` and `python scripts/run_etl.py`, or upload a CSV.")
    st.stop()

st.subheader("Financial overview")
a,b,c,d=st.columns(4)
a.metric("Income",f"R {totals['income']:,.2f}")
b.metric("Expenses",f"R {totals['expenses']:,.2f}")
c.metric("Net cash flow",f"R {totals['net_cash_flow']:,.2f}")
d.metric("Savings rate",f"{totals['savings_rate']:.1f}%")
st.caption(f"{totals['transaction_count']:,} processed transactions")
left,right=st.columns(2)
with left:
    st.subheader("Monthly income vs expenses")
    frame=pd.DataFrame(months).melt(id_vars="month",var_name="type",value_name="amount")
    st.plotly_chart(px.bar(frame,x="month",y="amount",color="type",barmode="group"),use_container_width=True)
with right:
    st.subheader("Expenses by category")
    st.plotly_chart(px.pie(pd.DataFrame(cats),names="category",values="total",hole=.45),use_container_width=True)
st.subheader("Recent transactions")
table=pd.DataFrame(tx)
table["amount"]=table.amount.map(lambda n:f"R {n:,.2f}")
st.dataframe(table,use_container_width=True,hide_index=True)
