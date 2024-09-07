from fastapi import FastAPI
from fastapi import FastAPI, Response, Cookie, HTTPException, Depends
from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from models.change_market import Product
from models.change_user import User
from models.fake_base import fake_users
from auth.auth import auth_backend
app = FastAPI(
    title="Web"
)

# @app.get("/")
# def get_hello():
#     return "Hello world!"

#поиск по имени
@app.get("/users/by-name/{name}")
async def get_user_name(name: str):
    return [user for user in fake_users if user.get("name") == name]


@app.get("/users/by-surname/{surname}")
async def get_user_surname(surname: str):
    # Возвращает список пользователей, у которых фамилия совпадает с переданным параметром surname
    print(surname)
    return [user for user in fake_users if user.get("surname") == surname]



#поиск по id
@app.get("/users/")
async def get_user(user_id: int):
    user = next((user for user in fake_users if user.get("id") == user_id), None)
    if user:
        return user
    else:
        return {"error": "User not found"}


#применение лимита поиска
@app.get("/users")
async def get_more_users(limit: int = 1, offset: int = 0):
    return fake_users[offset:][:limit]

#изменение имени и фамилии
@app.post("/users/{user_id}")
async def change_user_name(user_id: int, new_name: str, new_surname: str):
        current_user_name = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
        current_user_surname = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
        current_user_name["name"] = new_name
        current_user_surname["surname"] = new_surname
        return {"status": 200, "name": new_name,"surname": new_surname}

@app.post("/user/{User}")
async def create_user(user: User):
    return {"message": "User created successfully", "user": user}

@app.get("/set_cookie/")
def set_cookie(response: Response):
    response.set_cookie(key="my_cookie", value="cookie_value", httponly=True)
    return {"message": "Cookie has been set"}

# Чтение cookie из запроса
@app.get("/get_cookie/")
def get_cookie(my_cookie: str = Cookie(None)):
    if my_cookie:
        return {"my_cookie": my_cookie}
    else:
        raise HTTPException(status_code=404, detail="Cookie not found")

# Удаление cookie
@app.get("/delete_cookie/")
def delete_cookie(response: Response):
    response.delete_cookie(key="my_cookie")
    return {"message": "Cookie has been deleted"}

@app.post("/product/")
async def create_product(product: Product):
    return {"message": "Product created successfully", "product": Product}

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"