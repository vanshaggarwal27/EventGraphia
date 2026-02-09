from rest_framework.routers import DefaultRouter
from .views import EventViewSet, PhotographerViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'photographers', PhotographerViewSet)
router.register(r'assignments', AssignmentViewSet)

urlpatterns = router.urls
