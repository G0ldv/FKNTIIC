from aiogram import Router
from .menu import router as menu_router
from .rules import router as rules_router
from .documents import router as docs_router
from .specialties import router as spec_router
from .price import router as price_router
from .contacts import router as contacts_router
from .prep_courses import router as prep_courses_router
from .motivation import router as motivation_router
from .deadlines import router as deadlines_router
from .exams import router as exams_router

router = Router()

router.include_router(menu_router)
router.include_router(rules_router)
router.include_router(docs_router)
router.include_router(spec_router)
router.include_router(price_router)
router.include_router(contacts_router)
router.include_router(prep_courses_router)
router.include_router(motivation_router)
router.include_router(deadlines_router)
router.include_router(exams_router)