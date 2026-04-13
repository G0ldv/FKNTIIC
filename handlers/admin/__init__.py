from aiogram import Router
from .admin import router as admin_router
from .questions import router as questions_router

router=Router()

router.include_router(admin_router)
router.include_router(questions_router)