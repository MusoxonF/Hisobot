from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('xodim/', XodimView.as_view(), name='xodim'),
    path('xodim/<int:id>/', XodimDetail.as_view(), name='xodim_detail'),
]