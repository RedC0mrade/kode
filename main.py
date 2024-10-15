import uvicorn

from fastapi import FastAPI
from app.users.views import router_users, router_user
# from auth.views import auth_router
from app.authentication.views import auth_router

app = FastAPI()
app.include_router(router_user)
app.include_router(router_users)
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
