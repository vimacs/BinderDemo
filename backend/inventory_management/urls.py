# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     DepartmentViewSet, SegmentViewSet, department_menu_structure,
#     BuyerCodeViewSet, VendorCodeViewSet
# )

# # Create router and register viewsets
# router = DefaultRouter()
# router.register(r'departments', DepartmentViewSet, basename='department')
# router.register(r'segments', SegmentViewSet, basename='segment')
# router.register(r'buyer-codes', BuyerCodeViewSet, basename='buyer-code')
# router.register(r'vendor-codes', VendorCodeViewSet, basename='vendor-code')

# urlpatterns = [
#     # Router URLs for ViewSets
#     path('', include(router.urls)),
    
#     # Additional endpoints
#     path('menu-structure/', department_menu_structure, name='department-menu-structure'),
# ]

# """
# Factory Code URLs - V2
# =======================

# URL routing for the Factory Code module.
# Uses DRF nested routers for hierarchical resources.

# URL Structure:
# - /api/factory-code/choices/              -> All choice lists
# - /api/factory-code/schemas/              -> All field schemas
# - /api/factory-codes/                     -> FactoryCode CRUD
# - /api/factory-codes/{id}/products/       -> Products nested under FactoryCode
# - /api/factory-codes/{id}/consumption-materials/  -> Trims nested under FactoryCode
# - /api/factory-codes/{id}/artwork-materials/      -> Artwork nested under FactoryCode
# - /api/factory-codes/{id}/packaging/              -> Packaging nested under FactoryCode
# """

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers as nested_routers

# from .views import (
#     # ViewSets
#     FactoryCodeViewSet,
#     ProductViewSet,
#     ComponentViewSet,
#     RawMaterialViewSet,
#     ConsumptionMaterialViewSet,
#     ArtworkMaterialViewSet,
#     PackagingViewSet,
#     PackagingMaterialViewSet,
#     # Choice endpoints
#     all_choices,
#     trim_category_choices,
#     artwork_category_choices,
#     packaging_material_type_choices,
#     work_order_type_choices,
#     unit_choices,
#     size_unit_choices,
#     approval_choices,
#     approval_against_choices,
#     # Schema endpoints
#     all_field_schemas,
#     trim_category_fields,
#     artwork_category_fields,
#     packaging_material_fields,
# )


# # =============================================================================
# # MAIN ROUTER
# # =============================================================================

# router = DefaultRouter()
# router.register(r'factory-codes', FactoryCodeViewSet, basename='factory-code')


# # =============================================================================
# # NESTED ROUTERS
# # =============================================================================

# # Factory Code -> Products
# factory_code_router = nested_routers.NestedDefaultRouter(
#     router, r'factory-codes', lookup='factory_code'
# )
# factory_code_router.register(
#     r'products', ProductViewSet, basename='factory-code-products'
# )
# factory_code_router.register(
#     r'consumption-materials', ConsumptionMaterialViewSet, 
#     basename='factory-code-consumption-materials'
# )
# factory_code_router.register(
#     r'artwork-materials', ArtworkMaterialViewSet,
#     basename='factory-code-artwork-materials'
# )
# factory_code_router.register(
#     r'packaging', PackagingViewSet,
#     basename='factory-code-packaging'
# )

# # Products -> Components
# products_router = nested_routers.NestedDefaultRouter(
#     factory_code_router, r'products', lookup='product'
# )
# products_router.register(
#     r'components', ComponentViewSet, basename='product-components'
# )

# # Components -> Raw Materials
# components_router = nested_routers.NestedDefaultRouter(
#     products_router, r'components', lookup='component'
# )
# components_router.register(
#     r'raw-materials', RawMaterialViewSet, basename='component-raw-materials'
# )

# # Packaging -> Packaging Materials
# packaging_router = nested_routers.NestedDefaultRouter(
#     factory_code_router, r'packaging', lookup='packaging'
# )
# packaging_router.register(
#     r'materials', PackagingMaterialViewSet, basename='packaging-materials'
# )


# # =============================================================================
# # URL PATTERNS
# # =============================================================================

# urlpatterns = [
#     # Choice list endpoints
#     path('factory-code/choices/', all_choices, name='all-choices'),
#     path('factory-code/choices/trim-categories/', trim_category_choices, name='trim-category-choices'),
#     path('factory-code/choices/artwork-categories/', artwork_category_choices, name='artwork-category-choices'),
#     path('factory-code/choices/packaging-material-types/', packaging_material_type_choices, name='packaging-material-type-choices'),
#     path('factory-code/choices/work-order-types/', work_order_type_choices, name='work-order-type-choices'),
#     path('factory-code/choices/units/', unit_choices, name='unit-choices'),
#     path('factory-code/choices/size-units/', size_unit_choices, name='size-unit-choices'),
#     path('factory-code/choices/approvals/', approval_choices, name='approval-choices'),
#     path('factory-code/choices/approval-against/', approval_against_choices, name='approval-against-choices'),
    
#     # Field schema endpoints
#     path('factory-code/schemas/', all_field_schemas, name='all-field-schemas'),
#     path('factory-code/schemas/trim-fields/', trim_category_fields, name='trim-category-fields'),
#     path('factory-code/schemas/trim-fields/<str:category>/', trim_category_fields, name='trim-category-fields-detail'),
#     path('factory-code/schemas/artwork-fields/', artwork_category_fields, name='artwork-category-fields'),
#     path('factory-code/schemas/artwork-fields/<str:category>/', artwork_category_fields, name='artwork-category-fields-detail'),
#     path('factory-code/schemas/packaging-fields/', packaging_material_fields, name='packaging-material-fields'),
#     path('factory-code/schemas/packaging-fields/<str:material_type>/', packaging_material_fields, name='packaging-material-fields-detail'),
    
#     # Router URLs
#     path('', include(router.urls)),
#     path('', include(factory_code_router.urls)),
#     path('', include(products_router.urls)),
#     path('', include(components_router.urls)),
#     path('', include(packaging_router.urls)),
# ]


# # =============================================================================
# # API DOCUMENTATION
# # =============================================================================
# """
# API Endpoints Summary:

# CHOICE LISTS (for frontend dropdowns):
# --------------------------------------
# GET  /api/factory-code/choices/                    -> All choices in one response
# GET  /api/factory-code/choices/trim-categories/    -> 30 trim categories
# GET  /api/factory-code/choices/artwork-categories/ -> 18 artwork categories
# GET  /api/factory-code/choices/packaging-material-types/ -> 8 packaging types
# GET  /api/factory-code/choices/work-order-types/   -> Work order process types
# GET  /api/factory-code/choices/units/              -> Unit choices
# GET  /api/factory-code/choices/size-units/         -> Size unit choices
# GET  /api/factory-code/choices/approvals/          -> Approval choices
# GET  /api/factory-code/choices/approval-against/   -> Approval against choices

# FIELD SCHEMAS (for dynamic form rendering):
# -------------------------------------------
# GET  /api/factory-code/schemas/                    -> All schemas
# GET  /api/factory-code/schemas/trim-fields/        -> All trim category field schemas
# GET  /api/factory-code/schemas/trim-fields/{category}/ -> Specific trim category schema
# GET  /api/factory-code/schemas/artwork-fields/     -> All artwork category field schemas
# GET  /api/factory-code/schemas/artwork-fields/{category}/ -> Specific artwork category schema
# GET  /api/factory-code/schemas/packaging-fields/   -> All packaging material field schemas
# GET  /api/factory-code/schemas/packaging-fields/{type}/ -> Specific packaging type schema

# FACTORY CODE CRUD:
# ------------------
# GET    /api/factory-codes/                         -> List all factory codes
# POST   /api/factory-codes/                         -> Create factory code (Step 0)
# GET    /api/factory-codes/{id}/                    -> Retrieve factory code
# PUT    /api/factory-codes/{id}/                    -> Update factory code
# PATCH  /api/factory-codes/{id}/                    -> Partial update
# DELETE /api/factory-codes/{id}/                    -> Delete factory code
# GET    /api/factory-codes/{id}/complete/           -> Full factory code with all nested data
# POST   /api/factory-codes/wizard/                  -> Create complete factory code from wizard

# PRODUCTS (Step 1):
# ------------------
# GET    /api/factory-codes/{id}/products/           -> List products
# POST   /api/factory-codes/{id}/products/           -> Create product
# GET    /api/factory-codes/{id}/products/{pid}/     -> Retrieve product
# PUT    /api/factory-codes/{id}/products/{pid}/     -> Update product
# DELETE /api/factory-codes/{id}/products/{pid}/     -> Delete product

# COMPONENTS (Step 1 - nested under products):
# --------------------------------------------
# GET    /api/factory-codes/{id}/products/{pid}/components/
# POST   /api/factory-codes/{id}/products/{pid}/components/
# GET    /api/factory-codes/{id}/products/{pid}/components/{cid}/
# PUT    /api/factory-codes/{id}/products/{pid}/components/{cid}/
# DELETE /api/factory-codes/{id}/products/{pid}/components/{cid}/

# RAW MATERIALS (Step 2 - nested under components):
# -------------------------------------------------
# GET    /api/factory-codes/{id}/products/{pid}/components/{cid}/raw-materials/
# POST   /api/factory-codes/{id}/products/{pid}/components/{cid}/raw-materials/
# GET    /api/factory-codes/{id}/products/{pid}/components/{cid}/raw-materials/{rid}/
# PUT    /api/factory-codes/{id}/products/{pid}/components/{cid}/raw-materials/{rid}/
# DELETE /api/factory-codes/{id}/products/{pid}/components/{cid}/raw-materials/{rid}/

# CONSUMPTION MATERIALS / TRIMS (Step 3):
# ---------------------------------------
# GET    /api/factory-codes/{id}/consumption-materials/      -> List (filter: ?category=ZIPPERS)
# POST   /api/factory-codes/{id}/consumption-materials/      -> Create
# POST   /api/factory-codes/{id}/consumption-materials/bulk_create/ -> Bulk create
# GET    /api/factory-codes/{id}/consumption-materials/{mid}/ -> Retrieve
# PUT    /api/factory-codes/{id}/consumption-materials/{mid}/ -> Update
# DELETE /api/factory-codes/{id}/consumption-materials/{mid}/ -> Delete

# ARTWORK MATERIALS (Step 4):
# ---------------------------
# GET    /api/factory-codes/{id}/artwork-materials/          -> List (filter: ?category=MAIN LABELS)
# POST   /api/factory-codes/{id}/artwork-materials/          -> Create
# POST   /api/factory-codes/{id}/artwork-materials/bulk_create/ -> Bulk create
# GET    /api/factory-codes/{id}/artwork-materials/{mid}/    -> Retrieve
# PUT    /api/factory-codes/{id}/artwork-materials/{mid}/    -> Update
# DELETE /api/factory-codes/{id}/artwork-materials/{mid}/    -> Delete

# PACKAGING (Step 5):
# -------------------
# GET    /api/factory-codes/{id}/packaging/                  -> List (usually one)
# POST   /api/factory-codes/{id}/packaging/                  -> Create
# GET    /api/factory-codes/{id}/packaging/{pid}/            -> Retrieve
# PUT    /api/factory-codes/{id}/packaging/{pid}/            -> Update
# DELETE /api/factory-codes/{id}/packaging/{pid}/            -> Delete

# PACKAGING MATERIALS (Step 5 - nested):
# --------------------------------------
# GET    /api/factory-codes/{id}/packaging/{pid}/materials/
# POST   /api/factory-codes/{id}/packaging/{pid}/materials/
# GET    /api/factory-codes/{id}/packaging/{pid}/materials/{mid}/
# PUT    /api/factory-codes/{id}/packaging/{pid}/materials/{mid}/
# DELETE /api/factory-codes/{id}/packaging/{pid}/materials/{mid}/
# """

"""
Inventory Management URLs - Unified
====================================

Combines:
- Core IMS routes (departments, segments, buyer-codes, vendor-codes)
- Factory Code routes (with nested routers)
- IPO, Purchase Orders, Company Essentials (NEW)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers

from .views import (
    # Core IMS ViewSets
    DepartmentViewSet, SegmentViewSet, department_menu_structure,
    BuyerCodeViewSet, VendorCodeViewSet,
    # Factory Code ViewSets
    FactoryCodeViewSet,
    ProductViewSet,
    ComponentViewSet,
    RawMaterialViewSet,
    ConsumptionMaterialViewSet,
    ArtworkMaterialViewSet,
    PackagingViewSet,
    PackagingMaterialViewSet,
    # Factory Code choice/schema endpoints
    all_choices,
    trim_category_choices,
    artwork_category_choices,
    packaging_material_type_choices,
    work_order_type_choices,
    unit_choices,
    size_unit_choices,
    approval_choices,
    approval_against_choices,
    all_field_schemas,
    trim_category_fields,
    artwork_category_fields,
    packaging_material_fields,
    # NEW ViewSets
    InternalPurchaseOrderViewSet,
    PurchaseOrderViewSet,
    CompanyEssentialViewSet,
)


# =============================================================================
# MAIN ROUTER
# =============================================================================

router = DefaultRouter()

# Core IMS
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'segments', SegmentViewSet, basename='segment')
router.register(r'buyer-codes', BuyerCodeViewSet, basename='buyer-code')
router.register(r'vendor-codes', VendorCodeViewSet, basename='vendor-code')

# Factory Codes
router.register(r'factory-codes', FactoryCodeViewSet, basename='factory-code')

# NEW: IPOs, Purchase Orders, Company Essentials
router.register(r'ipos', InternalPurchaseOrderViewSet, basename='ipo')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-order')
router.register(r'company-essentials', CompanyEssentialViewSet, basename='company-essential')


# =============================================================================
# NESTED ROUTERS (Factory Code hierarchy)
# =============================================================================

factory_code_router = nested_routers.NestedDefaultRouter(
    router, r'factory-codes', lookup='factory_code'
)
factory_code_router.register(r'products', ProductViewSet, basename='factory-code-products')
factory_code_router.register(r'consumption-materials', ConsumptionMaterialViewSet, basename='factory-code-consumption-materials')
factory_code_router.register(r'artwork-materials', ArtworkMaterialViewSet, basename='factory-code-artwork-materials')
factory_code_router.register(r'packaging', PackagingViewSet, basename='factory-code-packaging')

products_router = nested_routers.NestedDefaultRouter(factory_code_router, r'products', lookup='product')
products_router.register(r'components', ComponentViewSet, basename='product-components')

components_router = nested_routers.NestedDefaultRouter(products_router, r'components', lookup='component')
components_router.register(r'raw-materials', RawMaterialViewSet, basename='component-raw-materials')

packaging_router = nested_routers.NestedDefaultRouter(factory_code_router, r'packaging', lookup='packaging')
packaging_router.register(r'materials', PackagingMaterialViewSet, basename='packaging-materials')


# =============================================================================
# URL PATTERNS
# =============================================================================

urlpatterns = [
    # Core IMS
    path('menu-structure/', department_menu_structure, name='department-menu-structure'),

    # Factory Code choices
    path('factory-code/choices/', all_choices, name='all-choices'),
    path('factory-code/choices/trim-categories/', trim_category_choices, name='trim-category-choices'),
    path('factory-code/choices/artwork-categories/', artwork_category_choices, name='artwork-category-choices'),
    path('factory-code/choices/packaging-material-types/', packaging_material_type_choices, name='packaging-material-type-choices'),
    path('factory-code/choices/work-order-types/', work_order_type_choices, name='work-order-type-choices'),
    path('factory-code/choices/units/', unit_choices, name='unit-choices'),
    path('factory-code/choices/size-units/', size_unit_choices, name='size-unit-choices'),
    path('factory-code/choices/approvals/', approval_choices, name='approval-choices'),
    path('factory-code/choices/approval-against/', approval_against_choices, name='approval-against-choices'),

    # Factory Code schemas
    path('factory-code/schemas/', all_field_schemas, name='all-field-schemas'),
    path('factory-code/schemas/trim-fields/', trim_category_fields, name='trim-category-fields'),
    path('factory-code/schemas/trim-fields/<str:category>/', trim_category_fields, name='trim-category-fields-detail'),
    path('factory-code/schemas/artwork-fields/', artwork_category_fields, name='artwork-category-fields'),
    path('factory-code/schemas/artwork-fields/<str:category>/', artwork_category_fields, name='artwork-category-fields-detail'),
    path('factory-code/schemas/packaging-fields/', packaging_material_fields, name='packaging-material-fields'),
    path('factory-code/schemas/packaging-fields/<str:material_type>/', packaging_material_fields, name='packaging-material-fields-detail'),

    # All router URLs
    path('', include(router.urls)),
    path('', include(factory_code_router.urls)),
    path('', include(products_router.urls)),
    path('', include(components_router.urls)),
    path('', include(packaging_router.urls)),
]
