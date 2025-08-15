from .auth_api import router as auth_router
from .diagnosis_api import router as diagnosis_router
from .statistic_api import router as statistic_router
from .feedback_api import router as feedback_router

all_routers = [
    auth_router,
    diagnosis_router,
    statistic_router,
    feedback_router
]
