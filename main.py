from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dictionary storage
expenses = {}


class Expense(BaseModel):
    expense_id: int
    description: str
    amount: float
    category: str


# Add Expense
@app.post("/expenses")
async def add_expense(expense: Expense):

    if not expense.description.strip():
        raise HTTPException(status_code=400,
                            detail="Description cannot be empty")

    if expense.amount <= 0:
        raise HTTPException(status_code=400,
                            detail="Amount must be greater than zero")

    expenses[expense.expense_id] = expense.dict()

    return {"message": "Expense added successfully"}


# View All Expenses
@app.get("/expenses")
async def get_expenses():
    return list(expenses.values())


# Update Expense
@app.put("/expenses/{expense_id}")
async def update_expense(expense_id: int, expense: Expense):

    if expense_id not in expenses:
        raise HTTPException(status_code=404,
                            detail="Expense not found")

    if not expense.description.strip():
        raise HTTPException(status_code=400,
                            detail="Description cannot be empty")

    if expense.amount <= 0:
        raise HTTPException(status_code=400,
                            detail="Amount must be greater than zero")

    expenses[expense_id] = expense.dict()

    return {"message": "Expense updated successfully"}


# Delete Expense
@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):

    if expense_id not in expenses:
        raise HTTPException(status_code=404,
                            detail="Expense not found")

    del expenses[expense_id]

    return {"message": "Expense deleted successfully"}


@app.get("/expenses/{expense_id}")
async def get_expense(expense_id: int):

    if expense_id not in expenses:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expenses[expense_id]