from pydantic import BaseModel

#отправка данных в БД
class Product(BaseModel):
    id: int
    name: str
    text: str
    price: int