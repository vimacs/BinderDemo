"""
Factory Code API Schema - V2
=============================

drf-spectacular schema extensions for comprehensive Swagger/OpenAPI documentation.
Provides detailed API documentation with examples and schema extensions.
"""

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample,
    OpenApiResponse, inline_serializer
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


# =============================================================================
# SCHEMA EXTENSIONS FOR VIEWS
# =============================================================================

# Note: Apply these decorators to the ViewSets in factory_code_views.py
# This file provides the schema definitions and examples

# =============================================================================
# EXAMPLE REQUEST/RESPONSE DATA
# =============================================================================

# Step 0: Factory Code Examples
FACTORY_CODE_CREATE_EXAMPLE = {
    "type": "RUG",
    "buyer": "IKEA",
    "style_no": "STOCKHOLM-2024-001",
    "style_name": "Stockholm Collection Rug",
    "size": "160x230",
    "gsm": "2500",
    "article_description": "Hand-woven wool rug with traditional pattern",
    "colour": "Natural Beige"
}

FACTORY_CODE_RESPONSE_EXAMPLE = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "code": "FC-2024-001",
    "type": "RUG",
    "buyer": "IKEA",
    "style_no": "STOCKHOLM-2024-001",
    "style_name": "Stockholm Collection Rug",
    "size": "160x230",
    "gsm": "2500",
    "article_description": "Hand-woven wool rug with traditional pattern",
    "colour": "Natural Beige",
    "reference_image": None,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}

# Step 3: Consumption Material (Trims) Examples
CONSUMPTION_MATERIAL_ZIPPER_EXAMPLE = {
    "category": "ZIPPERS",
    "zipNumber": "5",
    "zipType": "Metal",
    "zipMaterial": "Brass",
    "sliderType": "Auto Lock",
    "zipColour": "Antique Brass",
    "tapeColour": "Black",
    "endType": "Closed End",
    "sizeWidth": "2.5",
    "sizeLength": "50",
    "sizeUnit": "CMS",
    "testingRequirement": "Pull strength test required",
    "lengthQuantity": "100",
    "surplus": "5%",
    "approval": "PP",
    "remarks": "Must match sample #ZP-2024-001"
}

CONSUMPTION_MATERIAL_VELCRO_EXAMPLE = {
    "category": "VELCRO",
    "velcroType": "Sew-on",
    "velcroMaterial": "Nylon",
    "velcroWidth": "25",
    "velcroColour": "White",
    "adhesiveBacked": False,
    "hooksLoops": "Both",
    "sizeLength": "100",
    "sizeUnit": "CMS",
    "lengthQuantity": "50 meters",
    "surplus": "10%",
    "approval": "BUYER'S"
}

CONSUMPTION_MATERIAL_RFID_EXAMPLE = {
    "category": "RFID / EAS TAGS",
    "rfidType": "UHF RFID",
    "formFactor": "Label/Sticker",
    "frequency": "860-960 MHz",
    "chipIcType": "Impinj Monza R6",
    "rfidSize": "50x30mm",
    "coding": "EPC Gen2",
    "security": "Password Protected",
    "lengthQuantity": "1000 pcs",
    "approval": "BUYER'S"
}

# Step 4: Artwork Material Examples
ARTWORK_MAIN_LABEL_EXAMPLE = {
    "category": "MAIN LABELS",
    "specificType": "Woven Damask",
    "material": "100% Polyester",
    "sizeShape": "40mm x 20mm",
    "content": "Brand name, Made in India, Care symbols",
    "colours": "White background, Black text",
    "finishing": "Heat cut edges",
    "permanence": "Washable",
    "surplus": "5%",
    "approval": "PP"
}

ARTWORK_HANG_TAG_EXAMPLE = {
    "category": "HANG TAGS",
    "specificType": "Die-cut shaped",
    "material": "350 GSM Coated Art Card",
    "sizeShape": "100mm x 50mm with hole",
    "content": "Brand, Price, Barcode, Product info",
    "colours": "4C+4C CMYK",
    "finishing": "Matte lamination, Spot UV",
    "permanence": "N/A",
    "surplus": "10%",
    "approval": "BUYER'S"
}

# Step 5: Packaging Examples
PACKAGING_CREATE_EXAMPLE = {
    "packing_method": "FLAT PACK",
    "polybag_type": "Individual",
    "silica_gel": True,
    "remarks": "Each piece in individual polybag, 10 pcs per carton",
    "materials": [
        {
            "materialType": "CARTONS/CORRUGATED BOX",
            "sizeWidth": "60",
            "sizeLength": "40",
            "sizeHeight": "30",
            "sizeUnit": "CMS",
            "colour": "Brown Kraft",
            "printing": "1C Black - Logo and shipping marks",
            "noOfPlys": "5 PLY",
            "jointType": "STAPLE",
            "burstingStrength": "175 LBS"
        },
        {
            "materialType": "POLY BAG WITH FLAP",
            "sizeWidth": "55",
            "sizeLength": "35",
            "sizeUnit": "CMS",
            "colour": "Transparent",
            "printing": "1C - Warning text",
            "guage": "200",
            "gummingQuality": "Standard",
            "punchHoles": "2 holes"
        }
    ]
}


# =============================================================================
# INLINE SERIALIZERS FOR SCHEMA DOCUMENTATION
# =============================================================================

class ChoiceItemSerializer(serializers.Serializer):
    """Schema for choice list items"""
    value = serializers.CharField(help_text="The value to submit")
    label = serializers.CharField(help_text="Human-readable label for display")


class ChoiceListResponseSerializer(serializers.Serializer):
    """Schema for choice list responses"""
    choices = ChoiceItemSerializer(many=True)
    count = serializers.IntegerField()


class AllChoicesResponseSerializer(serializers.Serializer):
    """Schema for all-choices endpoint response"""
    trimCategories = ChoiceItemSerializer(many=True)
    artworkCategories = ChoiceItemSerializer(many=True)
    packagingMaterialTypes = ChoiceItemSerializer(many=True)
    workOrderTypes = ChoiceItemSerializer(many=True)
    units = ChoiceItemSerializer(many=True)
    sizeUnits = ChoiceItemSerializer(many=True)
    approvals = ChoiceItemSerializer(many=True)
    approvalAgainst = ChoiceItemSerializer(many=True)


class FieldSchemaSerializer(serializers.Serializer):
    """Schema for category field definitions"""
    fields = serializers.ListField(child=serializers.CharField())
    placeholders = serializers.DictField(required=False)
    options = serializers.DictField(required=False)


class TrimFieldsResponseSerializer(serializers.Serializer):
    """Schema for trim category fields response"""
    schemas = serializers.DictField(child=FieldSchemaSerializer())
    count = serializers.IntegerField()


class SizeSerializer(serializers.Serializer):
    """Schema for nested size object"""
    width = serializers.CharField(required=False, allow_blank=True)
    length = serializers.CharField(required=False, allow_blank=True)
    height = serializers.CharField(required=False, allow_blank=True)
    unit = serializers.ChoiceField(choices=['CMS', 'INCHES', 'MM'], required=False)


class BulkCreateResponseSerializer(serializers.Serializer):
    """Schema for bulk create responses"""
    created = serializers.ListField()
    errors = serializers.ListField()
    created_count = serializers.IntegerField()
    error_count = serializers.IntegerField()


# =============================================================================
# SCHEMA TAGS
# =============================================================================

SCHEMA_TAGS = [
    {
        "name": "Factory Codes",
        "description": "Main factory code management (Step 0: Product Identification)"
    },
    {
        "name": "Products & Components",
        "description": "Product and component specifications (Step 1: Cut & Sew)"
    },
    {
        "name": "Raw Materials",
        "description": "Raw material specifications with work orders (Step 2)"
    },
    {
        "name": "Consumption Materials",
        "description": "Trims & Accessories - 30 categories (Step 3)"
    },
    {
        "name": "Artwork Materials",
        "description": "Artwork & Labeling - 18 categories (Step 4)"
    },
    {
        "name": "Packaging",
        "description": "Packaging specifications - 8 material types (Step 5)"
    },
    {
        "name": "Choices",
        "description": "Dropdown choice lists for form fields"
    },
    {
        "name": "Schemas",
        "description": "Field schemas for dynamic form rendering"
    }
]


# =============================================================================
# SPECTACULAR SETTINGS EXTENSION
# =============================================================================

SPECTACULAR_SETTINGS_EXTENSION = {
    'TITLE': 'Factory Code API - V2',
    'DESCRIPTION': '''
## Factory Code Module API

Comprehensive API for the 6-step Factory Code generation wizard in the Binder ERP system.

### Steps Overview

1. **Step 0: Product Identification** - Basic factory code details (buyer, style, etc.)
2. **Step 1: Cut & Sew Specification** - Product components and sizes
3. **Step 2: Raw Material Sourcing** - Raw materials with work order processes
4. **Step 3: Trims & Accessories** - 30 trim categories with conditional fields
5. **Step 4: Artwork & Labeling** - 18 artwork categories
6. **Step 5: Packaging** - 8 packaging material types

### Key Features

- **Multi-tenant Support**: All data is tenant-scoped
- **Conditional Fields**: Category-specific fields stored in JSONField
- **File Uploads**: Support for reference images, testing documents
- **Bulk Operations**: Batch create for consumption/artwork materials
- **Complete Retrieval**: Get entire factory code with all nested data

### Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Choice Lists

Before rendering forms, fetch choice lists from `/api/factory-code/choices/` 
to populate dropdowns.

### Field Schemas

For dynamic form rendering based on selected category, fetch field schemas 
from `/api/factory-code/schemas/`.
    ''',
    'VERSION': '2.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'TAGS': SCHEMA_TAGS,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/',
}


# =============================================================================
# SCHEMA DECORATORS FOR VIEWSETS
# =============================================================================

# These decorators should be applied to the ViewSets in factory_code_views.py
# Example usage:

"""
from .factory_code_schema import (
    factory_code_viewset_schema,
    consumption_material_viewset_schema
)

@factory_code_viewset_schema
class FactoryCodeViewSet(viewsets.ModelViewSet):
    ...
"""

factory_code_list_schema = extend_schema(
    summary="List all factory codes",
    description="Returns paginated list of factory codes for the current tenant.",
    tags=["Factory Codes"],
    responses={200: OpenApiTypes.OBJECT}
)

factory_code_create_schema = extend_schema(
    summary="Create a new factory code",
    description="Creates a new factory code (Step 0: Product Identification).",
    tags=["Factory Codes"],
    examples=[
        OpenApiExample(
            "Create Factory Code",
            value=FACTORY_CODE_CREATE_EXAMPLE,
            request_only=True
        ),
        OpenApiExample(
            "Factory Code Response",
            value=FACTORY_CODE_RESPONSE_EXAMPLE,
            response_only=True
        )
    ]
)

consumption_material_create_schema = extend_schema(
    summary="Create a consumption material (trim)",
    description="""
Creates a new consumption material for the specified factory code.

The `category` field determines which additional fields are required.
Use the `/api/factory-code/schemas/trim-fields/{category}/` endpoint
to get the field schema for a specific category.

### Available Categories (30 total):
- ZIPPERS, VELCRO, STITCHING THREAD, BUTTONS, RIVETS
- NIWAR (Webbing/Tapes), LACE, INTERLINING/FUSING
- HOOKS & EYES, BUCKLES & ADJUSTERS, EYELETS & GROMMETS
- ELASTIC, FELT, SHOULDER PADS, TUBULAR KNITS / RIBBING
- RFID / EAS TAGS, PLASTIC CABLE TIES / LOOPS
- FRINGE / TASSELS, PLASTIC PIPES / RODS, SEAM SEALING TAPE
- ADHESIVES / GUNNING, PRE-CUT HEMS / BINDINGS
- REFLECTIVE TAPES / TRIMS, FIRE RETARDANT (FR) TRIMS
- REPAIR KITS / PATCHES, CORD STOPS / CORD LOCKS / TOGGLES
- D-RINGS / O-RINGS / WEBBING LOOPS, FOAM / WADDING (Pre-Cut Shapes)
- PINS / TAGGING BARBS, MAGNETIC CLOSURES / SNAPS
    """,
    tags=["Consumption Materials"],
    examples=[
        OpenApiExample(
            "Create Zipper",
            value=CONSUMPTION_MATERIAL_ZIPPER_EXAMPLE,
            request_only=True
        ),
        OpenApiExample(
            "Create Velcro",
            value=CONSUMPTION_MATERIAL_VELCRO_EXAMPLE,
            request_only=True
        ),
        OpenApiExample(
            "Create RFID Tag",
            value=CONSUMPTION_MATERIAL_RFID_EXAMPLE,
            request_only=True
        )
    ]
)

artwork_material_create_schema = extend_schema(
    summary="Create an artwork material",
    description="""
Creates a new artwork material for the specified factory code.

### Available Categories (18 total):
- MAIN LABELS, CARE LABELS, SIZE LABELS, FLAG LABELS
- HANG TAGS, BARCODE STICKERS, PRINTED FABRIC LABELS
- WOVEN LABELS, INSERT CARDS, RIBBONS
- SECURITY SEALS / TAMPER TAGS, HEAT TRANSFER LABELS / PRINTS
- PRINTED / BRANDED STRAPS / BELTS, EMBROIDERED BADGES / PATCHES
- LEATHER / PU PATCHES, METAL CHARMS / LOGO PLATES
- EMBROIDERY THREAD / DESIGN, SCREEN PRINT / TRANSFERS
- PRICE TAGS / JOKER TAGS
    """,
    tags=["Artwork Materials"],
    examples=[
        OpenApiExample(
            "Create Main Label",
            value=ARTWORK_MAIN_LABEL_EXAMPLE,
            request_only=True
        ),
        OpenApiExample(
            "Create Hang Tag",
            value=ARTWORK_HANG_TAG_EXAMPLE,
            request_only=True
        )
    ]
)

packaging_create_schema = extend_schema(
    summary="Create packaging specification",
    description="""
Creates packaging specification with nested materials for the factory code.

### Available Material Types (8 total):
- CARTONS/CORRUGATED BOX
- MASTER CARTONS
- INNER CARTONS
- POLY BAG WITH FLAP
- POLYSHEET
- BALE WRAP
- TAPE
- TISSUE / WRAPPING PAPER
    """,
    tags=["Packaging"],
    examples=[
        OpenApiExample(
            "Create Packaging with Materials",
            value=PACKAGING_CREATE_EXAMPLE,
            request_only=True
        )
    ]
)

all_choices_schema = extend_schema(
    summary="Get all choice lists",
    description="Returns all dropdown choice lists in a single response for frontend initialization.",
    tags=["Choices"],
    responses={200: AllChoicesResponseSerializer}
)

trim_category_choices_schema = extend_schema(
    summary="Get trim category choices",
    description="Returns list of all 30 trim/accessory categories for Step 3 dropdown.",
    tags=["Choices"],
    responses={200: ChoiceListResponseSerializer}
)

trim_fields_schema = extend_schema(
    summary="Get trim category field schemas",
    description="Returns field definitions for all or specific trim categories.",
    tags=["Schemas"],
    parameters=[
        OpenApiParameter(
            name="category",
            type=str,
            location=OpenApiParameter.PATH,
            description="Specific trim category (URL encoded)",
            required=False
        )
    ],
    responses={200: TrimFieldsResponseSerializer}
)

bulk_create_schema = extend_schema(
    summary="Bulk create items",
    description="Create multiple items in a single request.",
    tags=["Consumption Materials"],
    request=inline_serializer(
        name="BulkCreateRequest",
        fields={
            "items": serializers.ListField(help_text="Array of items to create")
        }
    ),
    responses={
        201: BulkCreateResponseSerializer,
        400: BulkCreateResponseSerializer
    }
)