
from pydantic import BaseModel

#отправка данных в БД
class User(BaseModel):
    id: int
    name: str
    surname: str
    emale: str
    role: str
    