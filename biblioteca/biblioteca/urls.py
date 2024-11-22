from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Rota para o esquema OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Rota para o Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Rota para o Redoc UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Endpoint para gerar o token de autenticação
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]