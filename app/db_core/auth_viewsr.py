from fastapi import APIRouter

auth_router = APIRouter(prefix="auth_user", tags="JWT")


@auth_router.post("/login")
