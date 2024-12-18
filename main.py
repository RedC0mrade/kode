import uvicorn

from fastapi import FastAPI
from app.users.views import router_users, router_user
from app.tickets.views import ticket_router
from app.authentication.views import auth_router
from app.tags.views import tag_router, association_router
from app.messages.views import messages_router

app = FastAPI()
app.include_router(router_user)
app.include_router(router_users)
app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(tag_router)
app.include_router(association_router)
app.include_router(messages_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
