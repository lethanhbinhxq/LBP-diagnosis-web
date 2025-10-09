from .auth_api import router as auth_router
from .diagnosis_api import router as diagnosis_router
from .statistic_api import router as statistic_router

all_routers = [
    auth_router,
    diagnosis_router,
    statistic_router,
]
