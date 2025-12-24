from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.orm import Session
from models import Product as ProductModel
from database import Product as DBProduct, get_db
import database
from typing import Annotated
from fastapi import Form

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

products = [
    ProductModel(id=1, name="apple", description="good health", price=10, is_offer=False),
    ProductModel(id=2, name="banana", description="yellow fruit", price=20, is_offer=True),
    ProductModel(id=3, name="grapes", description="small fruit", price=30, is_offer=False),
]

def init_db():
    db = database.SessionLocal()
    for product in products:
        db.add(product(**product.model_dump()))
    db.commit()
    db.close()

# init_db()  # Commented out to avoid duplicate inserts
'''@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return "login successful"'''

@app.get("/products")
async def get_data(db: Session = Depends(get_db)):
    products = db.query(DBProduct).all()
    return {"products": [p.__dict__ for p in products]}

@app.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.__dict__
    
@app.post("/products")
async def add_product(p: ProductModel, db: Session = Depends(get_db)):
    db_product = DBProduct(**p.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product.__dict__

@app.put("/products/{product_id}")
async def update_product(product_id: int, p: ProductModel, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in p.dict().items():
        setattr(product, key, value)
    db.commit()
    return "product updated"

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return "product deleted"
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)