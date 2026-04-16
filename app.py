from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="LedgerLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAMPLE_ROWS = 5000
USD_TO_INR = 83.0


def read_uploaded_file(file: UploadFile) -> pd.DataFrame:
    filename = file.filename or ""
    suffix = Path(filename).suffix.lower()
    contents = file.file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if suffix == ".zip":
        with ZipFile(BytesIO(contents)) as archive:
            csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]

            if not csv_names:
                raise HTTPException(status_code=400, detail="ZIP file does not contain a CSV.")

            with archive.open(csv_names[0]) as csv_file:
                return pd.read_csv(csv_file, nrows=SAMPLE_ROWS)

    if suffix == ".csv":
        return pd.read_csv(BytesIO(contents), nrows=SAMPLE_ROWS)

    raise HTTPException(status_code=400, detail="Please upload a CSV or ZIP file.")


def find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    normalized_columns = {column.lower().strip(): column for column in df.columns}

    for candidate in candidates:
        if candidate in normalized_columns:
            return normalized_columns[candidate]

    return None


@app.get("/")
def health_check():
    return {"status": "LedgerLens API is running"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        df = read_uploaded_file(file)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read file: {exc}") from exc

    amount_col = find_column(df, ["amount", "amt", "transaction_amount"])
    category_col = find_column(df, ["category", "merchant_category"])
    date_col = find_column(df, ["date", "trans_date_trans_time", "transaction_date"])
    description_col = find_column(df, ["description", "merchant", "details", "name"])
    fraud_col = find_column(df, ["is_fraud", "fraud", "risky"])

    if not amount_col:
        raise HTTPException(status_code=400, detail="CSV needs an amount or amt column.")

    transactions = []

    for _, row in df.iterrows():
        amount_usd = pd.to_numeric(row.get(amount_col), errors="coerce")

        if pd.isna(amount_usd):
            continue

        amount = round(float(amount_usd) * USD_TO_INR, 2)
        category = str(row.get(category_col, "Uncategorized")) if category_col else "Uncategorized"
        description = str(row.get(description_col, "Transaction")) if description_col else "Transaction"
        date = str(row.get(date_col, ""))[:10] if date_col else ""
        fraud_value = row.get(fraud_col, 0) if fraud_col else 0

        is_marked_fraud = str(fraud_value).strip().lower() in {"1", "true", "yes"}
        is_rule_risky = amount >= 15000 or category in {"misc_net", "shopping_net", "grocery_pos"}

        transactions.append(
            {
                "date": date,
                "description": description.replace("fraud_", ""),
                "category": category,
                "amount": amount,
                "risky": is_marked_fraud or is_rule_risky,
            }
        )

    if not transactions:
        raise HTTPException(status_code=400, detail="No valid transaction rows found.")

    total_spent = round(sum(item["amount"] for item in transactions), 2)
    avg_spent = round(total_spent / len(transactions), 2)
    risky = sorted(
        [item for item in transactions if item["risky"]],
        key=lambda item: item["amount"],
        reverse=True,
    )[:20]

    return {
        "transactions": transactions,
        "summary": {
            "total_spent": total_spent,
            "avg_spent": avg_spent,
            "risky": risky,
            "transaction_count": len(transactions),
        },
    }
