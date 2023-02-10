from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm


import pymysql
pymysql.install_as_MySQLdb()
# import models
# from . import models
from database import engine
# from routes.routes_masterdata import router_masterdata
from routes.routes_general import router_general
from routes.routes_user import router_user
from routes.router_user_part2 import router_user_part2
# from starlette.requests import Request
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/test")
# async def my_route(request: Request) -> None:
#     print(request.url.path)
#     return request.base_url._url

# สำหรับเปิด Test Swagger UI


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    setuser = "siwakorn"
    # setpassword = "5CJwIvpNYwASgKUU"
    setpassword = "12345"
    username = form_data.username
    password = form_data.password
    # print(username)
    if username == setuser and password == setpassword:
        return {"access_token": "success", "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
app.include_router(router_user, prefix="/user", tags=["UserPart1"])
app.include_router(router_user_part2, prefix="/userpart2", tags=["UserPart2"])
# app.include_router(router_masterdata, prefix="/masterdata",
#                    tags=["Masterdata"])
app.include_router(router_general, prefix="/general", tags=["General"])



