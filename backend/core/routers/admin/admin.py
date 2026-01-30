from fastapi import APIRouter
from .import admin_home,notice,user_view

router=APIRouter(prefix="/admin",tags=["Admin"])

router.include_router(admin_home.router)
#router.include_router(notice.router)
router.include_router(user_view.router)





