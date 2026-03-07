# """
# URL Configuration for Binder ERP System
# """
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from rest_framework import permissions
# # from drf_yasg.views import get_schema_view
# # from drf_yasg import openapi

# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView,
# )

# # Swagger/OpenAPI Schema
# # schema_view = get_schema_view(
# #     openapi.Info(
# #         title="Binder ERP API",
# #         default_version='v1',
# #         description="""
# #         Binder - Complete ERP System for Textile Manufacturing Industry
        
# #         ## Features
# #         - Multi-tenant SaaS architecture
# #         - Role-based access control (RBAC)
# #         - JWT authentication
# #         - Email verification
# #         - Google Sheets integration
# #         - Inventory management
# #         - Community forum
# #         - System health monitoring
        
# #         ## Authentication
# #         Use Bearer token in Authorization header:
# #         `Authorization: Bearer <your_jwt_token>`
# #         """,
# #         terms_of_service="https://binder.com/terms/",
# #         contact=openapi.Contact(email="support@binder.com"),
# #         license=openapi.License(name="Proprietary License"),
# #     ),
# #     public=True,
# #     permission_classes=[permissions.AllowAny],
# # )

# urlpatterns = [
#     # Admin
#     path('admin/', admin.site.urls),
    
    
#     # API Documentation
#     path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
#     # API Endpoints - 4 Pillars
#     path('api/auth/', include('auth_service.urls')),           # Pillar 1: Authentication
#     path('api/ims/', include('inventory_management.urls')),    # Pillar 2: IMS
#     path('api/community/', include('community.urls')),         # Pillar 3: Community
#     path('api/health/', include('load_balancer.urls')),        # Pillar 4: Load Balancer
    
#     # Shared Services
#     path('api/sheets/', include('shared.sheets_urls')),        # Google Sheets API
# ]

# # Serve media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # Admin site customization
# admin.site.site_header = "Binder ERP Administration"
# admin.site.site_title = "Binder Admin"
# admin.site.index_title = "Welcome to Binder ERP Admin Panel"


"""
URL Configuration for Binder ERP System
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints - 4 Pillars
    path('api/auth/', include('auth_service.urls')),
    path('api/ims/', include('inventory_management.urls')),
    path('api/community/', include('community.urls')),
    path('api/health/', include('load_balancer.urls')),
    
    # Shared Services
    path('api/sheets/', include('shared.sheets_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Binder ERP Administration"
admin.site.site_title = "Binder Admin"
admin.site.index_title = "Welcome to Binder ERP Admin Panel"