# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404
# from django.db.models import Q

# from .models import Department, Segment, BuyerCode, VendorCode
# from .serializers import (
#     DepartmentSerializer, DepartmentListSerializer, DepartmentCreateSerializer,
#     SegmentSerializer, SegmentDetailSerializer,
#     BuyerCodeSerializer, BuyerCodeCreateSerializer, BuyerCodeListSerializer,
#     VendorCodeSerializer, VendorCodeCreateSerializer, VendorCodeListSerializer
# )


# class DepartmentViewSet(ModelViewSet):
#     """
#     ViewSet for Department CRUD operations
#     """
#     permission_classes = [IsAuthenticated]
#     queryset = Department.objects.all()
    
#     def get_serializer_class(self):
#         """Return appropriate serializer based on action"""
#         if self.action == 'list':
#             return DepartmentListSerializer
#         elif self.action == 'create':
#             return DepartmentCreateSerializer
#         return DepartmentSerializer
    
#     def get_queryset(self):
#         """Filter departments based on tenant if user is not master admin"""
#         queryset = Department.objects.all()
        
#         # Filter by tenant if user is not master admin
#         user = self.request.user
#         if not user.is_master_admin and user.tenant:
#             queryset = queryset.filter(
#                 Q(tenant=user.tenant) | Q(tenant__isnull=True)
#             )
        
#         # Filter by active status if requested
#         is_active = self.request.query_params.get('is_active')
#         if is_active is not None:
#             queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
#         # Search functionality
#         search = self.request.query_params.get('search')
#         if search:
#             queryset = queryset.filter(
#                 Q(name__icontains=search) |
#                 Q(code__icontains=search) |
#                 Q(description__icontains=search)
#             )
        
#         return queryset.select_related('tenant', 'created_by').prefetch_related('segments')
    
#     def perform_create(self, serializer):
#         """Set created_by to current user"""
#         serializer.save(created_by=self.request.user)
    
#     @action(detail=True, methods=['get'])
#     def segments(self, request, pk=None):
#         """Get all segments for a department"""
#         department = self.get_object()
#         segments = department.segments.all()
#         serializer = SegmentDetailSerializer(segments, many=True)
#         return Response({
#             'status': 'success',
#             'data': serializer.data
#         })
    
#     @action(detail=True, methods=['post'])
#     def add_segment(self, request, pk=None):
#         """Add a segment to a department"""
#         department = self.get_object()
#         serializer = SegmentSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save(department=department, created_by=request.user)
#             return Response({
#                 'status': 'success',
#                 'message': 'Segment added successfully',
#                 'data': serializer.data
#             }, status=status.HTTP_201_CREATED)
        
#         return Response({
#             'status': 'error',
#             'message': 'Failed to add segment',
#             'data': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)


# class SegmentViewSet(ModelViewSet):
#     """
#     ViewSet for Segment CRUD operations
#     """
#     permission_classes = [IsAuthenticated]
#     queryset = Segment.objects.all()
#     serializer_class = SegmentSerializer
    
#     def get_serializer_class(self):
#         """Return appropriate serializer based on action"""
#         if self.action == 'retrieve':
#             return SegmentDetailSerializer
#         return SegmentSerializer
    
#     def get_queryset(self):
#         """Filter segments based on department and tenant"""
#         queryset = Segment.objects.all()
        
#         # Filter by department if provided
#         department_id = self.request.query_params.get('department')
#         if department_id:
#             queryset = queryset.filter(department_id=department_id)
        
#         # Filter by active status if requested
#         is_active = self.request.query_params.get('is_active')
#         if is_active is not None:
#             queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
#         # Filter by tenant if user is not master admin
#         user = self.request.user
#         if not user.is_master_admin and user.tenant:
#             queryset = queryset.filter(
#                 Q(department__tenant=user.tenant) | Q(department__tenant__isnull=True)
#             )
        
#         # Search functionality
#         search = self.request.query_params.get('search')
#         if search:
#             queryset = queryset.filter(
#                 Q(name__icontains=search) |
#                 Q(code__icontains=search) |
#                 Q(description__icontains=search)
#             )
        
#         return queryset.select_related('department', 'department__tenant', 'created_by')
    
#     def perform_create(self, serializer):
#         """Set created_by to current user"""
#         serializer.save(created_by=self.request.user)
    
#     def create(self, request, *args, **kwargs):
#         """Create a segment"""
#         serializer = self.get_serializer(data=request.data)
        
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response({
#                 'status': 'success',
#                 'message': 'Segment created successfully',
#                 'data': SegmentDetailSerializer(serializer.instance).data
#             }, status=status.HTTP_201_CREATED)
        
#         return Response({
#             'status': 'error',
#             'message': 'Failed to create segment',
#             'data': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     def update(self, request, *args, **kwargs):
#         """Update a segment"""
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
#         if serializer.is_valid():
#             self.perform_update(serializer)
#             return Response({
#                 'status': 'success',
#                 'message': 'Segment updated successfully',
#                 'data': SegmentDetailSerializer(serializer.instance).data
#             })
        
#         return Response({
#             'status': 'error',
#             'message': 'Failed to update segment',
#             'data': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, *args, **kwargs):
#         """Delete a segment"""
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response({
#             'status': 'success',
#             'message': 'Segment deleted successfully'
#         }, status=status.HTTP_200_OK)


# # Additional API views for convenience
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def department_menu_structure(request):
#     """
#     Get complete department menu structure with segments
#     Useful for frontend menu rendering
#     """
#     departments = Department.objects.filter(is_active=True).prefetch_related(
#         'segments'
#     ).order_by('display_order', 'name')
    
#     menu_data = []
#     for dept in departments:
#         segments = dept.segments.filter(is_active=True).order_by('display_order', 'name')
#         menu_data.append({
#             'id': str(dept.id),
#             'code': dept.code,
#             'label': dept.name,
#             'hasSubMenu': segments.exists(),
#             'segments': [
#                 {
#                     'id': str(seg.id),
#                     'code': seg.code,
#                     'label': seg.name
#                 }
#                 for seg in segments
#             ]
#         })
    
#     return Response({
#         'status': 'success',
#         'data': menu_data
#     })


# class BuyerCodeViewSet(ModelViewSet):
#     """
#     ViewSet for BuyerCode CRUD operations
#     Handles buyer code generation with auto-incrementing codes (101A, 102A, etc.)
#     """
#     permission_classes = [IsAuthenticated]
#     queryset = BuyerCode.objects.all()
    
#     def get_serializer_class(self):
#         """Return appropriate serializer based on action"""
#         if self.action == 'list':
#             return BuyerCodeListSerializer
#         elif self.action == 'create':
#             return BuyerCodeCreateSerializer
#         return BuyerCodeSerializer
    
#     def get_queryset(self):
#         """Filter buyer codes based on tenant if user is not master admin"""
#         queryset = BuyerCode.objects.all()
        
#         # Filter by tenant if user is not master admin
#         user = self.request.user
#         if not user.is_master_admin and user.tenant:
#             queryset = queryset.filter(tenant=user.tenant)
        
#         # Search functionality
#         search = self.request.query_params.get('search')
#         if search:
#             queryset = queryset.filter(
#                 Q(buyer_name__icontains=search) |
#                 Q(code__icontains=search) |
#                 Q(retailer__icontains=search) |
#                 Q(contact_person__icontains=search)
#             )
        
#         return queryset.select_related('tenant', 'created_by')
    
#     def create(self, request, *args, **kwargs):
#         """Create a new buyer code with auto-generated code"""
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Create buyer code (code will be auto-generated)
#         buyer_code = serializer.save()
        
#         return Response({
#             'status': 'success',
#             'message': 'Buyer code generated successfully',
#             'data': BuyerCodeSerializer(buyer_code).data
#         }, status=status.HTTP_201_CREATED)
    
#     def update(self, request, *args, **kwargs):
#         """Update a buyer code (code cannot be changed)"""
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
        
#         # Remove code from request data if present (code is read-only)
#         request_data = request.data.copy()
#         if 'code' in request_data:
#             request_data.pop('code')
        
#         serializer = self.get_serializer(instance, data=request_data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
        
#         return Response({
#             'status': 'success',
#             'message': 'Buyer code updated successfully',
#             'data': BuyerCodeSerializer(serializer.instance).data
#         })
    
#     def destroy(self, request, *args, **kwargs):
#         """Delete a buyer code"""
#         instance = self.get_object()
#         code = instance.code
#         self.perform_destroy(instance)
        
#         return Response({
#             'status': 'success',
#             'message': f'Buyer code {code} deleted successfully'
#         }, status=status.HTTP_200_OK)
    
#     @action(detail=False, methods=['get'])
#     def generate(self, request):
#         """
#         Preview the next buyer code that would be generated
#         Useful for frontend to show what code will be generated
#         """
#         user = request.user
#         tenant = user.tenant if user and not user.is_master_admin else None
        
#         next_code = BuyerCode.generate_next_code(tenant=tenant)
        
#         return Response({
#             'status': 'success',
#             'data': {
#                 'next_code': next_code
#             }
#         })
    
#     @action(detail=False, methods=['get'], url_path='master-sheet')
#     def master_sheet(self, request):
#         """
#         Get all buyer codes in master sheet format
#         Returns all buyer codes formatted for frontend master sheet display
#         """
#         queryset = self.get_queryset()
        
#         # Format data for frontend
#         buyer_codes = []
#         for buyer in queryset:
#             buyer_codes.append({
#                 'code': buyer.code,
#                 'buyerName': buyer.buyer_name,
#                 'buyerAddress': buyer.buyer_address,
#                 'contactPerson': buyer.contact_person,
#                 'retailer': buyer.retailer,
#                 'createdAt': buyer.created_at.isoformat() if buyer.created_at else None
#             })
        
#         return Response({
#             'status': 'success',
#             'data': buyer_codes,
#             'count': len(buyer_codes)
#         })


# class VendorCodeViewSet(ModelViewSet):
#     """
#     ViewSet for VendorCode CRUD operations
#     Handles vendor code generation with auto-incrementing numeric codes (101, 102, etc.)
#     """
#     permission_classes = [IsAuthenticated]
#     queryset = VendorCode.objects.all()
    
#     def get_serializer_class(self):
#         """Return appropriate serializer based on action"""
#         if self.action == 'list':
#             return VendorCodeListSerializer
#         elif self.action == 'create':
#             return VendorCodeCreateSerializer
#         return VendorCodeSerializer
    
#     def get_queryset(self):
#         """Filter vendor codes based on tenant if user is not master admin"""
#         queryset = VendorCode.objects.all()
        
#         # Filter by tenant if user is not master admin
#         user = self.request.user
#         if not user.is_master_admin and user.tenant:
#             queryset = queryset.filter(tenant=user.tenant)
        
#         # Search functionality
#         search = self.request.query_params.get('search')
#         if search:
#             queryset = queryset.filter(
#                 Q(vendor_name__icontains=search) |
#                 Q(code__icontains=search) |
#                 Q(gst__icontains=search) |
#                 Q(contact_person__icontains=search) |
#                 Q(email__icontains=search) |
#                 Q(job_work_category__icontains=search)
#             )
        
#         return queryset.select_related('tenant', 'created_by')
    
#     def create(self, request, *args, **kwargs):
#         """Create a new vendor code with auto-generated code"""
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Create vendor code (code will be auto-generated)
#         vendor_code = serializer.save()
        
#         return Response({
#             'status': 'success',
#             'message': 'Vendor code generated successfully',
#             'data': VendorCodeSerializer(vendor_code).data
#         }, status=status.HTTP_201_CREATED)
    
#     def update(self, request, *args, **kwargs):
#         """Update a vendor code (code cannot be changed)"""
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
        
#         # Remove code from request data if present (code is read-only)
#         request_data = request.data.copy()
#         if 'code' in request_data:
#             request_data.pop('code')
        
#         serializer = self.get_serializer(instance, data=request_data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
        
#         return Response({
#             'status': 'success',
#             'message': 'Vendor code updated successfully',
#             'data': VendorCodeSerializer(serializer.instance).data
#         })
    
#     def destroy(self, request, *args, **kwargs):
#         """Delete a vendor code"""
#         instance = self.get_object()
#         code = instance.code
#         self.perform_destroy(instance)
        
#         return Response({
#             'status': 'success',
#             'message': f'Vendor code {code} deleted successfully'
#         }, status=status.HTTP_200_OK)
    
#     @action(detail=False, methods=['get'])
#     def generate(self, request):
#         """
#         Preview the next vendor code that would be generated
#         Useful for frontend to show what code will be generated
#         """
#         user = request.user
#         tenant = user.tenant if user and not user.is_master_admin else None
        
#         next_code = VendorCode.generate_next_code(tenant=tenant)
        
#         return Response({
#             'status': 'success',
#             'data': {
#                 'next_code': next_code
#             }
#         })
    
#     @action(detail=False, methods=['get'], url_path='master-sheet')
#     def master_sheet(self, request):
#         """
#         Get all vendor codes in master sheet format
#         Returns all vendor codes formatted for frontend master sheet display
#         """
#         queryset = self.get_queryset()
        
#         # Format data for frontend
#         vendor_codes = []
#         for vendor in queryset:
#             vendor_codes.append({
#                 'code': vendor.code,
#                 'vendorName': vendor.vendor_name,
#                 'address': vendor.address,
#                 'gst': vendor.gst,
#                 'bankName': vendor.bank_name,
#                 'accNo': vendor.account_number,
#                 'ifscCode': vendor.ifsc_code,
#                 'jobWorkCategory': vendor.job_work_category,
#                 'jobWorkSubCategory': vendor.job_work_sub_category,
#                 'contactPerson': vendor.contact_person,
#                 'whatsappNo': vendor.whatsapp_number,
#                 'altWhatsappNo': vendor.alt_whatsapp_number or '',
#                 'email': vendor.email,
#                 'paymentTerms': vendor.payment_terms,
#                 'createdAt': vendor.created_at.isoformat() if vendor.created_at else None
#             })
        
#         return Response({
#             'status': 'success',
#             'data': vendor_codes,
#             'count': len(vendor_codes)
#         })

# """
# Factory Code Views - V2
# ========================

# DRF ViewSets and API Views for the Factory Code module.
# Includes endpoints for:
# - CRUD operations on all models
# - Choice list endpoints for frontend dropdowns
# - Category field schema endpoints for dynamic form rendering
# - Step-by-step wizard endpoints
# """

# from rest_framework import viewsets, status
# from rest_framework.decorators import action, api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# from django.shortcuts import get_object_or_404

# from .models import (
#     FactoryCode, Product, Component, RawMaterial, WorkOrder,
#     ConsumptionMaterial, ArtworkMaterial, Packaging, PackagingMaterial,
#     TrimAccessoryChoices, ArtworkCategoryChoices, PackagingMaterialTypeChoices,
#     WorkOrderTypeChoices, UnitChoices, SizeUnitChoices,
#     ApprovalChoices, ApprovalAgainstChoices,
#     TRIM_CATEGORY_FIELDS_SCHEMA, ARTWORK_CATEGORY_FIELDS_SCHEMA,
#     PACKAGING_MATERIAL_FIELDS_SCHEMA
# )

# from .serializers import (
#     FactoryCodeSerializer, FactoryCodeCreateSerializer,
#     FactoryCodeCompleteSerializer, FactoryCodeWizardCreateSerializer,
#     ProductSerializer, ProductCreateSerializer,
#     ComponentSerializer, ComponentCreateSerializer,
#     RawMaterialSerializer, RawMaterialCreateSerializer,
#     ConsumptionMaterialSerializer, ConsumptionMaterialCreateSerializer,
#     ArtworkMaterialSerializer, ArtworkMaterialCreateSerializer,
#     PackagingSerializer, PackagingCreateSerializer,
#     PackagingMaterialSerializer, PackagingMaterialCreateSerializer
# )


# # =============================================================================
# # UTILITY FUNCTIONS
# # =============================================================================

# def choices_to_list(choices_class):
#     """Convert Django TextChoices to list of {value, label} dicts"""
#     return [{'value': choice.value, 'label': choice.label} for choice in choices_class]


# # =============================================================================
# # CHOICE LIST API VIEWS
# # =============================================================================

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def trim_category_choices(request):
#     """
#     GET /api/factory-code/choices/trim-categories/
#     Returns list of all 30 trim/accessory categories.
#     """
#     return Response({
#         'choices': choices_to_list(TrimAccessoryChoices),
#         'count': len(TrimAccessoryChoices)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def artwork_category_choices(request):
#     """
#     GET /api/factory-code/choices/artwork-categories/
#     Returns list of all 18 artwork categories.
#     """
#     return Response({
#         'choices': choices_to_list(ArtworkCategoryChoices),
#         'count': len(ArtworkCategoryChoices)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def packaging_material_type_choices(request):
#     """
#     GET /api/factory-code/choices/packaging-material-types/
#     Returns list of all 8 packaging material types.
#     """
#     return Response({
#         'choices': choices_to_list(PackagingMaterialTypeChoices),
#         'count': len(PackagingMaterialTypeChoices)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def work_order_type_choices(request):
#     """
#     GET /api/factory-code/choices/work-order-types/
#     Returns list of work order process types.
#     """
#     return Response({
#         'choices': choices_to_list(WorkOrderTypeChoices),
#         'count': len(WorkOrderTypeChoices)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def unit_choices(request):
#     """GET /api/factory-code/choices/units/"""
#     return Response({
#         'choices': choices_to_list(UnitChoices),
#         'count': len(UnitChoices)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def size_unit_choices(request):
#     """GET /api/factory-code/choices/size-units/"""
#     return Response({
#         'choices': choices_to_list(SizeUnitChoices),
#         'count': len(SizeUnitChoices)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def approval_choices(request):
#     """GET /api/factory-code/choices/approvals/"""
#     return Response({
#         'choices': choices_to_list(ApprovalChoices),
#         'count': len(ApprovalChoices)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def approval_against_choices(request):
#     """GET /api/factory-code/choices/approval-against/"""
#     return Response({
#         'choices': choices_to_list(ApprovalAgainstChoices),
#         'count': len(ApprovalAgainstChoices)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def all_choices(request):
#     """
#     GET /api/factory-code/choices/
#     Returns all choice lists for frontend initialization.
#     """
#     return Response({
#         'trimCategories': choices_to_list(TrimAccessoryChoices),
#         'artworkCategories': choices_to_list(ArtworkCategoryChoices),
#         'packagingMaterialTypes': choices_to_list(PackagingMaterialTypeChoices),
#         'workOrderTypes': choices_to_list(WorkOrderTypeChoices),
#         'units': choices_to_list(UnitChoices),
#         'sizeUnits': choices_to_list(SizeUnitChoices),
#         'approvals': choices_to_list(ApprovalChoices),
#         'approvalAgainst': choices_to_list(ApprovalAgainstChoices)
#     })


# # =============================================================================
# # CATEGORY FIELD SCHEMA API VIEWS
# # =============================================================================

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def trim_category_fields(request, category=None):
#     """
#     GET /api/factory-code/schemas/trim-fields/
#     GET /api/factory-code/schemas/trim-fields/{category}/
#     """
#     if category:
#         import urllib.parse
#         category = urllib.parse.unquote(category)
#         if category in TRIM_CATEGORY_FIELDS_SCHEMA:
#             return Response({
#                 'category': category,
#                 'schema': TRIM_CATEGORY_FIELDS_SCHEMA[category]
#             })
#         return Response({'error': f'Unknown trim category: {category}'}, status=404)
#     return Response({
#         'schemas': TRIM_CATEGORY_FIELDS_SCHEMA,
#         'count': len(TRIM_CATEGORY_FIELDS_SCHEMA)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def artwork_category_fields(request, category=None):
#     """
#     GET /api/factory-code/schemas/artwork-fields/
#     GET /api/factory-code/schemas/artwork-fields/{category}/
#     """
#     if category:
#         import urllib.parse
#         category = urllib.parse.unquote(category)
#         if category in ARTWORK_CATEGORY_FIELDS_SCHEMA:
#             return Response({
#                 'category': category,
#                 'schema': ARTWORK_CATEGORY_FIELDS_SCHEMA[category]
#             })
#         return Response({'error': f'Unknown artwork category: {category}'}, status=404)
#     return Response({
#         'schemas': ARTWORK_CATEGORY_FIELDS_SCHEMA,
#         'count': len(ARTWORK_CATEGORY_FIELDS_SCHEMA)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def packaging_material_fields(request, material_type=None):
#     """
#     GET /api/factory-code/schemas/packaging-fields/
#     GET /api/factory-code/schemas/packaging-fields/{material_type}/
#     """
#     if material_type:
#         import urllib.parse
#         material_type = urllib.parse.unquote(material_type)
#         if material_type in PACKAGING_MATERIAL_FIELDS_SCHEMA:
#             return Response({
#                 'materialType': material_type,
#                 'schema': PACKAGING_MATERIAL_FIELDS_SCHEMA[material_type]
#             })
#         return Response({'error': f'Unknown packaging material type: {material_type}'}, status=404)
#     return Response({
#         'schemas': PACKAGING_MATERIAL_FIELDS_SCHEMA,
#         'count': len(PACKAGING_MATERIAL_FIELDS_SCHEMA)
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def all_field_schemas(request):
#     """GET /api/factory-code/schemas/ - Returns all field schemas."""
#     return Response({
#         'trimFields': TRIM_CATEGORY_FIELDS_SCHEMA,
#         'artworkFields': ARTWORK_CATEGORY_FIELDS_SCHEMA,
#         'packagingFields': PACKAGING_MATERIAL_FIELDS_SCHEMA
#     })


# # =============================================================================
# # FACTORY CODE VIEWSET
# # =============================================================================

# class FactoryCodeViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for FactoryCode CRUD operations.
    
#     list:      GET    /api/factory-codes/
#     create:    POST   /api/factory-codes/
#     retrieve:  GET    /api/factory-codes/{id}/
#     update:    PUT    /api/factory-codes/{id}/
#     partial:   PATCH  /api/factory-codes/{id}/
#     destroy:   DELETE /api/factory-codes/{id}/
#     complete:  GET    /api/factory-codes/{id}/complete/
#     wizard:    POST   /api/factory-codes/wizard/
#     """
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
    
#     def get_queryset(self):
#         return FactoryCode.objects.filter(
#             tenant=self.request.user.tenant
#         ).order_by('-created_at')
    
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return FactoryCodeCreateSerializer
#         elif self.action == 'complete':
#             return FactoryCodeCompleteSerializer
#         return FactoryCodeSerializer
    
#     @action(detail=True, methods=['get'])
#     def complete(self, request, pk=None):
#         """GET /api/factory-codes/{id}/complete/ - Complete factory code with all nested data."""
#         factory_code = self.get_object()
#         serializer = FactoryCodeCompleteSerializer(factory_code)
#         return Response(serializer.data)
    
#     @action(detail=False, methods=['post'])
#     def wizard(self, request):
#         """POST /api/factory-codes/wizard/ - Create complete factory code from wizard data."""
#         serializer = FactoryCodeWizardCreateSerializer(
#             data=request.data,
#             context={'request': request}
#         )
#         if serializer.is_valid():
#             factory_code = serializer.save()
#             return Response(
#                 FactoryCodeCompleteSerializer(factory_code).data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # =============================================================================
# # PRODUCT VIEWSET (Step 1)
# # =============================================================================

# class ProductViewSet(viewsets.ModelViewSet):
#     """ViewSet for Product CRUD operations. Nested under FactoryCode."""
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         if factory_code_id:
#             return Product.objects.filter(
#                 factory_code_id=factory_code_id,
#                 factory_code__tenant=self.request.user.tenant
#             )
#         return Product.objects.filter(factory_code__tenant=self.request.user.tenant)
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return ProductCreateSerializer
#         return ProductSerializer
    
#     def perform_create(self, serializer):
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         factory_code = get_object_or_404(
#             FactoryCode, id=factory_code_id, tenant=self.request.user.tenant
#         )
#         serializer.save(factory_code=factory_code)


# # =============================================================================
# # COMPONENT VIEWSET (Step 1)
# # =============================================================================

# class ComponentViewSet(viewsets.ModelViewSet):
#     """ViewSet for Component CRUD operations. Nested under Product."""
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         product_id = self.kwargs.get('product_pk')
#         if product_id:
#             return Component.objects.filter(
#                 product_id=product_id,
#                 product__factory_code__tenant=self.request.user.tenant
#             )
#         return Component.objects.filter(product__factory_code__tenant=self.request.user.tenant)
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return ComponentCreateSerializer
#         return ComponentSerializer
    
#     def perform_create(self, serializer):
#         product_id = self.kwargs.get('product_pk')
#         product = get_object_or_404(
#             Product, id=product_id, factory_code__tenant=self.request.user.tenant
#         )
#         serializer.save(product=product)


# # =============================================================================
# # RAW MATERIAL VIEWSET (Step 2)
# # =============================================================================

# class RawMaterialViewSet(viewsets.ModelViewSet):
#     """ViewSet for RawMaterial CRUD operations."""
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
    
#     def get_queryset(self):
#         component_id = self.kwargs.get('component_pk')
#         if component_id:
#             return RawMaterial.objects.filter(
#                 component_id=component_id,
#                 component__product__factory_code__tenant=self.request.user.tenant
#             )
#         return RawMaterial.objects.filter(
#             component__product__factory_code__tenant=self.request.user.tenant
#         )
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return RawMaterialCreateSerializer
#         return RawMaterialSerializer
    
#     def perform_create(self, serializer):
#         component_id = self.kwargs.get('component_pk')
#         if component_id:
#             component = get_object_or_404(
#                 Component, id=component_id,
#                 product__factory_code__tenant=self.request.user.tenant
#             )
#             serializer.save(component=component)
#         else:
#             serializer.save()


# # =============================================================================
# # CONSUMPTION MATERIAL VIEWSET (Step 3) - 30 Trim Categories
# # =============================================================================

# class ConsumptionMaterialViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for ConsumptionMaterial (Trims & Accessories) CRUD operations.
#     Handles all 30 trim categories with conditional fields.
#     """
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
    
#     def get_queryset(self):
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         queryset = ConsumptionMaterial.objects.filter(
#             factory_code__tenant=self.request.user.tenant
#         )
#         if factory_code_id:
#             queryset = queryset.filter(factory_code_id=factory_code_id)
#         category = self.request.query_params.get('category')
#         if category:
#             queryset = queryset.filter(category=category)
#         return queryset.order_by('-created_at')
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return ConsumptionMaterialCreateSerializer
#         return ConsumptionMaterialSerializer
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         if factory_code_id:
#             context['factory_code_id'] = factory_code_id
#         return context
    
#     def perform_create(self, serializer):
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         if factory_code_id:
#             factory_code = get_object_or_404(
#                 FactoryCode, id=factory_code_id, tenant=self.request.user.tenant
#             )
#             serializer.context['factory_code_id'] = factory_code.id
#         serializer.save()
    
#     @action(detail=False, methods=['post'])
#     def bulk_create(self, request, factory_code_pk=None):
#         """POST /api/factory-codes/{id}/consumption-materials/bulk_create/"""
#         if not factory_code_pk:
#             return Response({'error': 'factory_code_pk required'}, status=400)
        
#         factory_code = get_object_or_404(
#             FactoryCode, id=factory_code_pk, tenant=request.user.tenant
#         )
        
#         items = request.data.get('items', [])
#         created, errors = [], []
        
#         for idx, item_data in enumerate(items):
#             serializer = ConsumptionMaterialCreateSerializer(
#                 data=item_data,
#                 context={'factory_code_id': factory_code.id, 'request': request}
#             )
#             if serializer.is_valid():
#                 instance = serializer.save()
#                 created.append(ConsumptionMaterialSerializer(instance).data)
#             else:
#                 errors.append({'index': idx, 'errors': serializer.errors})
        
#         return Response({
#             'created': created, 'errors': errors,
#             'created_count': len(created), 'error_count': len(errors)
#         }, status=201 if created else 400)


# # =============================================================================
# # ARTWORK MATERIAL VIEWSET (Step 4) - 18 Categories
# # =============================================================================

# class ArtworkMaterialViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for ArtworkMaterial CRUD operations.
#     Handles all 18 artwork categories with conditional fields.
#     """
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
    
#     def get_queryset(self):
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         queryset = ArtworkMaterial.objects.filter(
#             factory_code__tenant=self.request.user.tenant
#         )
#         if factory_code_id:
#             queryset = queryset.filter(factory_code_id=factory_code_id)
#         category = self.request.query_params.get('category')
#         if category:
#             queryset = queryset.filter(category=category)
#         return queryset.order_by('-created_at')
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return ArtworkMaterialCreateSerializer
#         return ArtworkMaterialSerializer
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         if factory_code_id:
#             context['factory_code_id'] = factory_code_id
#         return context
    
#     def perform_create(self, serializer):
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         if factory_code_id:
#             factory_code = get_object_or_404(
#                 FactoryCode, id=factory_code_id, tenant=self.request.user.tenant
#             )
#             serializer.context['factory_code_id'] = factory_code.id
#         serializer.save()
    
#     @action(detail=False, methods=['post'])
#     def bulk_create(self, request, factory_code_pk=None):
#         """POST /api/factory-codes/{id}/artwork-materials/bulk_create/"""
#         if not factory_code_pk:
#             return Response({'error': 'factory_code_pk required'}, status=400)
        
#         factory_code = get_object_or_404(
#             FactoryCode, id=factory_code_pk, tenant=request.user.tenant
#         )
        
#         items = request.data.get('items', [])
#         created, errors = [], []
        
#         for idx, item_data in enumerate(items):
#             serializer = ArtworkMaterialCreateSerializer(
#                 data=item_data,
#                 context={'factory_code_id': factory_code.id, 'request': request}
#             )
#             if serializer.is_valid():
#                 instance = serializer.save()
#                 created.append(ArtworkMaterialSerializer(instance).data)
#             else:
#                 errors.append({'index': idx, 'errors': serializer.errors})
        
#         return Response({
#             'created': created, 'errors': errors,
#             'created_count': len(created), 'error_count': len(errors)
#         }, status=201 if created else 400)


# # =============================================================================
# # PACKAGING VIEWSET (Step 5)
# # =============================================================================

# class PackagingViewSet(viewsets.ModelViewSet):
#     """ViewSet for Packaging CRUD operations."""
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
    
#     def get_queryset(self):
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         queryset = Packaging.objects.filter(
#             factory_code__tenant=self.request.user.tenant
#         )
#         if factory_code_id:
#             queryset = queryset.filter(factory_code_id=factory_code_id)
#         return queryset
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return PackagingCreateSerializer
#         return PackagingSerializer
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         if factory_code_id:
#             context['factory_code_id'] = factory_code_id
#         return context
    
#     def perform_create(self, serializer):
#         factory_code_id = self.kwargs.get('factory_code_pk')
#         if factory_code_id:
#             factory_code = get_object_or_404(
#                 FactoryCode, id=factory_code_id, tenant=self.request.user.tenant
#             )
#             serializer.context['factory_code_id'] = factory_code.id
#         serializer.save()


# # =============================================================================
# # PACKAGING MATERIAL VIEWSET (Step 5 - nested)
# # =============================================================================

# class PackagingMaterialViewSet(viewsets.ModelViewSet):
#     """ViewSet for PackagingMaterial CRUD operations. Nested under Packaging."""
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
    
#     def get_queryset(self):
#         packaging_id = self.kwargs.get('packaging_pk')
#         queryset = PackagingMaterial.objects.filter(
#             packaging__factory_code__tenant=self.request.user.tenant
#         )
#         if packaging_id:
#             queryset = queryset.filter(packaging_id=packaging_id)
#         material_type = self.request.query_params.get('material_type')
#         if material_type:
#             queryset = queryset.filter(material_type=material_type)
#         return queryset.order_by('-created_at')
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return PackagingMaterialCreateSerializer
#         return PackagingMaterialSerializer
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         packaging_id = self.kwargs.get('packaging_pk')
#         if packaging_id:
#             context['packaging_id'] = packaging_id
#         return context
    
#     def perform_create(self, serializer):
#         packaging_id = self.kwargs.get('packaging_pk')
#         if packaging_id:
#             packaging = get_object_or_404(
#                 Packaging, id=packaging_id,
#                 factory_code__tenant=self.request.user.tenant
#             )
#             serializer.context['packaging_id'] = packaging.id
#         serializer.save()

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Department, Segment, BuyerCode, VendorCode
from .models import InternalPurchaseOrder, PurchaseOrder, CompanyEssential
from .serializers import (
    DepartmentSerializer, DepartmentListSerializer, DepartmentCreateSerializer,
    SegmentSerializer, SegmentDetailSerializer,
    BuyerCodeSerializer, BuyerCodeCreateSerializer, BuyerCodeListSerializer,
    VendorCodeSerializer, VendorCodeCreateSerializer, VendorCodeListSerializer,
    InternalPurchaseOrderSerializer, InternalPurchaseOrderCreateSerializer,
    PurchaseOrderSerializer, PurchaseOrderCreateSerializer,
    CompanyEssentialSerializer, CompanyEssentialCreateSerializer,
    CompanyEssentialBulkCreateSerializer
)


class DepartmentViewSet(ModelViewSet):
    """
    ViewSet for Department CRUD operations
    """
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return DepartmentListSerializer
        elif self.action == 'create':
            return DepartmentCreateSerializer
        return DepartmentSerializer
    
    def get_queryset(self):
        """Filter departments based on tenant if user is not master admin"""
        queryset = Department.objects.all()
        
        # Filter by tenant if user is not master admin
        user = self.request.user
        if not user.is_master_admin and user.tenant:
            queryset = queryset.filter(
                Q(tenant=user.tenant) | Q(tenant__isnull=True)
            )
        
        # Filter by active status if requested
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.select_related('tenant', 'created_by').prefetch_related('segments')
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def segments(self, request, pk=None):
        """Get all segments for a department"""
        department = self.get_object()
        segments = department.segments.all()
        serializer = SegmentDetailSerializer(segments, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def add_segment(self, request, pk=None):
        """Add a segment to a department"""
        department = self.get_object()
        serializer = SegmentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(department=department, created_by=request.user)
            return Response({
                'status': 'success',
                'message': 'Segment added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Failed to add segment',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SegmentViewSet(ModelViewSet):
    """
    ViewSet for Segment CRUD operations
    """
    permission_classes = [IsAuthenticated]
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return SegmentDetailSerializer
        return SegmentSerializer
    
    def get_queryset(self):
        """Filter segments based on department and tenant"""
        queryset = Segment.objects.all()
        
        # Filter by department if provided
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        
        # Filter by active status if requested
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by tenant if user is not master admin
        user = self.request.user
        if not user.is_master_admin and user.tenant:
            queryset = queryset.filter(
                Q(department__tenant=user.tenant) | Q(department__tenant__isnull=True)
            )
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.select_related('department', 'department__tenant', 'created_by')
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create a segment"""
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                'status': 'success',
                'message': 'Segment created successfully',
                'data': SegmentDetailSerializer(serializer.instance).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Failed to create segment',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update a segment"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'status': 'success',
                'message': 'Segment updated successfully',
                'data': SegmentDetailSerializer(serializer.instance).data
            })
        
        return Response({
            'status': 'error',
            'message': 'Failed to update segment',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Delete a segment"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Segment deleted successfully'
        }, status=status.HTTP_200_OK)


# Additional API views for convenience
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def department_menu_structure(request):
    """
    Get complete department menu structure with segments
    Useful for frontend menu rendering
    """
    departments = Department.objects.filter(is_active=True).prefetch_related(
        'segments'
    ).order_by('display_order', 'name')
    
    menu_data = []
    for dept in departments:
        segments = dept.segments.filter(is_active=True).order_by('display_order', 'name')
        menu_data.append({
            'id': str(dept.id),
            'code': dept.code,
            'label': dept.name,
            'hasSubMenu': segments.exists(),
            'segments': [
                {
                    'id': str(seg.id),
                    'code': seg.code,
                    'label': seg.name
                }
                for seg in segments
            ]
        })
    
    return Response({
        'status': 'success',
        'data': menu_data
    })


class BuyerCodeViewSet(ModelViewSet):
    """
    ViewSet for BuyerCode CRUD operations
    Handles buyer code generation with auto-incrementing codes (101A, 102A, etc.)
    """
    permission_classes = [IsAuthenticated]
    queryset = BuyerCode.objects.all()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return BuyerCodeListSerializer
        elif self.action == 'create':
            return BuyerCodeCreateSerializer
        return BuyerCodeSerializer
    
    def get_queryset(self):
        """Filter buyer codes based on tenant if user is not master admin"""
        queryset = BuyerCode.objects.all()
        
        # Filter by tenant if user is not master admin
        user = self.request.user
        if not user.is_master_admin and user.tenant:
            queryset = queryset.filter(tenant=user.tenant)
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(buyer_name__icontains=search) |
                Q(code__icontains=search) |
                Q(retailer__icontains=search) |
                Q(contact_person__icontains=search)
            )
        
        return queryset.select_related('tenant', 'created_by')
    
    def create(self, request, *args, **kwargs):
        """Create a new buyer code with auto-generated code"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create buyer code (code will be auto-generated)
        buyer_code = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Buyer code generated successfully',
            'data': BuyerCodeSerializer(buyer_code).data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Update a buyer code (code cannot be changed)"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Remove code from request data if present (code is read-only)
        request_data = request.data.copy()
        if 'code' in request_data:
            request_data.pop('code')
        
        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Buyer code updated successfully',
            'data': BuyerCodeSerializer(serializer.instance).data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Delete a buyer code"""
        instance = self.get_object()
        code = instance.code
        self.perform_destroy(instance)
        
        return Response({
            'status': 'success',
            'message': f'Buyer code {code} deleted successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def generate(self, request):
        """
        Preview the next buyer code that would be generated
        Useful for frontend to show what code will be generated
        """
        user = request.user
        tenant = user.tenant if user and not user.is_master_admin else None
        
        next_code = BuyerCode.generate_next_code(tenant=tenant)
        
        return Response({
            'status': 'success',
            'data': {
                'next_code': next_code
            }
        })
    
    @action(detail=False, methods=['get'], url_path='master-sheet')
    def master_sheet(self, request):
        """
        Get all buyer codes in master sheet format
        Returns all buyer codes formatted for frontend master sheet display
        """
        queryset = self.get_queryset()
        
        # Format data for frontend
        buyer_codes = []
        for buyer in queryset:
            buyer_codes.append({
                'code': buyer.code,
                'buyerName': buyer.buyer_name,
                'buyerAddress': buyer.buyer_address,
                'contactPerson': buyer.contact_person,
                'retailer': buyer.retailer,
                'createdAt': buyer.created_at.isoformat() if buyer.created_at else None
            })
        
        return Response({
            'status': 'success',
            'data': buyer_codes,
            'count': len(buyer_codes)
        })


class VendorCodeViewSet(ModelViewSet):
    """
    ViewSet for VendorCode CRUD operations
    Handles vendor code generation with auto-incrementing numeric codes (101, 102, etc.)
    """
    permission_classes = [IsAuthenticated]
    queryset = VendorCode.objects.all()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return VendorCodeListSerializer
        elif self.action == 'create':
            return VendorCodeCreateSerializer
        return VendorCodeSerializer
    
    def get_queryset(self):
        """Filter vendor codes based on tenant if user is not master admin"""
        queryset = VendorCode.objects.all()
        
        # Filter by tenant if user is not master admin
        user = self.request.user
        if not user.is_master_admin and user.tenant:
            queryset = queryset.filter(tenant=user.tenant)
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(vendor_name__icontains=search) |
                Q(code__icontains=search) |
                Q(gst__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(email__icontains=search) |
                Q(job_work_category__icontains=search)
            )
        
        return queryset.select_related('tenant', 'created_by')
    
    def create(self, request, *args, **kwargs):
        """Create a new vendor code with auto-generated code"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create vendor code (code will be auto-generated)
        vendor_code = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Vendor code generated successfully',
            'data': VendorCodeSerializer(vendor_code).data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Update a vendor code (code cannot be changed)"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Remove code from request data if present (code is read-only)
        request_data = request.data.copy()
        if 'code' in request_data:
            request_data.pop('code')
        
        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Vendor code updated successfully',
            'data': VendorCodeSerializer(serializer.instance).data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Delete a vendor code"""
        instance = self.get_object()
        code = instance.code
        self.perform_destroy(instance)
        
        return Response({
            'status': 'success',
            'message': f'Vendor code {code} deleted successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def generate(self, request):
        """
        Preview the next vendor code that would be generated
        Useful for frontend to show what code will be generated
        """
        user = request.user
        tenant = user.tenant if user and not user.is_master_admin else None
        
        next_code = VendorCode.generate_next_code(tenant=tenant)
        
        return Response({
            'status': 'success',
            'data': {
                'next_code': next_code
            }
        })
    
    @action(detail=False, methods=['get'], url_path='master-sheet')
    def master_sheet(self, request):
        """
        Get all vendor codes in master sheet format
        Returns all vendor codes formatted for frontend master sheet display
        """
        queryset = self.get_queryset()
        
        # Format data for frontend
        vendor_codes = []
        for vendor in queryset:
            vendor_codes.append({
                'code': vendor.code,
                'vendorName': vendor.vendor_name,
                'address': vendor.address,
                'gst': vendor.gst,
                'bankName': vendor.bank_name,
                'accNo': vendor.account_number,
                'ifscCode': vendor.ifsc_code,
                'jobWorkCategory': vendor.job_work_category,
                'jobWorkSubCategory': vendor.job_work_sub_category,
                'contactPerson': vendor.contact_person,
                'whatsappNo': vendor.whatsapp_number,
                'altWhatsappNo': vendor.alt_whatsapp_number or '',
                'email': vendor.email,
                'paymentTerms': vendor.payment_terms,
                'createdAt': vendor.created_at.isoformat() if vendor.created_at else None
            })
        
        return Response({
            'status': 'success',
            'data': vendor_codes,
            'count': len(vendor_codes)
        })

"""
Factory Code Views - V2
========================

DRF ViewSets and API Views for the Factory Code module.
Includes endpoints for:
- CRUD operations on all models
- Choice list endpoints for frontend dropdowns
- Category field schema endpoints for dynamic form rendering
- Step-by-step wizard endpoints
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404

from .models import (
    FactoryCode, Product, Component, RawMaterial, WorkOrder,
    ConsumptionMaterial, ArtworkMaterial, Packaging, PackagingMaterial,
    TrimAccessoryChoices, ArtworkCategoryChoices, PackagingMaterialTypeChoices,
    WorkOrderTypeChoices, UnitChoices, SizeUnitChoices,
    ApprovalChoices, ApprovalAgainstChoices,
    TRIM_CATEGORY_FIELDS_SCHEMA, ARTWORK_CATEGORY_FIELDS_SCHEMA,
    PACKAGING_MATERIAL_FIELDS_SCHEMA
)

from .serializers import (
    FactoryCodeSerializer, FactoryCodeCreateSerializer,
    FactoryCodeCompleteSerializer, FactoryCodeWizardCreateSerializer,
    ProductSerializer, ProductCreateSerializer,
    ComponentSerializer, ComponentCreateSerializer,
    RawMaterialSerializer, RawMaterialCreateSerializer,
    ConsumptionMaterialSerializer, ConsumptionMaterialCreateSerializer,
    ArtworkMaterialSerializer, ArtworkMaterialCreateSerializer,
    PackagingSerializer, PackagingCreateSerializer,
    PackagingMaterialSerializer, PackagingMaterialCreateSerializer
)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def choices_to_list(choices_class):
    """Convert Django TextChoices to list of {value, label} dicts"""
    return [{'value': choice.value, 'label': choice.label} for choice in choices_class]


# =============================================================================
# CHOICE LIST API VIEWS
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trim_category_choices(request):
    """
    GET /api/factory-code/choices/trim-categories/
    Returns list of all 30 trim/accessory categories.
    """
    return Response({
        'choices': choices_to_list(TrimAccessoryChoices),
        'count': len(TrimAccessoryChoices)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def artwork_category_choices(request):
    """
    GET /api/factory-code/choices/artwork-categories/
    Returns list of all 18 artwork categories.
    """
    return Response({
        'choices': choices_to_list(ArtworkCategoryChoices),
        'count': len(ArtworkCategoryChoices)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def packaging_material_type_choices(request):
    """
    GET /api/factory-code/choices/packaging-material-types/
    Returns list of all 8 packaging material types.
    """
    return Response({
        'choices': choices_to_list(PackagingMaterialTypeChoices),
        'count': len(PackagingMaterialTypeChoices)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def work_order_type_choices(request):
    """
    GET /api/factory-code/choices/work-order-types/
    Returns list of work order process types.
    """
    return Response({
        'choices': choices_to_list(WorkOrderTypeChoices),
        'count': len(WorkOrderTypeChoices)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unit_choices(request):
    """GET /api/factory-code/choices/units/"""
    return Response({
        'choices': choices_to_list(UnitChoices),
        'count': len(UnitChoices)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def size_unit_choices(request):
    """GET /api/factory-code/choices/size-units/"""
    return Response({
        'choices': choices_to_list(SizeUnitChoices),
        'count': len(SizeUnitChoices)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def approval_choices(request):
    """GET /api/factory-code/choices/approvals/"""
    return Response({
        'choices': choices_to_list(ApprovalChoices),
        'count': len(ApprovalChoices)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def approval_against_choices(request):
    """GET /api/factory-code/choices/approval-against/"""
    return Response({
        'choices': choices_to_list(ApprovalAgainstChoices),
        'count': len(ApprovalAgainstChoices)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_choices(request):
    """
    GET /api/factory-code/choices/
    Returns all choice lists for frontend initialization.
    """
    return Response({
        'trimCategories': choices_to_list(TrimAccessoryChoices),
        'artworkCategories': choices_to_list(ArtworkCategoryChoices),
        'packagingMaterialTypes': choices_to_list(PackagingMaterialTypeChoices),
        'workOrderTypes': choices_to_list(WorkOrderTypeChoices),
        'units': choices_to_list(UnitChoices),
        'sizeUnits': choices_to_list(SizeUnitChoices),
        'approvals': choices_to_list(ApprovalChoices),
        'approvalAgainst': choices_to_list(ApprovalAgainstChoices)
    })


# =============================================================================
# CATEGORY FIELD SCHEMA API VIEWS
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trim_category_fields(request, category=None):
    """
    GET /api/factory-code/schemas/trim-fields/
    GET /api/factory-code/schemas/trim-fields/{category}/
    """
    if category:
        import urllib.parse
        category = urllib.parse.unquote(category)
        if category in TRIM_CATEGORY_FIELDS_SCHEMA:
            return Response({
                'category': category,
                'schema': TRIM_CATEGORY_FIELDS_SCHEMA[category]
            })
        return Response({'error': f'Unknown trim category: {category}'}, status=404)
    return Response({
        'schemas': TRIM_CATEGORY_FIELDS_SCHEMA,
        'count': len(TRIM_CATEGORY_FIELDS_SCHEMA)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def artwork_category_fields(request, category=None):
    """
    GET /api/factory-code/schemas/artwork-fields/
    GET /api/factory-code/schemas/artwork-fields/{category}/
    """
    if category:
        import urllib.parse
        category = urllib.parse.unquote(category)
        if category in ARTWORK_CATEGORY_FIELDS_SCHEMA:
            return Response({
                'category': category,
                'schema': ARTWORK_CATEGORY_FIELDS_SCHEMA[category]
            })
        return Response({'error': f'Unknown artwork category: {category}'}, status=404)
    return Response({
        'schemas': ARTWORK_CATEGORY_FIELDS_SCHEMA,
        'count': len(ARTWORK_CATEGORY_FIELDS_SCHEMA)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def packaging_material_fields(request, material_type=None):
    """
    GET /api/factory-code/schemas/packaging-fields/
    GET /api/factory-code/schemas/packaging-fields/{material_type}/
    """
    if material_type:
        import urllib.parse
        material_type = urllib.parse.unquote(material_type)
        if material_type in PACKAGING_MATERIAL_FIELDS_SCHEMA:
            return Response({
                'materialType': material_type,
                'schema': PACKAGING_MATERIAL_FIELDS_SCHEMA[material_type]
            })
        return Response({'error': f'Unknown packaging material type: {material_type}'}, status=404)
    return Response({
        'schemas': PACKAGING_MATERIAL_FIELDS_SCHEMA,
        'count': len(PACKAGING_MATERIAL_FIELDS_SCHEMA)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_field_schemas(request):
    """GET /api/factory-code/schemas/ - Returns all field schemas."""
    return Response({
        'trimFields': TRIM_CATEGORY_FIELDS_SCHEMA,
        'artworkFields': ARTWORK_CATEGORY_FIELDS_SCHEMA,
        'packagingFields': PACKAGING_MATERIAL_FIELDS_SCHEMA
    })


# =============================================================================
# FACTORY CODE VIEWSET
# =============================================================================

class FactoryCodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for FactoryCode CRUD operations.
    
    list:      GET    /api/factory-codes/
    create:    POST   /api/factory-codes/
    retrieve:  GET    /api/factory-codes/{id}/
    update:    PUT    /api/factory-codes/{id}/
    partial:   PATCH  /api/factory-codes/{id}/
    destroy:   DELETE /api/factory-codes/{id}/
    complete:  GET    /api/factory-codes/{id}/complete/
    wizard:    POST   /api/factory-codes/wizard/
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        return FactoryCode.objects.filter(
            tenant=self.request.user.tenant
        ).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FactoryCodeCreateSerializer
        elif self.action == 'complete':
            return FactoryCodeCompleteSerializer
        return FactoryCodeSerializer
    
    @action(detail=True, methods=['get'])
    def complete(self, request, pk=None):
        """GET /api/factory-codes/{id}/complete/ - Complete factory code with all nested data."""
        factory_code = self.get_object()
        serializer = FactoryCodeCompleteSerializer(factory_code)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def wizard(self, request):
        """POST /api/factory-codes/wizard/ - Create complete factory code from wizard data."""
        serializer = FactoryCodeWizardCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            factory_code = serializer.save()
            return Response(
                FactoryCodeCompleteSerializer(factory_code).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================================================================
# PRODUCT VIEWSET (Step 1)
# =============================================================================

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product CRUD operations. Nested under FactoryCode."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        factory_code_id = self.kwargs.get('factory_code_pk')
        if factory_code_id:
            return Product.objects.filter(
                factory_code_id=factory_code_id,
                factory_code__tenant=self.request.user.tenant
            )
        return Product.objects.filter(factory_code__tenant=self.request.user.tenant)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def perform_create(self, serializer):
        factory_code_id = self.kwargs.get('factory_code_pk')
        factory_code = get_object_or_404(
            FactoryCode, id=factory_code_id, tenant=self.request.user.tenant
        )
        serializer.save(factory_code=factory_code)


# =============================================================================
# COMPONENT VIEWSET (Step 1)
# =============================================================================

class ComponentViewSet(viewsets.ModelViewSet):
    """ViewSet for Component CRUD operations. Nested under Product."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        if product_id:
            return Component.objects.filter(
                product_id=product_id,
                product__factory_code__tenant=self.request.user.tenant
            )
        return Component.objects.filter(product__factory_code__tenant=self.request.user.tenant)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ComponentCreateSerializer
        return ComponentSerializer
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = get_object_or_404(
            Product, id=product_id, factory_code__tenant=self.request.user.tenant
        )
        serializer.save(product=product)


# =============================================================================
# RAW MATERIAL VIEWSET (Step 2)
# =============================================================================

class RawMaterialViewSet(viewsets.ModelViewSet):
    """ViewSet for RawMaterial CRUD operations."""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        component_id = self.kwargs.get('component_pk')
        if component_id:
            return RawMaterial.objects.filter(
                component_id=component_id,
                component__product__factory_code__tenant=self.request.user.tenant
            )
        return RawMaterial.objects.filter(
            component__product__factory_code__tenant=self.request.user.tenant
        )
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RawMaterialCreateSerializer
        return RawMaterialSerializer
    
    def perform_create(self, serializer):
        component_id = self.kwargs.get('component_pk')
        if component_id:
            component = get_object_or_404(
                Component, id=component_id,
                product__factory_code__tenant=self.request.user.tenant
            )
            serializer.save(component=component)
        else:
            serializer.save()


# =============================================================================
# CONSUMPTION MATERIAL VIEWSET (Step 3) - 30 Trim Categories
# =============================================================================

class ConsumptionMaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ConsumptionMaterial (Trims & Accessories) CRUD operations.
    Handles all 30 trim categories with conditional fields.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        factory_code_id = self.kwargs.get('factory_code_pk')
        queryset = ConsumptionMaterial.objects.filter(
            factory_code__tenant=self.request.user.tenant
        )
        if factory_code_id:
            queryset = queryset.filter(factory_code_id=factory_code_id)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConsumptionMaterialCreateSerializer
        return ConsumptionMaterialSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        factory_code_id = self.kwargs.get('factory_code_pk')
        if factory_code_id:
            context['factory_code_id'] = factory_code_id
        return context
    
    def perform_create(self, serializer):
        factory_code_id = self.kwargs.get('factory_code_pk')
        if factory_code_id:
            factory_code = get_object_or_404(
                FactoryCode, id=factory_code_id, tenant=self.request.user.tenant
            )
            serializer.context['factory_code_id'] = factory_code.id
        serializer.save()
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request, factory_code_pk=None):
        """POST /api/factory-codes/{id}/consumption-materials/bulk_create/"""
        if not factory_code_pk:
            return Response({'error': 'factory_code_pk required'}, status=400)
        
        factory_code = get_object_or_404(
            FactoryCode, id=factory_code_pk, tenant=request.user.tenant
        )
        
        items = request.data.get('items', [])
        created, errors = [], []
        
        for idx, item_data in enumerate(items):
            serializer = ConsumptionMaterialCreateSerializer(
                data=item_data,
                context={'factory_code_id': factory_code.id, 'request': request}
            )
            if serializer.is_valid():
                instance = serializer.save()
                created.append(ConsumptionMaterialSerializer(instance).data)
            else:
                errors.append({'index': idx, 'errors': serializer.errors})
        
        return Response({
            'created': created, 'errors': errors,
            'created_count': len(created), 'error_count': len(errors)
        }, status=201 if created else 400)


# =============================================================================
# ARTWORK MATERIAL VIEWSET (Step 4) - 18 Categories
# =============================================================================

class ArtworkMaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ArtworkMaterial CRUD operations.
    Handles all 18 artwork categories with conditional fields.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        factory_code_id = self.kwargs.get('factory_code_pk')
        queryset = ArtworkMaterial.objects.filter(
            factory_code__tenant=self.request.user.tenant
        )
        if factory_code_id:
            queryset = queryset.filter(factory_code_id=factory_code_id)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ArtworkMaterialCreateSerializer
        return ArtworkMaterialSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        factory_code_id = self.kwargs.get('factory_code_pk')
        if factory_code_id:
            context['factory_code_id'] = factory_code_id
        return context
    
    def perform_create(self, serializer):
        factory_code_id = self.kwargs.get('factory_code_pk')
        if factory_code_id:
            factory_code = get_object_or_404(
                FactoryCode, id=factory_code_id, tenant=self.request.user.tenant
            )
            serializer.context['factory_code_id'] = factory_code.id
        serializer.save()
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request, factory_code_pk=None):
        """POST /api/factory-codes/{id}/artwork-materials/bulk_create/"""
        if not factory_code_pk:
            return Response({'error': 'factory_code_pk required'}, status=400)
        
        factory_code = get_object_or_404(
            FactoryCode, id=factory_code_pk, tenant=request.user.tenant
        )
        
        items = request.data.get('items', [])
        created, errors = [], []
        
        for idx, item_data in enumerate(items):
            serializer = ArtworkMaterialCreateSerializer(
                data=item_data,
                context={'factory_code_id': factory_code.id, 'request': request}
            )
            if serializer.is_valid():
                instance = serializer.save()
                created.append(ArtworkMaterialSerializer(instance).data)
            else:
                errors.append({'index': idx, 'errors': serializer.errors})
        
        return Response({
            'created': created, 'errors': errors,
            'created_count': len(created), 'error_count': len(errors)
        }, status=201 if created else 400)


# =============================================================================
# PACKAGING VIEWSET (Step 5)
# =============================================================================

class PackagingViewSet(viewsets.ModelViewSet):
    """ViewSet for Packaging CRUD operations."""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        factory_code_id = self.kwargs.get('factory_code_pk')
        queryset = Packaging.objects.filter(
            factory_code__tenant=self.request.user.tenant
        )
        if factory_code_id:
            queryset = queryset.filter(factory_code_id=factory_code_id)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PackagingCreateSerializer
        return PackagingSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        factory_code_id = self.kwargs.get('factory_code_pk')
        if factory_code_id:
            context['factory_code_id'] = factory_code_id
        return context
    
    def perform_create(self, serializer):
        factory_code_id = self.kwargs.get('factory_code_pk')
        if factory_code_id:
            factory_code = get_object_or_404(
                FactoryCode, id=factory_code_id, tenant=self.request.user.tenant
            )
            serializer.context['factory_code_id'] = factory_code.id
        serializer.save()


# =============================================================================
# PACKAGING MATERIAL VIEWSET (Step 5 - nested)
# =============================================================================

class PackagingMaterialViewSet(viewsets.ModelViewSet):
    """ViewSet for PackagingMaterial CRUD operations. Nested under Packaging."""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        packaging_id = self.kwargs.get('packaging_pk')
        queryset = PackagingMaterial.objects.filter(
            packaging__factory_code__tenant=self.request.user.tenant
        )
        if packaging_id:
            queryset = queryset.filter(packaging_id=packaging_id)
        material_type = self.request.query_params.get('material_type')
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PackagingMaterialCreateSerializer
        return PackagingMaterialSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        packaging_id = self.kwargs.get('packaging_pk')
        if packaging_id:
            context['packaging_id'] = packaging_id
        return context
    
    def perform_create(self, serializer):
        packaging_id = self.kwargs.get('packaging_pk')
        if packaging_id:
            packaging = get_object_or_404(
                Packaging, id=packaging_id,
                factory_code__tenant=self.request.user.tenant
            )
            serializer.context['packaging_id'] = packaging.id
        serializer.save()


# =============================================================================
# INTERNAL PURCHASE ORDER VIEWSET
# =============================================================================

class InternalPurchaseOrderViewSet(ModelViewSet):
    """
    ViewSet for Internal Purchase Order CRUD operations
    Auto-generates IPO codes like: CHD/PD/101A/PROGRAM1/1
    """
    permission_classes = [IsAuthenticated]
    queryset = InternalPurchaseOrder.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return InternalPurchaseOrderCreateSerializer
        return InternalPurchaseOrderSerializer

    def get_queryset(self):
        queryset = InternalPurchaseOrder.objects.all()
        user = self.request.user
        if not user.is_master_admin and user.tenant:
            queryset = queryset.filter(tenant=user.tenant)
        
        # Filter by program
        program = self.request.query_params.get('program_name')
        if program:
            queryset = queryset.filter(program_name__iexact=program)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(ipo_code__icontains=search) |
                Q(program_name__icontains=search) |
                Q(buyer_code_text__icontains=search)
            )
        
        return queryset.select_related('buyer_code', 'tenant', 'created_by')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ipo = serializer.save()
        return Response({
            'status': 'success',
            'message': 'IPO created successfully',
            'data': InternalPurchaseOrderSerializer(ipo).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='next-sr-no')
    def next_sr_no(self, request):
        """Get next SR number for a given program name."""
        program = request.query_params.get('program', '')
        if not program:
            return Response({'error': 'program parameter is required'}, status=400)
        tenant = request.user.tenant if not request.user.is_master_admin else None
        next_no = InternalPurchaseOrder.get_next_sr_no(program, tenant)
        return Response({'next_sr_no': next_no, 'program_name': program})


# =============================================================================
# PURCHASE ORDER VIEWSET
# =============================================================================

class PurchaseOrderViewSet(ModelViewSet):
    """
    ViewSet for Purchase Order CRUD operations
    Auto-generates PO codes like: PO1001, PO1002, etc.
    """
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PurchaseOrderCreateSerializer
        return PurchaseOrderSerializer

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        user = self.request.user
        if not user.is_master_admin and user.tenant:
            queryset = queryset.filter(tenant=user.tenant)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(po_code__icontains=search) |
                Q(po_description__icontains=search) |
                Q(product_category__icontains=search)
            )
        
        return queryset.select_related('buyer', 'vendor', 'tenant', 'created_by')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        po = serializer.save()
        return Response({
            'status': 'success',
            'message': 'Purchase Order created successfully',
            'data': PurchaseOrderSerializer(po).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='next-code')
    def next_code(self, request):
        """Preview the next PO code that would be generated."""
        tenant = request.user.tenant if not request.user.is_master_admin else None
        next_po = PurchaseOrder.generate_next_code(tenant)
        return Response({'next_po_code': next_po})


# =============================================================================
# COMPANY ESSENTIAL VIEWSET
# =============================================================================

class CompanyEssentialViewSet(ModelViewSet):
    """
    ViewSet for Company Essentials CRUD operations
    Unified model for 12 categories (Stationary, Pantry, Machinery, etc.)
    Auto-generates codes like: CHD/E/STATIONARY/26-27/PO-1
    """
    permission_classes = [IsAuthenticated]
    queryset = CompanyEssential.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CompanyEssentialCreateSerializer
        if self.action == 'bulk_create':
            return CompanyEssentialBulkCreateSerializer
        return CompanyEssentialSerializer

    def get_queryset(self):
        queryset = CompanyEssential.objects.all()
        user = self.request.user
        if not user.is_master_admin and user.tenant:
            queryset = queryset.filter(tenant=user.tenant)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category.upper())
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(item_description__icontains=search) |
                Q(item__icontains=search)
            )
        
        return queryset.select_related('tenant', 'created_by')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        essential = serializer.save()
        return Response({
            'status': 'success',
            'message': 'Company essential created successfully',
            'data': CompanyEssentialSerializer(essential).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """Bulk create multiple company essentials."""
        serializer = CompanyEssentialBulkCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        created = serializer.save()
        return Response({
            'status': 'success',
            'message': f'{len(created)} items created successfully',
            'data': CompanyEssentialSerializer(created, many=True).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='next-po-number')
    def next_po_number(self, request):
        """Get next PO number for a given category."""
        category = request.query_params.get('category', '')
        if not category:
            return Response({'error': 'category parameter is required'}, status=400)
        tenant = request.user.tenant if not request.user.is_master_admin else None
        next_no = CompanyEssential.get_next_po_number(category.upper(), tenant)
        return Response({'next_po_number': next_no, 'category': category.upper()})

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """List all available categories."""
        return Response({
            'categories': [
                {'value': c[0], 'label': c[1]}
                for c in CompanyEssential.CATEGORY_CHOICES
            ]
        })