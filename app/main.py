import uvicorn

from fastapi import FastAPI
from users.views import router_users, router_user

app =FastAPI()
app.include_router(router_user)
app.include_router(router_users)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
