from fastapi import APIRouter
from . import user_dashboard
from .support import support_home
router=APIRouter(prefix="/user",tags=["User"])

router.include_router(user_dashboard.router)
router.include_router(support_home.router)


