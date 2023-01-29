from rest_framework import routers

from .views import TextViewSet, StringViewSet

router = routers.SimpleRouter()

router.register(r'texts', TextViewSet, basename="texts")
router.register(r'strings', StringViewSet, basename="strings")

urlpatterns = router.urls