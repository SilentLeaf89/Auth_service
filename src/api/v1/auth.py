from typing import Optional
from fastapi import APIRouter, Depends
from schemas.user import UserCreate, UserHistoryShow
from schemas.login import Login, Change
from services.auth_service import AuthService, get_auth_service

router = APIRouter()


@router.post("/signup")
async def signup(
    user_create: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    return await auth_service.signup(user_create=user_create)


@router.post("/refresh")
async def refresh(
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    return await auth_service.refresh()


@router.post("/login")
async def login(
    login: Login,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    return await auth_service.login(login)


@router.post("/logout")
async def logout(
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    return await auth_service.logout()


@router.post("/change")
async def change(
    change: Change,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    return await auth_service.change(change)


@router.post("/history")
async def history(
    n_items_per_page: Optional[int] = None,
    page_number: Optional[int] = None,
    descending: Optional[bool] = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> list[UserHistoryShow]:
    return await auth_service.history(
        n_items_per_page=n_items_per_page,
        page_number=page_number,
        descending=descending,
    )
