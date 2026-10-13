from pydantic import BaseModel, Field

from contextlib import asynccontextmanager

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Sale, SessionLocal, create_tables


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()

    df = pd.read_csv("sales.csv")
    required = {
        "order_id", "product", "region", "quantity", "unit_price"
    }

    if not required.issubset(df.columns):
        raise RuntimeError(f"CSV must contain columns: {sorted(required)}")

    db = SessionLocal()
    try:
        # Import CSV records not already present in the database.
        existing_ids = {
            row[0] for row in db.query(Sale.order_id).all()
        }

        for _, row in df.iterrows():
            order_id = int(row["order_id"])

            if order_id not in existing_ids:
                db.add(
                    Sale(
                        order_id=order_id,
                        product=str(row["product"]),
                        region=str(row["region"]),
                        quantity=int(row["quantity"]),
                        unit_price=float(row["unit_price"]),
                    )
                )

        db.commit()
    finally:
        db.close()

    yield


app = FastAPI(
    title="Enterprise AI Data Analysis Agent",
    description="Sales analysis API powered by FastAPI and SQLite",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {"message": "Enterprise AI Data Analysis Agent API is running"}


@app.get("/sales")
def get_sales(db: Session = Depends(get_db)):
    records = db.query(Sale).order_by(Sale.order_id).all()

    return [
        {
            "order_id": s.order_id,
            "product": s.product,
            "region": s.region,
            "quantity": s.quantity,
            "unit_price": s.unit_price,
            "revenue": round(s.revenue, 2),
        }
        for s in records
    ]


@app.get("/sales/summary")
def get_summary(db: Session = Depends(get_db)):
    total = db.query(
        func.sum(Sale.quantity * Sale.unit_price)
    ).scalar() or 0

    return {
        "total_revenue": round(total, 2),
        "total_orders": db.query(Sale).count(),
    }


@app.get("/sales/top-product")
def get_top_product(db: Session = Depends(get_db)):
    result = (
        db.query(
            Sale.product,
            func.sum(Sale.quantity * Sale.unit_price).label("revenue"),
        )
        .group_by(Sale.product)
        .order_by(func.sum(Sale.quantity * Sale.unit_price).desc())
        .first()
    )

    if result is None:
        raise HTTPException(status_code=404, detail="No sales data found")

    return {
        "product": result.product,
        "revenue": round(result.revenue, 2),
    }


@app.get("/sales/regions")
def get_sales_by_region(db: Session = Depends(get_db)):
    results = (
        db.query(
            Sale.region,
            func.sum(Sale.quantity * Sale.unit_price).label("revenue"),
        )
        .group_by(Sale.region)
        .order_by(Sale.region)
        .all()
    )

    return [
        {"region": row.region, "revenue": round(row.revenue, 2)}
        for row in results
    ]


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.post("/ask")
def ask_question(request: AskRequest):
    from llm_agent import ask_agent

    try:
        answer = ask_agent(request.question)

        return {
            "question": request.question,
            "answer": answer,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to process the question. Check the server logs.",
        ) from error

        
