from aiogram import Router
from .events import router as events_router
from .open_days import router as days_router
from .socials import router as socials_router
from .about import router as about_router
from .history import router as history_router
from .park import router as park_router
from .governance import router as governance_router

router=Router()

router.include_router(events_router)
router.include_router(days_router)
router.include_router(socials_router)
router.include_router(about_router)
router.include_router(history_router)
router.include_router(park_router)
router.include_router(governance_router)