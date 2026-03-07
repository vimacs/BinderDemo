# from rest_framework import serializers
# import re
# from .models import Department, Segment, BuyerCode, VendorCode


# class SegmentSerializer(serializers.ModelSerializer):
#     """Serializer for Segment model"""
    
#     class Meta:
#         model = Segment
#         fields = [
#             'id', 'code', 'name', 'description', 'department', 
#             'display_order', 'is_active', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at']
    
#     def validate_code(self, value):
#         """Validate segment code"""
#         if not value:
#             raise serializers.ValidationError("Segment code is required")
#         return value.lower().strip()


# class SegmentDetailSerializer(serializers.ModelSerializer):
#     """Detailed serializer for Segment with department info"""
    
#     department_name = serializers.CharField(source='department.name', read_only=True)
#     department_code = serializers.CharField(source='department.code', read_only=True)
    
#     class Meta:
#         model = Segment
#         fields = [
#             'id', 'code', 'name', 'description', 'department', 
#             'department_name', 'department_code',
#             'display_order', 'is_active', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at', 'department_name', 'department_code']


# class DepartmentSerializer(serializers.ModelSerializer):
#     """Serializer for Department model"""
    
#     segments = SegmentSerializer(many=True, read_only=True)
#     segments_count = serializers.IntegerField(source='segments.count', read_only=True)
    
#     class Meta:
#         model = Department
#         fields = [
#             'id', 'code', 'name', 'description', 'display_order', 
#             'is_active', 'tenant', 'segments', 'segments_count',
#             'created_at', 'updated_at', 'created_by'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at', 'segments_count']
    
#     def validate_code(self, value):
#         """Validate department code"""
#         if not value:
#             raise serializers.ValidationError("Department code is required")
#         return value.lower().strip()


# class DepartmentListSerializer(serializers.ModelSerializer):
#     """Lightweight serializer for department list"""
    
#     segments_count = serializers.IntegerField(source='segments.count', read_only=True)
#     active_segments_count = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Department
#         fields = [
#             'id', 'code', 'name', 'description', 'display_order', 
#             'is_active', 'segments_count', 'active_segments_count',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at']
    
#     def get_active_segments_count(self, obj):
#         """Get count of active segments"""
#         return obj.segments.filter(is_active=True).count()


# class DepartmentCreateSerializer(serializers.ModelSerializer):
#     """Serializer for creating department with initial segments"""
    
#     segments = SegmentSerializer(many=True, required=False)
    
#     class Meta:
#         model = Department
#         fields = [
#             'id', 'code', 'name', 'description', 'display_order', 
#             'is_active', 'tenant', 'segments', 'created_by'
#         ]
#         read_only_fields = ['id']
    
#     def create(self, validated_data):
#         """Create department and associated segments"""
#         segments_data = validated_data.pop('segments', [])
#         department = Department.objects.create(**validated_data)
        
#         for segment_data in segments_data:
#             Segment.objects.create(department=department, **segment_data)
        
#         return department


# class BuyerCodeSerializer(serializers.ModelSerializer):
#     """Serializer for BuyerCode model"""
    
#     class Meta:
#         model = BuyerCode
#         fields = [
#             'id', 'code', 'buyer_name', 'buyer_address', 'contact_person',
#             'retailer', 'tenant', 'created_at', 'updated_at', 'created_by'
#         ]
#         read_only_fields = ['id', 'code', 'created_at', 'updated_at']
    
#     def validate_buyer_name(self, value):
#         """Validate buyer name"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Buyer name is required")
#         return value.strip()
    
#     def validate_buyer_address(self, value):
#         """Validate buyer address"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Buyer address is required")
#         return value.strip()
    
#     def validate_contact_person(self, value):
#         """Validate contact person"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Contact person is required")
#         return value.strip()
    
#     def validate_retailer(self, value):
#         """Validate retailer"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Retailer is required")
#         return value.strip()


# class BuyerCodeCreateSerializer(serializers.ModelSerializer):
#     """Serializer for creating buyer code (code is auto-generated)"""
    
#     class Meta:
#         model = BuyerCode
#         fields = [
#             'id', 'code', 'buyer_name', 'buyer_address', 'contact_person',
#             'retailer', 'tenant'
#         ]
#         read_only_fields = ['id', 'code']
    
#     def validate_buyer_name(self, value):
#         """Validate buyer name"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Buyer name is required")
#         return value.strip()
    
#     def validate_buyer_address(self, value):
#         """Validate buyer address"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Buyer address is required")
#         return value.strip()
    
#     def validate_contact_person(self, value):
#         """Validate contact person"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Contact person is required")
#         return value.strip()
    
#     def validate_retailer(self, value):
#         """Validate retailer"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Retailer is required")
#         return value.strip()
    
#     def create(self, validated_data):
#         """Create buyer code with auto-generated code"""
#         request = self.context.get('request')
#         user = request.user if request else None
        
#         # Get tenant from user if not provided
#         if 'tenant' not in validated_data and user and user.tenant:
#             validated_data['tenant'] = user.tenant
        
#         # Create buyer code (code will be auto-generated in save method)
#         buyer_code = BuyerCode.objects.create(
#             **validated_data,
#             created_by=user
#         )
        
#         return buyer_code


# class BuyerCodeListSerializer(serializers.ModelSerializer):
#     """Lightweight serializer for buyer code list"""
    
#     class Meta:
#         model = BuyerCode
#         fields = [
#             'id', 'code', 'buyer_name', 'retailer', 'contact_person',
#             'created_at'
#         ]
#         read_only_fields = ['id', 'code', 'created_at']


# class VendorCodeSerializer(serializers.ModelSerializer):
#     """Serializer for VendorCode model"""
    
#     class Meta:
#         model = VendorCode
#         fields = [
#             'id', 'code', 'vendor_name', 'address', 'gst', 'bank_name',
#             'account_number', 'ifsc_code', 'job_work_category', 'job_work_sub_category',
#             'contact_person', 'whatsapp_number', 'alt_whatsapp_number', 'email',
#             'payment_terms', 'tenant', 'created_at', 'updated_at', 'created_by'
#         ]
#         read_only_fields = ['id', 'code', 'created_at', 'updated_at']
    
#     def validate_gst(self, value):
#         """Validate GST number format"""
#         if not value:
#             raise serializers.ValidationError("GST number is required")
#         # GST format: 22AAAAA0000A1Z5 (15 characters)
#         gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
#         if not re.match(gst_pattern, value.upper()):
#             raise serializers.ValidationError("Please enter a valid GST number (e.g., 22AAAAA0000A1Z5)")
#         return value.upper()
    
#     def validate_ifsc_code(self, value):
#         """Validate IFSC code format"""
#         if not value:
#             raise serializers.ValidationError("IFSC code is required")
#         # IFSC format: AAAA0XXXXX (11 characters)
#         ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
#         if not re.match(ifsc_pattern, value.upper()):
#             raise serializers.ValidationError("Please enter a valid IFSC code (e.g., SBIN0000123)")
#         return value.upper()
    
#     def validate_whatsapp_number(self, value):
#         """Validate WhatsApp number format"""
#         if not value:
#             raise serializers.ValidationError("WhatsApp number is required")
#         # Remove spaces and check if it's 10 digits
#         cleaned = value.replace(' ', '').replace('-', '')
#         if not cleaned.isdigit() or len(cleaned) != 10:
#             raise serializers.ValidationError("Please enter a valid 10-digit WhatsApp number")
#         return cleaned
    
#     def validate_alt_whatsapp_number(self, value):
#         """Validate alternative WhatsApp number format (optional)"""
#         if value:
#             cleaned = value.replace(' ', '').replace('-', '')
#             if not cleaned.isdigit() or len(cleaned) != 10:
#                 raise serializers.ValidationError("Please enter a valid 10-digit WhatsApp number")
#             return cleaned
#         return value
    
#     def validate_email(self, value):
#         """Validate email format"""
#         if not value:
#             raise serializers.ValidationError("Email is required")
#         email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
#         if not re.match(email_pattern, value):
#             raise serializers.ValidationError("Please enter a valid email address")
#         return value.lower()
    
#     def validate_vendor_name(self, value):
#         """Validate vendor name"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Vendor name is required")
#         return value.strip()
    
#     def validate_address(self, value):
#         """Validate address"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Address is required")
#         return value.strip()
    
#     def validate_contact_person(self, value):
#         """Validate contact person"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Contact person is required")
#         return value.strip()
    
#     def validate_bank_name(self, value):
#         """Validate bank name"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Bank name is required")
#         return value.strip()
    
#     def validate_account_number(self, value):
#         """Validate account number"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Account number is required")
#         return value.strip()
    
#     def validate_job_work_category(self, value):
#         """Validate job work category"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Job work category is required")
#         return value.strip()
    
#     def validate_job_work_sub_category(self, value):
#         """Validate job work sub-category"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Job work sub-category is required")
#         return value.strip()
    
#     def validate_payment_terms(self, value):
#         """Validate payment terms"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Payment terms is required")
#         return value.strip()


# class VendorCodeCreateSerializer(serializers.ModelSerializer):
#     """Serializer for creating vendor code (code is auto-generated)"""
    
#     class Meta:
#         model = VendorCode
#         fields = [
#             'id', 'code', 'vendor_name', 'address', 'gst', 'bank_name',
#             'account_number', 'ifsc_code', 'job_work_category', 'job_work_sub_category',
#             'contact_person', 'whatsapp_number', 'alt_whatsapp_number', 'email',
#             'payment_terms', 'tenant'
#         ]
#         read_only_fields = ['id', 'code']
    
#     def validate_gst(self, value):
#         """Validate GST number format"""
#         if not value:
#             raise serializers.ValidationError("GST number is required")
#         gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
#         if not re.match(gst_pattern, value.upper()):
#             raise serializers.ValidationError("Please enter a valid GST number (e.g., 22AAAAA0000A1Z5)")
#         return value.upper()
    
#     def validate_ifsc_code(self, value):
#         """Validate IFSC code format"""
#         if not value:
#             raise serializers.ValidationError("IFSC code is required")
#         ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
#         if not re.match(ifsc_pattern, value.upper()):
#             raise serializers.ValidationError("Please enter a valid IFSC code (e.g., SBIN0000123)")
#         return value.upper()
    
#     def validate_whatsapp_number(self, value):
#         """Validate WhatsApp number format"""
#         if not value:
#             raise serializers.ValidationError("WhatsApp number is required")
#         cleaned = value.replace(' ', '').replace('-', '')
#         if not cleaned.isdigit() or len(cleaned) != 10:
#             raise serializers.ValidationError("Please enter a valid 10-digit WhatsApp number")
#         return cleaned
    
#     def validate_alt_whatsapp_number(self, value):
#         """Validate alternative WhatsApp number format (optional)"""
#         if value:
#             cleaned = value.replace(' ', '').replace('-', '')
#             if not cleaned.isdigit() or len(cleaned) != 10:
#                 raise serializers.ValidationError("Please enter a valid 10-digit WhatsApp number")
#             return cleaned
#         return value
    
#     def validate_email(self, value):
#         """Validate email format"""
#         if not value:
#             raise serializers.ValidationError("Email is required")
#         email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
#         if not re.match(email_pattern, value):
#             raise serializers.ValidationError("Please enter a valid email address")
#         return value.lower()
    
#     def validate_vendor_name(self, value):
#         """Validate vendor name"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Vendor name is required")
#         return value.strip()
    
#     def validate_address(self, value):
#         """Validate address"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Address is required")
#         return value.strip()
    
#     def validate_contact_person(self, value):
#         """Validate contact person"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Contact person is required")
#         return value.strip()
    
#     def validate_bank_name(self, value):
#         """Validate bank name"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Bank name is required")
#         return value.strip()
    
#     def validate_account_number(self, value):
#         """Validate account number"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Account number is required")
#         return value.strip()
    
#     def validate_job_work_category(self, value):
#         """Validate job work category"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Job work category is required")
#         return value.strip()
    
#     def validate_job_work_sub_category(self, value):
#         """Validate job work sub-category"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Job work sub-category is required")
#         return value.strip()
    
#     def validate_payment_terms(self, value):
#         """Validate payment terms"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Payment terms is required")
#         return value.strip()
    
#     def create(self, validated_data):
#         """Create vendor code with auto-generated code"""
#         request = self.context.get('request')
#         user = request.user if request else None
        
#         # Get tenant from user if not provided
#         if 'tenant' not in validated_data and user and user.tenant:
#             validated_data['tenant'] = user.tenant
        
#         # Create vendor code (code will be auto-generated in save method)
#         vendor_code = VendorCode.objects.create(
#             **validated_data,
#             created_by=user
#         )
        
#         return vendor_code


# class VendorCodeListSerializer(serializers.ModelSerializer):
#     """Lightweight serializer for vendor code list"""
    
#     class Meta:
#         model = VendorCode
#         fields = [
#             'id', 'code', 'vendor_name', 'gst', 'job_work_category',
#             'contact_person', 'email', 'created_at'
#         ]
#         read_only_fields = ['id', 'code', 'created_at']


# """
# Factory Code Serializers - V2
# ==============================

# Comprehensive DRF serializers for the 6-step Factory Code wizard.
# Handles flattened frontend fields → nested JSONField conversion.

# Key Design Patterns:
# - CreateSerializers: Accept flattened frontend fields, transform to model structure
# - ReadSerializers: Return nested JSON for frontend consumption
# - Validation: Category-specific field validation
# - File handling: Base64 or multipart file uploads
# """

# from rest_framework import serializers
# from django.db import transaction
# from .models import (
#     FactoryCode, Product, Component, RawMaterial, WorkOrder,
#     ConsumptionMaterial, ArtworkMaterial, Packaging, PackagingMaterial,
#     TrimAccessoryChoices, ArtworkCategoryChoices, PackagingMaterialTypeChoices,
#     WorkOrderTypeChoices, UnitChoices, SizeUnitChoices,
#     ApprovalChoices, ApprovalAgainstChoices,
#     TRIM_CATEGORY_FIELDS_SCHEMA, ARTWORK_CATEGORY_FIELDS_SCHEMA,
#     PACKAGING_MATERIAL_FIELDS_SCHEMA
# )


# # =============================================================================
# # UTILITY SERIALIZERS
# # =============================================================================

# class SizeSerializer(serializers.Serializer):
#     """Nested size object serializer"""
#     width = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     length = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     height = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     unit = serializers.ChoiceField(choices=SizeUnitChoices.choices, required=False, allow_null=True)


# class ChoiceListSerializer(serializers.Serializer):
#     """Generic serializer for choice list endpoints"""
#     value = serializers.CharField()
#     label = serializers.CharField()


# # =============================================================================
# # STEP 0: FACTORY CODE (Product Identification)
# # =============================================================================

# # class FactoryCodeSerializer(serializers.ModelSerializer):
# #     """Read serializer for FactoryCode"""
    
# #     class Meta:
# #         model = FactoryCode
# #         fields = [
# #             'id', 'code', 'type', 'buyer', 'style_no', 'style_name',
# #             'size', 'gsm', 'article_description', 'colour',
# #             'reference_image', 'created_at', 'updated_at'
# #         ]
# #         read_only_fields = ['id', 'code', 'created_at', 'updated_at']


# # class FactoryCodeCreateSerializer(serializers.ModelSerializer):
# #     """Create serializer for FactoryCode - maps frontend step0 fields"""
    
# #     class Meta:
# #         model = FactoryCode
# #         fields = [
# #             'type', 'buyer', 'style_no', 'style_name',
# #             'size', 'gsm', 'article_description', 'colour',
# #             'reference_image'
# #         ]
    
# #     def create(self, validated_data):
# #         validated_data['tenant'] = self.context['request'].user.tenant
# #         validated_data['created_by'] = self.context['request'].user
# #         return super().create(validated_data)

# class FactoryCodeSerializer(serializers.ModelSerializer):
#     """Read serializer for FactoryCode"""
#     buyer_code_details = BuyerCodeSerializer(source='buyer_code', read_only=True)
    
#     class Meta:
#         model = FactoryCode
#         fields = [
#             'id', 'code', 'sku', 'product_name', 'buyer_code', 'buyer_code_details',
#             'status', 'is_active', 'notes', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'code', 'created_at', 'updated_at']


# class FactoryCodeCreateSerializer(serializers.ModelSerializer):
#     """Create serializer for FactoryCode"""
    
#     class Meta:
#         model = FactoryCode
#         fields = [
#             'sku', 'product_name', 'buyer_code', 'notes'
#         ]
    
#     def create(self, validated_data):
#         validated_data['tenant'] = self.context['request'].user.tenant
#         validated_data['created_by'] = self.context['request'].user
#         return super().create(validated_data)

# # =============================================================================
# # STEP 1: CUT & SEW (Product + Components)
# # =============================================================================

# class ComponentSerializer(serializers.ModelSerializer):
#     """Read serializer for Component"""
#     size = SizeSerializer(source='*', read_only=True)
    
#     class Meta:
#         model = Component
#         fields = [
#             'id', 'name', 'placement', 'remarks', 'surplus',
#             'size', 'unit', 'quantity'
#         ]
    
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         # Nest size fields
#         data['size'] = {
#             'width': instance.size_width,
#             'length': instance.size_length,
#             'height': instance.size_height,
#             'unit': instance.size_unit
#         }
#         return data


# class ComponentCreateSerializer(serializers.ModelSerializer):
#     """Create serializer for Component - accepts flattened size fields"""
#     # Flattened size fields from frontend
#     sizeWidth = serializers.CharField(required=False, allow_blank=True, source='size_width')
#     sizeLength = serializers.CharField(required=False, allow_blank=True, source='size_length')
#     sizeHeight = serializers.CharField(required=False, allow_blank=True, source='size_height')
#     sizeUnit = serializers.ChoiceField(
#         choices=SizeUnitChoices.choices, 
#         required=False, 
#         allow_null=True,
#         source='size_unit'
#     )
    
#     class Meta:
#         model = Component
#         fields = [
#             'name', 'placement', 'remarks', 'surplus',
#             'sizeWidth', 'sizeLength', 'sizeHeight', 'sizeUnit',
#             'unit', 'quantity'
#         ]


# class ProductSerializer(serializers.ModelSerializer):
#     """Read serializer for Product with nested components"""
#     components = ComponentSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'placement', 'components']


# class ProductCreateSerializer(serializers.ModelSerializer):
#     """Create serializer for Product with nested component creation"""
#     components = ComponentCreateSerializer(many=True, required=False)
    
#     class Meta:
#         model = Product
#         fields = ['name', 'placement', 'components']
    
#     def create(self, validated_data):
#         components_data = validated_data.pop('components', [])
#         product = Product.objects.create(**validated_data)
#         for comp_data in components_data:
#             Component.objects.create(product=product, **comp_data)
#         return product


# # =============================================================================
# # STEP 2: RAW MATERIALS & WORK ORDERS
# # =============================================================================

# class WorkOrderSerializer(serializers.ModelSerializer):
#     """Read serializer for WorkOrder with process-specific data"""
#     process_specific_data = serializers.JSONField(read_only=True)
    
#     class Meta:
#         model = WorkOrder
#         fields = [
#             'id', 'process_type', 'process_note', 'process_specific_data'
#         ]


# class WorkOrderCreateSerializer(serializers.Serializer):
#     """
#     Create serializer for WorkOrder - handles conditional process fields
    
#     Frontend sends flat fields like: reed, pick, warp, weft (for WEAVING)
#     We pack them into process_specific_data JSONField
#     """
#     process_type = serializers.ChoiceField(choices=WorkOrderTypeChoices.choices)
#     process_note = serializers.CharField(required=False, allow_blank=True)
    
#     # WEAVING fields
#     reed = serializers.CharField(required=False, allow_blank=True)
#     pick = serializers.CharField(required=False, allow_blank=True)
#     warp = serializers.CharField(required=False, allow_blank=True)
#     weft = serializers.CharField(required=False, allow_blank=True)
    
#     # KNITTING fields
#     wales = serializers.CharField(required=False, allow_blank=True)
#     courses = serializers.CharField(required=False, allow_blank=True)
    
#     # DYEING fields
#     shrinkageWidth = serializers.CharField(required=False, allow_blank=True)
#     shrinkageLength = serializers.CharField(required=False, allow_blank=True)
#     processRoute = serializers.CharField(required=False, allow_blank=True)
    
#     # TUFTING fields
#     tuftGauge = serializers.CharField(required=False, allow_blank=True)
#     stitchRate = serializers.CharField(required=False, allow_blank=True)
#     pileHeight = serializers.CharField(required=False, allow_blank=True)
#     primaryBacking = serializers.CharField(required=False, allow_blank=True)
#     secondaryBacking = serializers.CharField(required=False, allow_blank=True)
    
#     # CUTTING fields
#     cuttingPattern = serializers.CharField(required=False, allow_blank=True)
#     cuttingMethod = serializers.CharField(required=False, allow_blank=True)
    
#     def create(self, validated_data):
#         process_type = validated_data.get('process_type')
#         process_note = validated_data.get('process_note', '')
        
#         # Build process_specific_data based on process_type
#         process_specific_data = {}
        
#         if process_type == 'WEAVING':
#             process_specific_data = {
#                 'reed': validated_data.get('reed', ''),
#                 'pick': validated_data.get('pick', ''),
#                 'warp': validated_data.get('warp', ''),
#                 'weft': validated_data.get('weft', '')
#             }
#         elif process_type == 'KNITTING':
#             process_specific_data = {
#                 'wales': validated_data.get('wales', ''),
#                 'courses': validated_data.get('courses', '')
#             }
#         elif process_type == 'DYEING':
#             process_specific_data = {
#                 'shrinkageWidth': validated_data.get('shrinkageWidth', ''),
#                 'shrinkageLength': validated_data.get('shrinkageLength', ''),
#                 'processRoute': validated_data.get('processRoute', '')
#             }
#         elif process_type == 'TUFTING':
#             process_specific_data = {
#                 'tuftGauge': validated_data.get('tuftGauge', ''),
#                 'stitchRate': validated_data.get('stitchRate', ''),
#                 'pileHeight': validated_data.get('pileHeight', ''),
#                 'primaryBacking': validated_data.get('primaryBacking', ''),
#                 'secondaryBacking': validated_data.get('secondaryBacking', '')
#             }
#         elif process_type == 'CUTTING':
#             process_specific_data = {
#                 'cuttingPattern': validated_data.get('cuttingPattern', ''),
#                 'cuttingMethod': validated_data.get('cuttingMethod', '')
#             }
        
#         return {
#             'process_type': process_type,
#             'process_note': process_note,
#             'process_specific_data': process_specific_data
#         }


# class RawMaterialSerializer(serializers.ModelSerializer):
#     """Read serializer for RawMaterial with nested work orders"""
#     work_orders = WorkOrderSerializer(many=True, read_only=True)
#     size = serializers.SerializerMethodField()
    
#     class Meta:
#         model = RawMaterial
#         fields = [
#             'id', 'component', 'material_name', 'composition',
#             'construction', 'colour', 'gsm', 'finish', 'thread_count',
#             'size', 'consumption', 'consumption_unit', 'surplus',
#             'rate', 'rate_unit', 'approval', 'approval_against',
#             'remarks', 'work_orders'
#         ]
    
#     def get_size(self, obj):
#         return {
#             'width': obj.size_width,
#             'length': obj.size_length,
#             'height': obj.size_height,
#             'unit': obj.size_unit
#         }


# class RawMaterialCreateSerializer(serializers.Serializer):
#     """
#     Create serializer for RawMaterial with nested work orders
#     Accepts flattened frontend structure
#     """
#     component = serializers.UUIDField(required=False, allow_null=True)
#     materialName = serializers.CharField(source='material_name')
#     composition = serializers.CharField(required=False, allow_blank=True)
#     construction = serializers.CharField(required=False, allow_blank=True)
#     colour = serializers.CharField(required=False, allow_blank=True)
#     gsm = serializers.CharField(required=False, allow_blank=True)
#     finish = serializers.CharField(required=False, allow_blank=True)
#     threadCount = serializers.CharField(required=False, allow_blank=True, source='thread_count')
    
#     # Size fields
#     sizeWidth = serializers.CharField(required=False, allow_blank=True)
#     sizeLength = serializers.CharField(required=False, allow_blank=True)
#     sizeHeight = serializers.CharField(required=False, allow_blank=True)
#     sizeUnit = serializers.ChoiceField(
#         choices=SizeUnitChoices.choices, 
#         required=False, 
#         allow_null=True
#     )
    
#     # Consumption
#     consumption = serializers.CharField(required=False, allow_blank=True)
#     consumptionUnit = serializers.ChoiceField(
#         choices=UnitChoices.choices,
#         required=False,
#         allow_null=True,
#         source='consumption_unit'
#     )
#     surplus = serializers.CharField(required=False, allow_blank=True)
    
#     # Rate
#     rate = serializers.CharField(required=False, allow_blank=True)
#     rateUnit = serializers.ChoiceField(
#         choices=UnitChoices.choices,
#         required=False,
#         allow_null=True,
#         source='rate_unit'
#     )
    
#     # Approval
#     approval = serializers.ChoiceField(
#         choices=ApprovalChoices.choices,
#         required=False,
#         allow_null=True
#     )
#     approvalAgainst = serializers.ChoiceField(
#         choices=ApprovalAgainstChoices.choices,
#         required=False,
#         allow_null=True,
#         source='approval_against'
#     )
#     remarks = serializers.CharField(required=False, allow_blank=True)
    
#     # Nested work orders
#     workOrders = WorkOrderCreateSerializer(many=True, required=False)
    
#     def create(self, validated_data):
#         work_orders_data = validated_data.pop('workOrders', [])
        
#         # Map size fields
#         raw_material_data = {
#             'material_name': validated_data.get('material_name', ''),
#             'composition': validated_data.get('composition', ''),
#             'construction': validated_data.get('construction', ''),
#             'colour': validated_data.get('colour', ''),
#             'gsm': validated_data.get('gsm', ''),
#             'finish': validated_data.get('finish', ''),
#             'thread_count': validated_data.get('thread_count', ''),
#             'size_width': validated_data.get('sizeWidth', ''),
#             'size_length': validated_data.get('sizeLength', ''),
#             'size_height': validated_data.get('sizeHeight', ''),
#             'size_unit': validated_data.get('sizeUnit'),
#             'consumption': validated_data.get('consumption', ''),
#             'consumption_unit': validated_data.get('consumption_unit'),
#             'surplus': validated_data.get('surplus', ''),
#             'rate': validated_data.get('rate', ''),
#             'rate_unit': validated_data.get('rate_unit'),
#             'approval': validated_data.get('approval'),
#             'approval_against': validated_data.get('approval_against'),
#             'remarks': validated_data.get('remarks', ''),
#         }
        
#         if validated_data.get('component'):
#             raw_material_data['component_id'] = validated_data['component']
        
#         raw_material = RawMaterial.objects.create(**raw_material_data)
        
#         # Create work orders
#         for wo_data in work_orders_data:
#             wo_serializer = WorkOrderCreateSerializer(data=wo_data)
#             if wo_serializer.is_valid():
#                 wo_result = wo_serializer.save()
#                 WorkOrder.objects.create(
#                     raw_material=raw_material,
#                     process_type=wo_result['process_type'],
#                     process_note=wo_result['process_note'],
#                     process_specific_data=wo_result['process_specific_data']
#                 )
        
#         return raw_material


# # =============================================================================
# # STEP 3: CONSUMPTION MATERIALS (Trims & Accessories) - 30 Categories
# # =============================================================================

# class ConsumptionMaterialSerializer(serializers.ModelSerializer):
#     """Read serializer for ConsumptionMaterial"""
#     size = serializers.SerializerMethodField()
#     category_specific_data = serializers.JSONField(read_only=True)
    
#     class Meta:
#         model = ConsumptionMaterial
#         fields = [
#             'id', 'factory_code', 'category', 'size',
#             'testing_requirement', 'testing_requirement_file',
#             'length_quantity', 'surplus', 'surplus_for_section',
#             'approval', 'remarks', 'unit_additional',
#             'category_specific_data', 'created_at'
#         ]
    
#     def get_size(self, obj):
#         return {
#             'width': obj.size_width,
#             'length': obj.size_length,
#             'height': obj.size_height,
#             'unit': obj.size_unit
#         }


# class ConsumptionMaterialCreateSerializer(serializers.Serializer):
#     """
#     Create serializer for ConsumptionMaterial - handles all 30 trim categories
    
#     Frontend sends flat fields for the selected category.
#     We validate and pack category-specific fields into category_specific_data JSONField.
#     """
    
#     # Required field
#     category = serializers.ChoiceField(choices=TrimAccessoryChoices.choices)
    
#     # Common fields across all categories
#     testingRequirement = serializers.CharField(required=False, allow_blank=True)
#     testingRequirementFile = serializers.FileField(required=False, allow_null=True)
#     lengthQuantity = serializers.CharField(required=False, allow_blank=True)
#     surplus = serializers.CharField(required=False, allow_blank=True)
#     surplusForSection = serializers.CharField(required=False, allow_blank=True)
#     approval = serializers.ChoiceField(
#         choices=ApprovalChoices.choices,
#         required=False,
#         allow_null=True
#     )
#     remarks = serializers.CharField(required=False, allow_blank=True)
#     unitAdditional = serializers.CharField(required=False, allow_blank=True)
    
#     # Size fields
#     sizeWidth = serializers.CharField(required=False, allow_blank=True)
#     sizeLength = serializers.CharField(required=False, allow_blank=True)
#     sizeHeight = serializers.CharField(required=False, allow_blank=True)
#     sizeUnit = serializers.ChoiceField(
#         choices=SizeUnitChoices.choices,
#         required=False,
#         allow_null=True
#     )
    
#     # =========================================================================
#     # CATEGORY-SPECIFIC FIELDS (30 categories)
#     # =========================================================================
    
#     # --- ZIPPERS ---
#     zipNumber = serializers.CharField(required=False, allow_blank=True)
#     zipType = serializers.CharField(required=False, allow_blank=True)
#     zipMaterial = serializers.CharField(required=False, allow_blank=True)
#     sliderType = serializers.CharField(required=False, allow_blank=True)
#     zipColour = serializers.CharField(required=False, allow_blank=True)
#     tapeColour = serializers.CharField(required=False, allow_blank=True)
#     endType = serializers.CharField(required=False, allow_blank=True)
    
#     # --- VELCRO ---
#     velcroType = serializers.CharField(required=False, allow_blank=True)
#     velcroMaterial = serializers.CharField(required=False, allow_blank=True)
#     velcroWidth = serializers.CharField(required=False, allow_blank=True)
#     velcroColour = serializers.CharField(required=False, allow_blank=True)
#     adhesiveBacked = serializers.BooleanField(required=False, allow_null=True)
#     hooksLoops = serializers.CharField(required=False, allow_blank=True)
    
#     # --- STITCHING THREAD ---
#     threadType = serializers.CharField(required=False, allow_blank=True)
#     threadMaterial = serializers.CharField(required=False, allow_blank=True)
#     threadCount = serializers.CharField(required=False, allow_blank=True)
#     threadColour = serializers.CharField(required=False, allow_blank=True)
#     strengthTenacity = serializers.CharField(required=False, allow_blank=True)
#     finish = serializers.CharField(required=False, allow_blank=True)
    
#     # --- BUTTONS ---
#     buttonType = serializers.CharField(required=False, allow_blank=True)
#     buttonMaterial = serializers.CharField(required=False, allow_blank=True)
#     buttonSize = serializers.CharField(required=False, allow_blank=True)
#     buttonColour = serializers.CharField(required=False, allow_blank=True)
#     numberOfHoles = serializers.CharField(required=False, allow_blank=True)
#     buttonFinish = serializers.CharField(required=False, allow_blank=True)
#     logo = serializers.CharField(required=False, allow_blank=True)
    
#     # --- RIVETS ---
#     rivetType = serializers.CharField(required=False, allow_blank=True)
#     rivetMaterial = serializers.CharField(required=False, allow_blank=True)
#     rivetSize = serializers.CharField(required=False, allow_blank=True)
#     rivetColour = serializers.CharField(required=False, allow_blank=True)
#     rivetFinish = serializers.CharField(required=False, allow_blank=True)
#     capDesign = serializers.CharField(required=False, allow_blank=True)
    
#     # --- NIWAR (Webbing/Tapes) ---
#     niwarType = serializers.CharField(required=False, allow_blank=True)
#     niwarMaterial = serializers.CharField(required=False, allow_blank=True)
#     niwarWidth = serializers.CharField(required=False, allow_blank=True)
#     niwarColour = serializers.CharField(required=False, allow_blank=True)
#     pattern = serializers.CharField(required=False, allow_blank=True)
#     tensileStrength = serializers.CharField(required=False, allow_blank=True)
    
#     # --- LACE ---
#     laceType = serializers.CharField(required=False, allow_blank=True)
#     laceMaterial = serializers.CharField(required=False, allow_blank=True)
#     laceWidth = serializers.CharField(required=False, allow_blank=True)
#     laceColour = serializers.CharField(required=False, allow_blank=True)
#     lacePattern = serializers.CharField(required=False, allow_blank=True)
#     edgeFinish = serializers.CharField(required=False, allow_blank=True)
    
#     # --- INTERLINING/FUSING ---
#     interliningType = serializers.CharField(required=False, allow_blank=True)
#     interliningMaterial = serializers.CharField(required=False, allow_blank=True)
#     weight = serializers.CharField(required=False, allow_blank=True)
#     interliningColour = serializers.CharField(required=False, allow_blank=True)
#     adhesiveType = serializers.CharField(required=False, allow_blank=True)
#     fusingTemperature = serializers.CharField(required=False, allow_blank=True)
    
#     # --- HOOKS & EYES ---
#     hookEyeType = serializers.CharField(required=False, allow_blank=True)
#     hookEyeMaterial = serializers.CharField(required=False, allow_blank=True)
#     hookEyeSize = serializers.CharField(required=False, allow_blank=True)
#     hookEyeColour = serializers.CharField(required=False, allow_blank=True)
#     hookEyeFinish = serializers.CharField(required=False, allow_blank=True)
#     closureStrength = serializers.CharField(required=False, allow_blank=True)
    
#     # --- BUCKLES & ADJUSTERS ---
#     buckleType = serializers.CharField(required=False, allow_blank=True)
#     buckleMaterial = serializers.CharField(required=False, allow_blank=True)
#     buckleSize = serializers.CharField(required=False, allow_blank=True)
#     buckleColour = serializers.CharField(required=False, allow_blank=True)
#     buckleFinish = serializers.CharField(required=False, allow_blank=True)
#     strapWidth = serializers.CharField(required=False, allow_blank=True)
    
#     # --- EYELETS & GROMMETS ---
#     eyeletType = serializers.CharField(required=False, allow_blank=True)
#     eyeletMaterial = serializers.CharField(required=False, allow_blank=True)
#     innerDiameter = serializers.CharField(required=False, allow_blank=True)
#     outerDiameter = serializers.CharField(required=False, allow_blank=True)
#     eyeletColour = serializers.CharField(required=False, allow_blank=True)
#     eyeletFinish = serializers.CharField(required=False, allow_blank=True)
    
#     # --- ELASTIC ---
#     elasticType = serializers.CharField(required=False, allow_blank=True)
#     elasticMaterial = serializers.CharField(required=False, allow_blank=True)
#     elasticWidth = serializers.CharField(required=False, allow_blank=True)
#     elasticColour = serializers.CharField(required=False, allow_blank=True)
#     stretchPercent = serializers.CharField(required=False, allow_blank=True)
#     elasticFinish = serializers.CharField(required=False, allow_blank=True)
    
#     # --- FELT ---
#     feltType = serializers.CharField(required=False, allow_blank=True)
#     feltMaterial = serializers.CharField(required=False, allow_blank=True)
#     feltThickness = serializers.CharField(required=False, allow_blank=True)
#     feltColour = serializers.CharField(required=False, allow_blank=True)
#     feltDensity = serializers.CharField(required=False, allow_blank=True)
#     feltFinish = serializers.CharField(required=False, allow_blank=True)
    
#     # --- SHOULDER PADS ---
#     padType = serializers.CharField(required=False, allow_blank=True)
#     padMaterial = serializers.CharField(required=False, allow_blank=True)
#     padSize = serializers.CharField(required=False, allow_blank=True)
#     padThickness = serializers.CharField(required=False, allow_blank=True)
#     padColour = serializers.CharField(required=False, allow_blank=True)
#     padShape = serializers.CharField(required=False, allow_blank=True)
#     covering = serializers.CharField(required=False, allow_blank=True)
    
#     # --- TUBULAR KNITS / RIBBING ---
#     tubularType = serializers.CharField(required=False, allow_blank=True)
#     tubularMaterial = serializers.CharField(required=False, allow_blank=True)
#     widthDiameter = serializers.CharField(required=False, allow_blank=True)
#     weightDensity = serializers.CharField(required=False, allow_blank=True)
#     tubularColour = serializers.CharField(required=False, allow_blank=True)
#     # stretchPercent shared with ELASTIC
#     cutting = serializers.CharField(required=False, allow_blank=True)
    
#     # --- RFID / EAS TAGS ---
#     rfidType = serializers.CharField(required=False, allow_blank=True)
#     formFactor = serializers.CharField(required=False, allow_blank=True)
#     frequency = serializers.CharField(required=False, allow_blank=True)
#     chipIcType = serializers.CharField(required=False, allow_blank=True)
#     rfidSize = serializers.CharField(required=False, allow_blank=True)
#     coding = serializers.CharField(required=False, allow_blank=True)
#     security = serializers.CharField(required=False, allow_blank=True)
    
#     # --- PLASTIC CABLE TIES / LOOPS ---
#     cableTieType = serializers.CharField(required=False, allow_blank=True)
#     cableTieMaterial = serializers.CharField(required=False, allow_blank=True)
#     cableTieSize = serializers.CharField(required=False, allow_blank=True)
#     cableTieColour = serializers.CharField(required=False, allow_blank=True)
#     cableTieTensileStrength = serializers.CharField(required=False, allow_blank=True)
#     cableTieFinish = serializers.CharField(required=False, allow_blank=True)
#     cableTieUsage = serializers.CharField(required=False, allow_blank=True)
    
#     # --- FRINGE / TASSELS ---
#     fringeType = serializers.CharField(required=False, allow_blank=True)
#     fringeMaterial = serializers.CharField(required=False, allow_blank=True)
#     dropLength = serializers.CharField(required=False, allow_blank=True)
#     fringeTapeWidth = serializers.CharField(required=False, allow_blank=True)
#     fringeColour = serializers.CharField(required=False, allow_blank=True)
#     fringeFinish = serializers.CharField(required=False, allow_blank=True)
#     construction = serializers.CharField(required=False, allow_blank=True)
    
#     # --- PLASTIC PIPES / RODS ---
#     pipeType = serializers.CharField(required=False, allow_blank=True)
#     pipeMaterial = serializers.CharField(required=False, allow_blank=True)
#     diameterDimensions = serializers.CharField(required=False, allow_blank=True)
#     pipeLength = serializers.CharField(required=False, allow_blank=True)
#     pipeColour = serializers.CharField(required=False, allow_blank=True)
#     endCaps = serializers.CharField(required=False, allow_blank=True)
#     flexibility = serializers.CharField(required=False, allow_blank=True)
#     pipeUsage = serializers.CharField(required=False, allow_blank=True)
    
#     # --- SEAM SEALING TAPE ---
#     seamTapeType = serializers.CharField(required=False, allow_blank=True)
#     seamTapeMaterial = serializers.CharField(required=False, allow_blank=True)
#     seamTapeWidth = serializers.CharField(required=False, allow_blank=True)
#     seamTapeColour = serializers.CharField(required=False, allow_blank=True)
#     seamTapeAdhesiveType = serializers.CharField(required=False, allow_blank=True)
#     applicationSpec = serializers.CharField(required=False, allow_blank=True)
#     elasticity = serializers.CharField(required=False, allow_blank=True)
    
#     # --- ADHESIVES / GUNNING ---
#     adhesiveGunType = serializers.CharField(required=False, allow_blank=True)
#     materialBase = serializers.CharField(required=False, allow_blank=True)
#     adhesiveApplication = serializers.CharField(required=False, allow_blank=True)
#     viscosity = serializers.CharField(required=False, allow_blank=True)
#     settingTime = serializers.CharField(required=False, allow_blank=True)
#     adhesiveColour = serializers.CharField(required=False, allow_blank=True)
#     applicator = serializers.CharField(required=False, allow_blank=True)
    
#     # --- PRE-CUT HEMS / BINDINGS ---
#     hemType = serializers.CharField(required=False, allow_blank=True)
#     hemMaterial = serializers.CharField(required=False, allow_blank=True)
#     cutType = serializers.CharField(required=False, allow_blank=True)
#     hemWidth = serializers.CharField(required=False, allow_blank=True)
#     foldType = serializers.CharField(required=False, allow_blank=True)
#     hemColour = serializers.CharField(required=False, allow_blank=True)
#     hemPackaging = serializers.CharField(required=False, allow_blank=True)
    
#     # --- REFLECTIVE TAPES / TRIMS ---
#     reflectiveType = serializers.CharField(required=False, allow_blank=True)
#     reflectiveMaterial = serializers.CharField(required=False, allow_blank=True)
#     reflectiveWidth = serializers.CharField(required=False, allow_blank=True)
#     reflectiveColour = serializers.CharField(required=False, allow_blank=True)
#     certification = serializers.CharField(required=False, allow_blank=True)
#     baseFabric = serializers.CharField(required=False, allow_blank=True)
    
#     # --- FIRE RETARDANT (FR) TRIMS ---
#     frType = serializers.CharField(required=False, allow_blank=True)
#     frMaterial = serializers.CharField(required=False, allow_blank=True)
#     complianceLevel = serializers.CharField(required=False, allow_blank=True)
#     frColour = serializers.CharField(required=False, allow_blank=True)
#     durability = serializers.CharField(required=False, allow_blank=True)
#     frComponents = serializers.CharField(required=False, allow_blank=True)
    
#     # --- REPAIR KITS / PATCHES ---
#     repairKitType = serializers.CharField(required=False, allow_blank=True)
#     repairKitMaterial = serializers.CharField(required=False, allow_blank=True)
#     sizeShape = serializers.CharField(required=False, allow_blank=True)
#     repairKitColour = serializers.CharField(required=False, allow_blank=True)
#     repairKitPackaging = serializers.CharField(required=False, allow_blank=True)
#     userApplication = serializers.CharField(required=False, allow_blank=True)
#     contents = serializers.CharField(required=False, allow_blank=True)
    
#     # --- CORD STOPS / CORD LOCKS / TOGGLES ---
#     cordStopType = serializers.CharField(required=False, allow_blank=True)
#     cordStopMaterial = serializers.CharField(required=False, allow_blank=True)
#     cordStopSize = serializers.CharField(required=False, allow_blank=True)
#     cordStopColour = serializers.CharField(required=False, allow_blank=True)
#     lockingMechanism = serializers.CharField(required=False, allow_blank=True)
#     cordStopFunction = serializers.CharField(required=False, allow_blank=True)
    
#     # --- D-RINGS / O-RINGS / WEBBING LOOPS ---
#     dRingType = serializers.CharField(required=False, allow_blank=True)
#     dRingMaterial = serializers.CharField(required=False, allow_blank=True)
#     dRingSize = serializers.CharField(required=False, allow_blank=True)
#     thicknessGauge = serializers.CharField(required=False, allow_blank=True)
#     dRingFinishPlating = serializers.CharField(required=False, allow_blank=True)
#     loadRating = serializers.CharField(required=False, allow_blank=True)
#     dRingApplication = serializers.CharField(required=False, allow_blank=True)
    
#     # --- FOAM / WADDING (Pre-Cut Shapes) ---
#     foamType = serializers.CharField(required=False, allow_blank=True)
#     foamDensity = serializers.CharField(required=False, allow_blank=True)
#     foamThickness = serializers.CharField(required=False, allow_blank=True)
#     shapeId = serializers.CharField(required=False, allow_blank=True)
#     foamColour = serializers.CharField(required=False, allow_blank=True)
#     properties = serializers.CharField(required=False, allow_blank=True)
#     foamAttachment = serializers.CharField(required=False, allow_blank=True)
    
#     # --- PINS / TAGGING BARBS ---
#     pinType = serializers.CharField(required=False, allow_blank=True)
#     pinMaterial = serializers.CharField(required=False, allow_blank=True)
#     pinSize = serializers.CharField(required=False, allow_blank=True)
#     pinColour = serializers.CharField(required=False, allow_blank=True)
#     pinTensileStrength = serializers.CharField(required=False, allow_blank=True)
#     headType = serializers.CharField(required=False, allow_blank=True)
#     pinApplication = serializers.CharField(required=False, allow_blank=True)
    
#     # --- MAGNETIC CLOSURES / SNAPS ---
#     magneticType = serializers.CharField(required=False, allow_blank=True)
#     magneticMaterial = serializers.CharField(required=False, allow_blank=True)
#     magneticSize = serializers.CharField(required=False, allow_blank=True)
#     magneticStrength = serializers.CharField(required=False, allow_blank=True)
#     polarity = serializers.CharField(required=False, allow_blank=True)
#     magneticApplication = serializers.CharField(required=False, allow_blank=True)
    
#     def _get_category_specific_fields(self, category, validated_data):
#         """
#         Extract category-specific fields based on the selected category.
#         Returns a dict of the relevant fields for that category.
#         """
#         category_field_map = {
#             'ZIPPERS': [
#                 'zipNumber', 'zipType', 'zipMaterial', 'sliderType',
#                 'zipColour', 'tapeColour', 'endType'
#             ],
#             'VELCRO': [
#                 'velcroType', 'velcroMaterial', 'velcroWidth', 'velcroColour',
#                 'adhesiveBacked', 'hooksLoops'
#             ],
#             'STITCHING THREAD': [
#                 'threadType', 'threadMaterial', 'threadCount', 'threadColour',
#                 'strengthTenacity', 'finish'
#             ],
#             'BUTTONS': [
#                 'buttonType', 'buttonMaterial', 'buttonSize', 'buttonColour',
#                 'numberOfHoles', 'buttonFinish', 'logo'
#             ],
#             'RIVETS': [
#                 'rivetType', 'rivetMaterial', 'rivetSize', 'rivetColour',
#                 'rivetFinish', 'capDesign'
#             ],
#             'NIWAR (Webbing/Tapes)': [
#                 'niwarType', 'niwarMaterial', 'niwarWidth', 'niwarColour',
#                 'pattern', 'tensileStrength'
#             ],
#             'LACE': [
#                 'laceType', 'laceMaterial', 'laceWidth', 'laceColour',
#                 'lacePattern', 'edgeFinish'
#             ],
#             'INTERLINING/FUSING': [
#                 'interliningType', 'interliningMaterial', 'weight', 'interliningColour',
#                 'adhesiveType', 'fusingTemperature'
#             ],
#             'HOOKS & EYES': [
#                 'hookEyeType', 'hookEyeMaterial', 'hookEyeSize', 'hookEyeColour',
#                 'hookEyeFinish', 'closureStrength'
#             ],
#             'BUCKLES & ADJUSTERS': [
#                 'buckleType', 'buckleMaterial', 'buckleSize', 'buckleColour',
#                 'buckleFinish', 'strapWidth'
#             ],
#             'EYELETS & GROMMETS': [
#                 'eyeletType', 'eyeletMaterial', 'innerDiameter', 'outerDiameter',
#                 'eyeletColour', 'eyeletFinish'
#             ],
#             'ELASTIC': [
#                 'elasticType', 'elasticMaterial', 'elasticWidth', 'elasticColour',
#                 'stretchPercent', 'elasticFinish'
#             ],
#             'FELT': [
#                 'feltType', 'feltMaterial', 'feltThickness', 'feltColour',
#                 'feltDensity', 'feltFinish'
#             ],
#             'SHOULDER PADS': [
#                 'padType', 'padMaterial', 'padSize', 'padThickness',
#                 'padColour', 'padShape', 'covering'
#             ],
#             'TUBULAR KNITS / RIBBING': [
#                 'tubularType', 'tubularMaterial', 'widthDiameter', 'weightDensity',
#                 'tubularColour', 'stretchPercent', 'cutting'
#             ],
#             'RFID / EAS TAGS': [
#                 'rfidType', 'formFactor', 'frequency', 'chipIcType',
#                 'rfidSize', 'coding', 'security'
#             ],
#             'PLASTIC CABLE TIES / LOOPS': [
#                 'cableTieType', 'cableTieMaterial', 'cableTieSize', 'cableTieColour',
#                 'cableTieTensileStrength', 'cableTieFinish', 'cableTieUsage'
#             ],
#             'FRINGE / TASSELS': [
#                 'fringeType', 'fringeMaterial', 'dropLength', 'fringeTapeWidth',
#                 'fringeColour', 'fringeFinish', 'construction'
#             ],
#             'PLASTIC PIPES / RODS': [
#                 'pipeType', 'pipeMaterial', 'diameterDimensions', 'pipeLength',
#                 'pipeColour', 'endCaps', 'flexibility', 'pipeUsage'
#             ],
#             'SEAM SEALING TAPE': [
#                 'seamTapeType', 'seamTapeMaterial', 'seamTapeWidth', 'seamTapeColour',
#                 'seamTapeAdhesiveType', 'applicationSpec', 'elasticity'
#             ],
#             'ADHESIVES / GUNNING': [
#                 'adhesiveGunType', 'materialBase', 'adhesiveApplication', 'viscosity',
#                 'settingTime', 'adhesiveColour', 'applicator'
#             ],
#             'PRE-CUT HEMS / BINDINGS': [
#                 'hemType', 'hemMaterial', 'cutType', 'hemWidth',
#                 'foldType', 'hemColour', 'hemPackaging'
#             ],
#             'REFLECTIVE TAPES / TRIMS': [
#                 'reflectiveType', 'reflectiveMaterial', 'reflectiveWidth', 'reflectiveColour',
#                 'certification', 'baseFabric'
#             ],
#             'FIRE RETARDANT (FR) TRIMS': [
#                 'frType', 'frMaterial', 'complianceLevel', 'frColour',
#                 'durability', 'frComponents'
#             ],
#             'REPAIR KITS / PATCHES': [
#                 'repairKitType', 'repairKitMaterial', 'sizeShape', 'repairKitColour',
#                 'repairKitPackaging', 'userApplication', 'contents'
#             ],
#             'CORD STOPS / CORD LOCKS / TOGGLES': [
#                 'cordStopType', 'cordStopMaterial', 'cordStopSize', 'cordStopColour',
#                 'lockingMechanism', 'cordStopFunction'
#             ],
#             'D-RINGS / O-RINGS / WEBBING LOOPS': [
#                 'dRingType', 'dRingMaterial', 'dRingSize', 'thicknessGauge',
#                 'dRingFinishPlating', 'loadRating', 'dRingApplication'
#             ],
#             'FOAM / WADDING (Pre-Cut Shapes)': [
#                 'foamType', 'foamDensity', 'foamThickness', 'shapeId',
#                 'foamColour', 'properties', 'foamAttachment'
#             ],
#             'PINS / TAGGING BARBS': [
#                 'pinType', 'pinMaterial', 'pinSize', 'pinColour',
#                 'pinTensileStrength', 'headType', 'pinApplication'
#             ],
#             'MAGNETIC CLOSURES / SNAPS': [
#                 'magneticType', 'magneticMaterial', 'magneticSize', 'magneticStrength',
#                 'polarity', 'magneticApplication'
#             ]
#         }
        
#         fields = category_field_map.get(category, [])
#         return {field: validated_data.get(field, '') for field in fields if field in validated_data}
    
#     def create(self, validated_data):
#         category = validated_data['category']
        
#         # Extract category-specific fields
#         category_specific_data = self._get_category_specific_fields(category, validated_data)
        
#         # Build model data
#         model_data = {
#             'factory_code_id': self.context.get('factory_code_id'),
#             'category': category,
#             'testing_requirement': validated_data.get('testingRequirement', ''),
#             'testing_requirement_file': validated_data.get('testingRequirementFile'),
#             'length_quantity': validated_data.get('lengthQuantity', ''),
#             'surplus': validated_data.get('surplus', ''),
#             'surplus_for_section': validated_data.get('surplusForSection', ''),
#             'approval': validated_data.get('approval'),
#             'remarks': validated_data.get('remarks', ''),
#             'unit_additional': validated_data.get('unitAdditional', ''),
#             'size_width': validated_data.get('sizeWidth', ''),
#             'size_length': validated_data.get('sizeLength', ''),
#             'size_height': validated_data.get('sizeHeight', ''),
#             'size_unit': validated_data.get('sizeUnit'),
#             'category_specific_data': category_specific_data
#         }
        
#         return ConsumptionMaterial.objects.create(**model_data)


# # =============================================================================
# # STEP 4: ARTWORK MATERIALS - 18 Categories
# # =============================================================================

# class ArtworkMaterialSerializer(serializers.ModelSerializer):
#     """Read serializer for ArtworkMaterial"""
#     size = serializers.SerializerMethodField()
#     category_specific_data = serializers.JSONField(read_only=True)
    
#     class Meta:
#         model = ArtworkMaterial
#         fields = [
#             'id', 'factory_code', 'category', 'size',
#             'surplus', 'surplus_for_section', 'usage',
#             'approval', 'remarks', 'reference_image',
#             'category_specific_data', 'created_at'
#         ]
    
#     def get_size(self, obj):
#         return {
#             'width': obj.size_width,
#             'length': obj.size_length,
#             'height': obj.size_height,
#             'unit': obj.size_unit
#         }


# class ArtworkMaterialCreateSerializer(serializers.Serializer):
#     """
#     Create serializer for ArtworkMaterial - handles all 18 artwork categories
#     """
    
#     # Required field
#     category = serializers.ChoiceField(choices=ArtworkCategoryChoices.choices)
    
#     # Common fields
#     surplus = serializers.CharField(required=False, allow_blank=True)
#     surplusForSection = serializers.CharField(required=False, allow_blank=True)
#     usage = serializers.CharField(required=False, allow_blank=True)
#     approval = serializers.ChoiceField(
#         choices=ApprovalChoices.choices,
#         required=False,
#         allow_null=True
#     )
#     remarks = serializers.CharField(required=False, allow_blank=True)
#     referenceImage = serializers.FileField(required=False, allow_null=True)
    
#     # Size fields
#     sizeWidth = serializers.CharField(required=False, allow_blank=True)
#     sizeLength = serializers.CharField(required=False, allow_blank=True)
#     sizeHeight = serializers.CharField(required=False, allow_blank=True)
#     sizeUnit = serializers.ChoiceField(
#         choices=SizeUnitChoices.choices,
#         required=False,
#         allow_null=True
#     )
    
#     # =========================================================================
#     # CATEGORY-SPECIFIC FIELDS (18 categories)
#     # =========================================================================
    
#     # Common artwork fields used across multiple categories
#     specificType = serializers.CharField(required=False, allow_blank=True)
#     material = serializers.CharField(required=False, allow_blank=True)
#     sizeShape = serializers.CharField(required=False, allow_blank=True)
#     colours = serializers.CharField(required=False, allow_blank=True)
#     finishing = serializers.CharField(required=False, allow_blank=True)
#     permanence = serializers.CharField(required=False, allow_blank=True)
#     permanenceFile = serializers.FileField(required=False, allow_null=True)
    
#     # Category-specific additional fields
#     content = serializers.CharField(required=False, allow_blank=True)  # Labels, Tags, Insert Cards
#     ribbonWidth = serializers.CharField(required=False, allow_blank=True)  # Ribbons
#     printingMethod = serializers.CharField(required=False, allow_blank=True)  # Various print categories
#     fabricType = serializers.CharField(required=False, allow_blank=True)  # Printed Fabric Labels
#     sealType = serializers.CharField(required=False, allow_blank=True)  # Security Seals
#     serialization = serializers.CharField(required=False, allow_blank=True)  # Security Seals
#     tamperEvidence = serializers.CharField(required=False, allow_blank=True)  # Security Seals
#     printingSpec = serializers.CharField(required=False, allow_blank=True)  # Heat Transfers
#     adhesiveStrength = serializers.CharField(required=False, allow_blank=True)  # Heat Transfers, Stickers
#     strapWidth = serializers.CharField(required=False, allow_blank=True)  # Straps/Belts
#     buckleType = serializers.CharField(required=False, allow_blank=True)  # Straps/Belts
#     badgeType = serializers.CharField(required=False, allow_blank=True)  # Embroidered Badges
#     borderFinish = serializers.CharField(required=False, allow_blank=True)  # Embroidered Badges
#     patchSize = serializers.CharField(required=False, allow_blank=True)  # Leather/PU Patches
#     embossDeboss = serializers.CharField(required=False, allow_blank=True)  # Leather/PU Patches
#     attachmentMethod = serializers.CharField(required=False, allow_blank=True)  # Leather/PU Patches
#     charmSize = serializers.CharField(required=False, allow_blank=True)  # Metal Charms
#     metalFinish = serializers.CharField(required=False, allow_blank=True)  # Metal Charms
#     engraving = serializers.CharField(required=False, allow_blank=True)  # Metal Charms
#     joiningType = serializers.CharField(required=False, allow_blank=True)  # Metal Charms
#     threadColours = serializers.CharField(required=False, allow_blank=True)  # Embroidery Thread
#     stitchDensity = serializers.CharField(required=False, allow_blank=True)  # Embroidery Thread
#     backingType = serializers.CharField(required=False, allow_blank=True)  # Embroidery Thread
#     screenCount = serializers.CharField(required=False, allow_blank=True)  # Screen Print Transfers
#     inkType = serializers.CharField(required=False, allow_blank=True)  # Screen Print Transfers
#     applicationMethod = serializers.CharField(required=False, allow_blank=True)  # Screen Print Transfers
#     tagType = serializers.CharField(required=False, allow_blank=True)  # Price Tags
#     attachmentType = serializers.CharField(required=False, allow_blank=True)  # Price Tags
#     qrBarcode = serializers.CharField(required=False, allow_blank=True)  # Price Tags
    
#     def _get_category_specific_fields(self, category, validated_data):
#         """Extract category-specific fields based on the selected artwork category."""
        
#         # Base fields common to most artwork categories
#         base_artwork_fields = [
#             'specificType', 'material', 'sizeShape', 'colours', 'finishing', 'permanence'
#         ]
        
#         category_additional_fields = {
#             'MAIN LABELS': ['content'],
#             'CARE LABELS': ['content'],
#             'SIZE LABELS': ['content'],
#             'FLAG LABELS': ['content'],
#             'HANG TAGS': ['content'],
#             'BARCODE STICKERS': ['content'],
#             'PRINTED FABRIC LABELS': ['content', 'fabricType', 'printingMethod'],
#             'WOVEN LABELS': ['content'],
#             'INSERT CARDS': ['content'],
#             'RIBBONS': ['ribbonWidth'],
#             'SECURITY SEALS / TAMPER TAGS': ['sealType', 'serialization', 'tamperEvidence'],
#             'HEAT TRANSFER LABELS / PRINTS': ['printingSpec', 'adhesiveStrength', 'applicationMethod'],
#             'PRINTED / BRANDED STRAPS / BELTS': ['strapWidth', 'buckleType'],
#             'EMBROIDERED BADGES / PATCHES': ['badgeType', 'borderFinish'],
#             'LEATHER / PU PATCHES': ['patchSize', 'embossDeboss', 'attachmentMethod'],
#             'METAL CHARMS / LOGO PLATES': ['charmSize', 'metalFinish', 'engraving', 'joiningType'],
#             'EMBROIDERY THREAD / DESIGN': ['threadColours', 'stitchDensity', 'backingType'],
#             'SCREEN PRINT / TRANSFERS': ['screenCount', 'inkType', 'applicationMethod'],
#             'PRICE TAGS / JOKER TAGS': ['tagType', 'attachmentType', 'qrBarcode']
#         }
        
#         # Get additional fields for this category
#         additional = category_additional_fields.get(category, [])
#         all_fields = base_artwork_fields + additional
        
#         return {field: validated_data.get(field, '') for field in all_fields if field in validated_data}
    
#     def create(self, validated_data):
#         category = validated_data['category']
        
#         # Extract category-specific fields
#         category_specific_data = self._get_category_specific_fields(category, validated_data)
        
#         # Handle permanence file if present
#         if validated_data.get('permanenceFile'):
#             category_specific_data['permanenceFile'] = 'uploaded'  # Actual file handling in view
        
#         # Build model data
#         model_data = {
#             'factory_code_id': self.context.get('factory_code_id'),
#             'category': category,
#             'surplus': validated_data.get('surplus', ''),
#             'surplus_for_section': validated_data.get('surplusForSection', ''),
#             'usage': validated_data.get('usage', ''),
#             'approval': validated_data.get('approval'),
#             'remarks': validated_data.get('remarks', ''),
#             'reference_image': validated_data.get('referenceImage'),
#             'size_width': validated_data.get('sizeWidth', ''),
#             'size_length': validated_data.get('sizeLength', ''),
#             'size_height': validated_data.get('sizeHeight', ''),
#             'size_unit': validated_data.get('sizeUnit'),
#             'category_specific_data': category_specific_data
#         }
        
#         return ArtworkMaterial.objects.create(**model_data)


# # =============================================================================
# # STEP 5: PACKAGING
# # =============================================================================

# class PackagingMaterialSerializer(serializers.ModelSerializer):
#     """Read serializer for PackagingMaterial"""
#     size = serializers.SerializerMethodField()
#     material_specific_data = serializers.JSONField(read_only=True)
    
#     class Meta:
#         model = PackagingMaterial
#         fields = [
#             'id', 'packaging', 'material_type', 'size',
#             'colour', 'printing', 'printing_ref',
#             'material_specific_data', 'created_at'
#         ]
    
#     def get_size(self, obj):
#         return {
#             'width': obj.size_width,
#             'length': obj.size_length,
#             'height': obj.size_height,
#             'unit': obj.size_unit
#         }


# class PackagingMaterialCreateSerializer(serializers.Serializer):
#     """
#     Create serializer for PackagingMaterial with conditional fields based on material type
#     """
    
#     # Required field
#     materialType = serializers.ChoiceField(
#         choices=PackagingMaterialTypeChoices.choices,
#         source='material_type'
#     )
    
#     # Common fields
#     colour = serializers.CharField(required=False, allow_blank=True)
#     printing = serializers.CharField(required=False, allow_blank=True)
#     printingRef = serializers.FileField(required=False, allow_null=True)
    
#     # Size fields
#     sizeWidth = serializers.CharField(required=False, allow_blank=True)
#     sizeLength = serializers.CharField(required=False, allow_blank=True)
#     sizeHeight = serializers.CharField(required=False, allow_blank=True)
#     sizeUnit = serializers.ChoiceField(
#         choices=SizeUnitChoices.choices,
#         required=False,
#         allow_null=True
#     )
    
#     # Material-specific fields
#     # CARTONS/CORRUGATED BOX
#     noOfPlys = serializers.CharField(required=False, allow_blank=True)
#     jointType = serializers.CharField(required=False, allow_blank=True)
#     burstingStrength = serializers.CharField(required=False, allow_blank=True)
    
#     # POLY BAG WITH FLAP
#     guage = serializers.CharField(required=False, allow_blank=True)
#     gummingQuality = serializers.CharField(required=False, allow_blank=True)
#     punchHoles = serializers.CharField(required=False, allow_blank=True)
    
#     # POLYSHEET / BALE WRAP
#     guageGsm = serializers.CharField(required=False, allow_blank=True)
#     rollWidth = serializers.CharField(required=False, allow_blank=True)
#     rollWidthUnit = serializers.CharField(required=False, allow_blank=True)
    
#     # POLY BAG WITH FLAP
#     flapSize = serializers.CharField(required=False, allow_blank=True)
    
#     # TAPE
#     tapeWidth = serializers.CharField(required=False, allow_blank=True)
#     tapeWidthUnit = serializers.CharField(required=False, allow_blank=True)
    
#     def _get_material_specific_fields(self, material_type, validated_data):
#         """Extract material-specific fields based on the selected material type."""
        
#         material_field_map = {
#             'CARTONS/CORRUGATED BOX': ['noOfPlys', 'jointType', 'burstingStrength'],
#             'MASTER CARTONS': ['noOfPlys', 'jointType', 'burstingStrength'],
#             'INNER CARTONS': ['noOfPlys', 'jointType', 'burstingStrength'],
#             'POLY BAG WITH FLAP': ['guage', 'gummingQuality', 'punchHoles', 'flapSize'],
#             'POLYSHEET': ['guageGsm', 'rollWidth', 'rollWidthUnit'],
#             'BALE WRAP': ['guageGsm', 'rollWidth', 'rollWidthUnit'],
#             'TAPE': ['guage', 'gummingQuality', 'tapeWidth', 'tapeWidthUnit'],
#             'TISSUE / WRAPPING PAPER': []
#         }
        
#         fields = material_field_map.get(material_type, [])
#         return {field: validated_data.get(field, '') for field in fields if field in validated_data}
    
#     def create(self, validated_data):
#         material_type = validated_data['material_type']
        
#         # Extract material-specific fields
#         material_specific_data = self._get_material_specific_fields(material_type, validated_data)
        
#         # Build model data
#         model_data = {
#             'packaging_id': self.context.get('packaging_id'),
#             'material_type': material_type,
#             'colour': validated_data.get('colour', ''),
#             'printing': validated_data.get('printing', ''),
#             'printing_ref': validated_data.get('printingRef'),
#             'size_width': validated_data.get('sizeWidth', ''),
#             'size_length': validated_data.get('sizeLength', ''),
#             'size_height': validated_data.get('sizeHeight', ''),
#             'size_unit': validated_data.get('sizeUnit'),
#             'material_specific_data': material_specific_data
#         }
        
#         return PackagingMaterial.objects.create(**model_data)


# class PackagingSerializer(serializers.ModelSerializer):
#     """Read serializer for Packaging with nested materials"""
#     materials = PackagingMaterialSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Packaging
#         fields = [
#             'id', 'factory_code', 'packing_method', 'polybag_type',
#             'silica_gel', 'remarks', 'materials', 'created_at'
#         ]


# class PackagingCreateSerializer(serializers.ModelSerializer):
#     """Create serializer for Packaging"""
#     materials = PackagingMaterialCreateSerializer(many=True, required=False)
    
#     class Meta:
#         model = Packaging
#         fields = ['packing_method', 'polybag_type', 'silica_gel', 'remarks', 'materials']
    
#     def create(self, validated_data):
#         materials_data = validated_data.pop('materials', [])
#         factory_code_id = self.context.get('factory_code_id')
        
#         packaging = Packaging.objects.create(
#             factory_code_id=factory_code_id,
#             **validated_data
#         )
        
#         for mat_data in materials_data:
#             mat_serializer = PackagingMaterialCreateSerializer(
#                 data=mat_data,
#                 context={'packaging_id': packaging.id}
#             )
#             if mat_serializer.is_valid():
#                 mat_serializer.save()
        
#         return packaging


# # =============================================================================
# # COMPLETE FACTORY CODE WIZARD SERIALIZER
# # =============================================================================

# class FactoryCodeCompleteSerializer(serializers.ModelSerializer):
#     """
#     Complete read serializer for entire Factory Code with all nested data.
#     Used for retrieving the complete factory code specification.
#     """
#     products = ProductSerializer(many=True, read_only=True)
#     consumption_materials = ConsumptionMaterialSerializer(many=True, read_only=True)
#     artwork_materials = ArtworkMaterialSerializer(many=True, read_only=True)
#     packaging = PackagingSerializer(read_only=True)
    
#     class Meta:
#         model = FactoryCode
#         fields = [
#             'id', 'code', 'type', 'buyer', 'style_no', 'style_name',
#             'size', 'gsm', 'article_description', 'colour',
#             'reference_image', 'products', 'consumption_materials',
#             'artwork_materials', 'packaging',
#             'created_at', 'updated_at', 'created_by'
#         ]
#         read_only_fields = ['id', 'code', 'created_at', 'updated_at', 'created_by']


# class FactoryCodeWizardCreateSerializer(serializers.Serializer):
#     """
#     Complete wizard create serializer - accepts the entire 6-step form data
#     and creates all related objects in a single transaction.
#     """
    
#     # Step 0: Product Identification
#     step0 = FactoryCodeCreateSerializer()
    
#     # Step 1: Cut & Sew
#     products = ProductCreateSerializer(many=True, required=False)
    
#     # Step 2: Raw Materials (nested within products/components)
#     rawMaterials = RawMaterialCreateSerializer(many=True, required=False)
    
#     # Step 3: Consumption Materials
#     consumptionMaterials = ConsumptionMaterialCreateSerializer(many=True, required=False)
    
#     # Step 4: Artwork Materials
#     artworkMaterials = ArtworkMaterialCreateSerializer(many=True, required=False)
    
#     # Step 5: Packaging
#     packaging = PackagingCreateSerializer(required=False)
    
#     @transaction.atomic
#     def create(self, validated_data):
#         request = self.context['request']
        
#         # Step 0: Create Factory Code
#         step0_data = validated_data['step0']
#         step0_data['tenant'] = request.user.tenant
#         step0_data['created_by'] = request.user
#         factory_code = FactoryCode.objects.create(**step0_data)
        
#         # Step 1: Create Products and Components
#         products_data = validated_data.get('products', [])
#         for prod_data in products_data:
#             components_data = prod_data.pop('components', [])
#             product = Product.objects.create(factory_code=factory_code, **prod_data)
#             for comp_data in components_data:
#                 Component.objects.create(product=product, **comp_data)
        
#         # Step 2: Raw Materials would be created per component
#         # (simplified - in real implementation, would link to components)
#         raw_materials_data = validated_data.get('rawMaterials', [])
#         for rm_data in raw_materials_data:
#             rm_serializer = RawMaterialCreateSerializer(data=rm_data)
#             if rm_serializer.is_valid():
#                 rm_serializer.save()
        
#         # Step 3: Consumption Materials
#         consumption_data = validated_data.get('consumptionMaterials', [])
#         for cm_data in consumption_data:
#             cm_serializer = ConsumptionMaterialCreateSerializer(
#                 data=cm_data,
#                 context={'factory_code_id': factory_code.id}
#             )
#             if cm_serializer.is_valid():
#                 cm_serializer.save()
        
#         # Step 4: Artwork Materials
#         artwork_data = validated_data.get('artworkMaterials', [])
#         for am_data in artwork_data:
#             am_serializer = ArtworkMaterialCreateSerializer(
#                 data=am_data,
#                 context={'factory_code_id': factory_code.id}
#             )
#             if am_serializer.is_valid():
#                 am_serializer.save()
        
#         # Step 5: Packaging
#         packaging_data = validated_data.get('packaging')
#         if packaging_data:
#             pkg_serializer = PackagingCreateSerializer(
#                 data=packaging_data,
#                 context={'factory_code_id': factory_code.id}
#             )
#             if pkg_serializer.is_valid():
#                 pkg_serializer.save()
        
#         return factory_code

from rest_framework import serializers
import re
from .models import (
    Department, Segment, BuyerCode, VendorCode,
    InternalPurchaseOrder, PurchaseOrder, CompanyEssential
)


class SegmentSerializer(serializers.ModelSerializer):
    """Serializer for Segment model"""
    
    class Meta:
        model = Segment
        fields = [
            'id', 'code', 'name', 'description', 'department', 
            'display_order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_code(self, value):
        """Validate segment code"""
        if not value:
            raise serializers.ValidationError("Segment code is required")
        return value.lower().strip()


class SegmentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Segment with department info"""
    
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    
    class Meta:
        model = Segment
        fields = [
            'id', 'code', 'name', 'description', 'department', 
            'department_name', 'department_code',
            'display_order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'department_name', 'department_code']


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""
    
    segments = SegmentSerializer(many=True, read_only=True)
    segments_count = serializers.IntegerField(source='segments.count', read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id', 'code', 'name', 'description', 'display_order', 
            'is_active', 'tenant', 'segments', 'segments_count',
            'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'segments_count']
    
    def validate_code(self, value):
        """Validate department code"""
        if not value:
            raise serializers.ValidationError("Department code is required")
        return value.lower().strip()


class DepartmentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for department list"""
    
    segments_count = serializers.IntegerField(source='segments.count', read_only=True)
    active_segments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = [
            'id', 'code', 'name', 'description', 'display_order', 
            'is_active', 'segments_count', 'active_segments_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_active_segments_count(self, obj):
        """Get count of active segments"""
        return obj.segments.filter(is_active=True).count()


class DepartmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating department with initial segments"""
    
    segments = SegmentSerializer(many=True, required=False)
    
    class Meta:
        model = Department
        fields = [
            'id', 'code', 'name', 'description', 'display_order', 
            'is_active', 'tenant', 'segments', 'created_by'
        ]
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Create department and associated segments"""
        segments_data = validated_data.pop('segments', [])
        department = Department.objects.create(**validated_data)
        
        for segment_data in segments_data:
            Segment.objects.create(department=department, **segment_data)
        
        return department


class BuyerCodeSerializer(serializers.ModelSerializer):
    """Serializer for BuyerCode model"""
    
    class Meta:
        model = BuyerCode
        fields = [
            'id', 'code', 'buyer_name', 'buyer_address', 'contact_person',
            'retailer', 'tenant', 'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']
    
    def validate_buyer_name(self, value):
        """Validate buyer name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Buyer name is required")
        return value.strip()
    
    def validate_buyer_address(self, value):
        """Validate buyer address"""
        if not value or not value.strip():
            raise serializers.ValidationError("Buyer address is required")
        return value.strip()
    
    def validate_contact_person(self, value):
        """Validate contact person"""
        if not value or not value.strip():
            raise serializers.ValidationError("Contact person is required")
        return value.strip()
    
    def validate_retailer(self, value):
        """Validate retailer"""
        if not value or not value.strip():
            raise serializers.ValidationError("Retailer is required")
        return value.strip()


class BuyerCodeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating buyer code (code is auto-generated)"""
    
    class Meta:
        model = BuyerCode
        fields = [
            'id', 'code', 'buyer_name', 'buyer_address', 'contact_person',
            'retailer', 'tenant'
        ]
        read_only_fields = ['id', 'code']
    
    def validate_buyer_name(self, value):
        """Validate buyer name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Buyer name is required")
        return value.strip()
    
    def validate_buyer_address(self, value):
        """Validate buyer address"""
        if not value or not value.strip():
            raise serializers.ValidationError("Buyer address is required")
        return value.strip()
    
    def validate_contact_person(self, value):
        """Validate contact person"""
        if not value or not value.strip():
            raise serializers.ValidationError("Contact person is required")
        return value.strip()
    
    def validate_retailer(self, value):
        """Validate retailer"""
        if not value or not value.strip():
            raise serializers.ValidationError("Retailer is required")
        return value.strip()
    
    def create(self, validated_data):
        """Create buyer code with auto-generated code"""
        request = self.context.get('request')
        user = request.user if request else None
        
        # Get tenant from user if not provided
        if 'tenant' not in validated_data and user and user.tenant:
            validated_data['tenant'] = user.tenant
        
        # Create buyer code (code will be auto-generated in save method)
        buyer_code = BuyerCode.objects.create(
            **validated_data,
            created_by=user
        )
        
        return buyer_code


class BuyerCodeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for buyer code list"""
    
    class Meta:
        model = BuyerCode
        fields = [
            'id', 'code', 'buyer_name', 'retailer', 'contact_person',
            'created_at'
        ]
        read_only_fields = ['id', 'code', 'created_at']


class VendorCodeSerializer(serializers.ModelSerializer):
    """Serializer for VendorCode model"""
    
    class Meta:
        model = VendorCode
        fields = [
            'id', 'code', 'vendor_name', 'address', 'gst', 'bank_name',
            'account_number', 'ifsc_code', 'job_work_category', 'job_work_sub_category',
            'contact_person', 'whatsapp_number', 'alt_whatsapp_number', 'email',
            'payment_terms', 'tenant', 'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']
    
    def validate_gst(self, value):
        """Validate GST number format"""
        if not value:
            raise serializers.ValidationError("GST number is required")
        # GST format: 22AAAAA0000A1Z5 (15 characters)
        gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        if not re.match(gst_pattern, value.upper()):
            raise serializers.ValidationError("Please enter a valid GST number (e.g., 22AAAAA0000A1Z5)")
        return value.upper()
    
    def validate_ifsc_code(self, value):
        """Validate IFSC code format"""
        if not value:
            raise serializers.ValidationError("IFSC code is required")
        # IFSC format: AAAA0XXXXX (11 characters)
        ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
        if not re.match(ifsc_pattern, value.upper()):
            raise serializers.ValidationError("Please enter a valid IFSC code (e.g., SBIN0000123)")
        return value.upper()
    
    def validate_whatsapp_number(self, value):
        """Validate WhatsApp number format"""
        if not value:
            raise serializers.ValidationError("WhatsApp number is required")
        # Remove spaces and check if it's 10 digits
        cleaned = value.replace(' ', '').replace('-', '')
        if not cleaned.isdigit() or len(cleaned) != 10:
            raise serializers.ValidationError("Please enter a valid 10-digit WhatsApp number")
        return cleaned
    
    def validate_alt_whatsapp_number(self, value):
        """Validate alternative WhatsApp number format (optional)"""
        if value:
            cleaned = value.replace(' ', '').replace('-', '')
            if not cleaned.isdigit() or len(cleaned) != 10:
                raise serializers.ValidationError("Please enter a valid 10-digit WhatsApp number")
            return cleaned
        return value
    
    def validate_email(self, value):
        """Validate email format"""
        if not value:
            raise serializers.ValidationError("Email is required")
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Please enter a valid email address")
        return value.lower()
    
    def validate_vendor_name(self, value):
        """Validate vendor name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Vendor name is required")
        return value.strip()
    
    def validate_address(self, value):
        """Validate address"""
        if not value or not value.strip():
            raise serializers.ValidationError("Address is required")
        return value.strip()
    
    def validate_contact_person(self, value):
        """Validate contact person"""
        if not value or not value.strip():
            raise serializers.ValidationError("Contact person is required")
        return value.strip()
    
    def validate_bank_name(self, value):
        """Validate bank name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Bank name is required")
        return value.strip()
    
    def validate_account_number(self, value):
        """Validate account number"""
        if not value or not value.strip():
            raise serializers.ValidationError("Account number is required")
        return value.strip()
    
    def validate_job_work_category(self, value):
        """Validate job work category"""
        if not value or not value.strip():
            raise serializers.ValidationError("Job work category is required")
        return value.strip()
    
    def validate_job_work_sub_category(self, value):
        """Validate job work sub-category"""
        if not value or not value.strip():
            raise serializers.ValidationError("Job work sub-category is required")
        return value.strip()
    
    def validate_payment_terms(self, value):
        """Validate payment terms"""
        if not value or not value.strip():
            raise serializers.ValidationError("Payment terms is required")
        return value.strip()


class VendorCodeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating vendor code (code is auto-generated)"""
    
    class Meta:
        model = VendorCode
        fields = [
            'id', 'code', 'vendor_name', 'address', 'gst', 'bank_name',
            'account_number', 'ifsc_code', 'job_work_category', 'job_work_sub_category',
            'contact_person', 'whatsapp_number', 'alt_whatsapp_number', 'email',
            'payment_terms', 'tenant'
        ]
        read_only_fields = ['id', 'code']
    
    def validate_gst(self, value):
        """Validate GST number format"""
        if not value:
            raise serializers.ValidationError("GST number is required")
        gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        if not re.match(gst_pattern, value.upper()):
            raise serializers.ValidationError("Please enter a valid GST number (e.g., 22AAAAA0000A1Z5)")
        return value.upper()
    
    def validate_ifsc_code(self, value):
        """Validate IFSC code format"""
        if not value:
            raise serializers.ValidationError("IFSC code is required")
        ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
        if not re.match(ifsc_pattern, value.upper()):
            raise serializers.ValidationError("Please enter a valid IFSC code (e.g., SBIN0000123)")
        return value.upper()
    
    def validate_whatsapp_number(self, value):
        """Validate WhatsApp number format"""
        if not value:
            raise serializers.ValidationError("WhatsApp number is required")
        cleaned = value.replace(' ', '').replace('-', '')
        if not cleaned.isdigit() or len(cleaned) != 10:
            raise serializers.ValidationError("Please enter a valid 10-digit WhatsApp number")
        return cleaned
    
    def validate_alt_whatsapp_number(self, value):
        """Validate alternative WhatsApp number format (optional)"""
        if value:
            cleaned = value.replace(' ', '').replace('-', '')
            if not cleaned.isdigit() or len(cleaned) != 10:
                raise serializers.ValidationError("Please enter a valid 10-digit WhatsApp number")
            return cleaned
        return value
    
    def validate_email(self, value):
        """Validate email format"""
        if not value:
            raise serializers.ValidationError("Email is required")
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Please enter a valid email address")
        return value.lower()
    
    def validate_vendor_name(self, value):
        """Validate vendor name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Vendor name is required")
        return value.strip()
    
    def validate_address(self, value):
        """Validate address"""
        if not value or not value.strip():
            raise serializers.ValidationError("Address is required")
        return value.strip()
    
    def validate_contact_person(self, value):
        """Validate contact person"""
        if not value or not value.strip():
            raise serializers.ValidationError("Contact person is required")
        return value.strip()
    
    def validate_bank_name(self, value):
        """Validate bank name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Bank name is required")
        return value.strip()
    
    def validate_account_number(self, value):
        """Validate account number"""
        if not value or not value.strip():
            raise serializers.ValidationError("Account number is required")
        return value.strip()
    
    def validate_job_work_category(self, value):
        """Validate job work category"""
        if not value or not value.strip():
            raise serializers.ValidationError("Job work category is required")
        return value.strip()
    
    def validate_job_work_sub_category(self, value):
        """Validate job work sub-category"""
        if not value or not value.strip():
            raise serializers.ValidationError("Job work sub-category is required")
        return value.strip()
    
    def validate_payment_terms(self, value):
        """Validate payment terms"""
        if not value or not value.strip():
            raise serializers.ValidationError("Payment terms is required")
        return value.strip()
    
    def create(self, validated_data):
        """Create vendor code with auto-generated code"""
        request = self.context.get('request')
        user = request.user if request else None
        
        # Get tenant from user if not provided
        if 'tenant' not in validated_data and user and user.tenant:
            validated_data['tenant'] = user.tenant
        
        # Create vendor code (code will be auto-generated in save method)
        vendor_code = VendorCode.objects.create(
            **validated_data,
            created_by=user
        )
        
        return vendor_code


class VendorCodeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for vendor code list"""
    
    class Meta:
        model = VendorCode
        fields = [
            'id', 'code', 'vendor_name', 'gst', 'job_work_category',
            'contact_person', 'email', 'created_at'
        ]
        read_only_fields = ['id', 'code', 'created_at']


"""
Factory Code Serializers - V2
==============================

Comprehensive DRF serializers for the 6-step Factory Code wizard.
Handles flattened frontend fields → nested JSONField conversion.

Key Design Patterns:
- CreateSerializers: Accept flattened frontend fields, transform to model structure
- ReadSerializers: Return nested JSON for frontend consumption
- Validation: Category-specific field validation
- File handling: Base64 or multipart file uploads
"""

from rest_framework import serializers
from django.db import transaction
from .models import (
    FactoryCode, Product, Component, RawMaterial, WorkOrder,
    ConsumptionMaterial, ArtworkMaterial, Packaging, PackagingMaterial,
    TrimAccessoryChoices, ArtworkCategoryChoices, PackagingMaterialTypeChoices,
    WorkOrderTypeChoices, UnitChoices, SizeUnitChoices,
    ApprovalChoices, ApprovalAgainstChoices,
    TRIM_CATEGORY_FIELDS_SCHEMA, ARTWORK_CATEGORY_FIELDS_SCHEMA,
    PACKAGING_MATERIAL_FIELDS_SCHEMA
)


# =============================================================================
# UTILITY SERIALIZERS
# =============================================================================

class SizeSerializer(serializers.Serializer):
    """Nested size object serializer"""
    width = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    length = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    height = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    unit = serializers.ChoiceField(choices=SizeUnitChoices.choices, required=False, allow_null=True)


class ChoiceListSerializer(serializers.Serializer):
    """Generic serializer for choice list endpoints"""
    value = serializers.CharField()
    label = serializers.CharField()


# =============================================================================
# STEP 0: FACTORY CODE (Product Identification)
# =============================================================================

# class FactoryCodeSerializer(serializers.ModelSerializer):
#     """Read serializer for FactoryCode"""
    
#     class Meta:
#         model = FactoryCode
#         fields = [
#             'id', 'code', 'type', 'buyer', 'style_no', 'style_name',
#             'size', 'gsm', 'article_description', 'colour',
#             'reference_image', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'code', 'created_at', 'updated_at']


# class FactoryCodeCreateSerializer(serializers.ModelSerializer):
#     """Create serializer for FactoryCode - maps frontend step0 fields"""
    
#     class Meta:
#         model = FactoryCode
#         fields = [
#             'type', 'buyer', 'style_no', 'style_name',
#             'size', 'gsm', 'article_description', 'colour',
#             'reference_image'
#         ]
    
#     def create(self, validated_data):
#         validated_data['tenant'] = self.context['request'].user.tenant
#         validated_data['created_by'] = self.context['request'].user
#         return super().create(validated_data)

class FactoryCodeSerializer(serializers.ModelSerializer):
    """Read serializer for FactoryCode"""
    buyer_code_details = BuyerCodeSerializer(source='buyer_code', read_only=True)
    
    class Meta:
        model = FactoryCode
        fields = [
            'id', 'code', 'sku', 'product_name', 'buyer_code', 'buyer_code_details',
            'status', 'is_active', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']


class FactoryCodeCreateSerializer(serializers.ModelSerializer):
    """Create serializer for FactoryCode"""
    
    class Meta:
        model = FactoryCode
        fields = [
            'sku', 'product_name', 'buyer_code', 'notes'
        ]
    
    def create(self, validated_data):
        validated_data['tenant'] = self.context['request'].user.tenant
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

# =============================================================================
# STEP 1: CUT & SEW (Product + Components)
# =============================================================================

class ComponentSerializer(serializers.ModelSerializer):
    """Read serializer for Component"""
    size = SizeSerializer(source='*', read_only=True)
    
    class Meta:
        model = Component
        fields = [
            'id', 'name', 'placement', 'remarks', 'surplus',
            'size', 'unit', 'quantity'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Nest size fields
        data['size'] = {
            'width': instance.size_width,
            'length': instance.size_length,
            'height': instance.size_height,
            'unit': instance.size_unit
        }
        return data


class ComponentCreateSerializer(serializers.ModelSerializer):
    """Create serializer for Component - accepts flattened size fields"""
    # Flattened size fields from frontend
    sizeWidth = serializers.CharField(required=False, allow_blank=True, source='size_width')
    sizeLength = serializers.CharField(required=False, allow_blank=True, source='size_length')
    sizeHeight = serializers.CharField(required=False, allow_blank=True, source='size_height')
    sizeUnit = serializers.ChoiceField(
        choices=SizeUnitChoices.choices, 
        required=False, 
        allow_null=True,
        source='size_unit'
    )
    
    class Meta:
        model = Component
        fields = [
            'name', 'placement', 'remarks', 'surplus',
            'sizeWidth', 'sizeLength', 'sizeHeight', 'sizeUnit',
            'unit', 'quantity'
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Read serializer for Product with nested components"""
    components = ComponentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'placement', 'components']


class ProductCreateSerializer(serializers.ModelSerializer):
    """Create serializer for Product with nested component creation"""
    components = ComponentCreateSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = ['name', 'placement', 'components']
    
    def create(self, validated_data):
        components_data = validated_data.pop('components', [])
        product = Product.objects.create(**validated_data)
        for comp_data in components_data:
            Component.objects.create(product=product, **comp_data)
        return product


# =============================================================================
# STEP 2: RAW MATERIALS & WORK ORDERS
# =============================================================================

class WorkOrderSerializer(serializers.ModelSerializer):
    """Read serializer for WorkOrder with process-specific data"""
    process_specific_data = serializers.JSONField(read_only=True)
    
    class Meta:
        model = WorkOrder
        fields = [
            'id', 'process_type', 'process_note', 'process_specific_data'
        ]


class WorkOrderCreateSerializer(serializers.Serializer):
    """
    Create serializer for WorkOrder - handles conditional process fields
    
    Frontend sends flat fields like: reed, pick, warp, weft (for WEAVING)
    We pack them into process_specific_data JSONField
    """
    process_type = serializers.ChoiceField(choices=WorkOrderTypeChoices.choices)
    process_note = serializers.CharField(required=False, allow_blank=True)
    
    # WEAVING fields
    reed = serializers.CharField(required=False, allow_blank=True)
    pick = serializers.CharField(required=False, allow_blank=True)
    warp = serializers.CharField(required=False, allow_blank=True)
    weft = serializers.CharField(required=False, allow_blank=True)
    
    # KNITTING fields
    wales = serializers.CharField(required=False, allow_blank=True)
    courses = serializers.CharField(required=False, allow_blank=True)
    
    # DYEING fields
    shrinkageWidth = serializers.CharField(required=False, allow_blank=True)
    shrinkageLength = serializers.CharField(required=False, allow_blank=True)
    processRoute = serializers.CharField(required=False, allow_blank=True)
    
    # TUFTING fields
    tuftGauge = serializers.CharField(required=False, allow_blank=True)
    stitchRate = serializers.CharField(required=False, allow_blank=True)
    pileHeight = serializers.CharField(required=False, allow_blank=True)
    primaryBacking = serializers.CharField(required=False, allow_blank=True)
    secondaryBacking = serializers.CharField(required=False, allow_blank=True)
    
    # CUTTING fields
    cuttingPattern = serializers.CharField(required=False, allow_blank=True)
    cuttingMethod = serializers.CharField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        process_type = validated_data.get('process_type')
        process_note = validated_data.get('process_note', '')
        
        # Build process_specific_data based on process_type
        process_specific_data = {}
        
        if process_type == 'WEAVING':
            process_specific_data = {
                'reed': validated_data.get('reed', ''),
                'pick': validated_data.get('pick', ''),
                'warp': validated_data.get('warp', ''),
                'weft': validated_data.get('weft', '')
            }
        elif process_type == 'KNITTING':
            process_specific_data = {
                'wales': validated_data.get('wales', ''),
                'courses': validated_data.get('courses', '')
            }
        elif process_type == 'DYEING':
            process_specific_data = {
                'shrinkageWidth': validated_data.get('shrinkageWidth', ''),
                'shrinkageLength': validated_data.get('shrinkageLength', ''),
                'processRoute': validated_data.get('processRoute', '')
            }
        elif process_type == 'TUFTING':
            process_specific_data = {
                'tuftGauge': validated_data.get('tuftGauge', ''),
                'stitchRate': validated_data.get('stitchRate', ''),
                'pileHeight': validated_data.get('pileHeight', ''),
                'primaryBacking': validated_data.get('primaryBacking', ''),
                'secondaryBacking': validated_data.get('secondaryBacking', '')
            }
        elif process_type == 'CUTTING':
            process_specific_data = {
                'cuttingPattern': validated_data.get('cuttingPattern', ''),
                'cuttingMethod': validated_data.get('cuttingMethod', '')
            }
        
        return {
            'process_type': process_type,
            'process_note': process_note,
            'process_specific_data': process_specific_data
        }


class RawMaterialSerializer(serializers.ModelSerializer):
    """Read serializer for RawMaterial with nested work orders"""
    work_orders = WorkOrderSerializer(many=True, read_only=True)
    size = serializers.SerializerMethodField()
    
    class Meta:
        model = RawMaterial
        fields = [
            'id', 'component', 'material_name', 'composition',
            'construction', 'colour', 'gsm', 'finish', 'thread_count',
            'size', 'consumption', 'consumption_unit', 'surplus',
            'rate', 'rate_unit', 'approval', 'approval_against',
            'remarks', 'work_orders'
        ]
    
    def get_size(self, obj):
        return {
            'width': obj.size_width,
            'length': obj.size_length,
            'height': obj.size_height,
            'unit': obj.size_unit
        }


class RawMaterialCreateSerializer(serializers.Serializer):
    """
    Create serializer for RawMaterial with nested work orders
    Accepts flattened frontend structure
    """
    component = serializers.UUIDField(required=False, allow_null=True)
    materialName = serializers.CharField(source='material_name')
    composition = serializers.CharField(required=False, allow_blank=True)
    construction = serializers.CharField(required=False, allow_blank=True)
    colour = serializers.CharField(required=False, allow_blank=True)
    gsm = serializers.CharField(required=False, allow_blank=True)
    finish = serializers.CharField(required=False, allow_blank=True)
    threadCount = serializers.CharField(required=False, allow_blank=True, source='thread_count')
    
    # Size fields
    sizeWidth = serializers.CharField(required=False, allow_blank=True)
    sizeLength = serializers.CharField(required=False, allow_blank=True)
    sizeHeight = serializers.CharField(required=False, allow_blank=True)
    sizeUnit = serializers.ChoiceField(
        choices=SizeUnitChoices.choices, 
        required=False, 
        allow_null=True
    )
    
    # Consumption
    consumption = serializers.CharField(required=False, allow_blank=True)
    consumptionUnit = serializers.ChoiceField(
        choices=UnitChoices.choices,
        required=False,
        allow_null=True,
        source='consumption_unit'
    )
    surplus = serializers.CharField(required=False, allow_blank=True)
    
    # Rate
    rate = serializers.CharField(required=False, allow_blank=True)
    rateUnit = serializers.ChoiceField(
        choices=UnitChoices.choices,
        required=False,
        allow_null=True,
        source='rate_unit'
    )
    
    # Approval
    approval = serializers.ChoiceField(
        choices=ApprovalChoices.choices,
        required=False,
        allow_null=True
    )
    approvalAgainst = serializers.ChoiceField(
        choices=ApprovalAgainstChoices.choices,
        required=False,
        allow_null=True,
        source='approval_against'
    )
    remarks = serializers.CharField(required=False, allow_blank=True)
    
    # Nested work orders
    workOrders = WorkOrderCreateSerializer(many=True, required=False)
    
    def create(self, validated_data):
        work_orders_data = validated_data.pop('workOrders', [])
        
        # Map size fields
        raw_material_data = {
            'material_name': validated_data.get('material_name', ''),
            'composition': validated_data.get('composition', ''),
            'construction': validated_data.get('construction', ''),
            'colour': validated_data.get('colour', ''),
            'gsm': validated_data.get('gsm', ''),
            'finish': validated_data.get('finish', ''),
            'thread_count': validated_data.get('thread_count', ''),
            'size_width': validated_data.get('sizeWidth', ''),
            'size_length': validated_data.get('sizeLength', ''),
            'size_height': validated_data.get('sizeHeight', ''),
            'size_unit': validated_data.get('sizeUnit'),
            'consumption': validated_data.get('consumption', ''),
            'consumption_unit': validated_data.get('consumption_unit'),
            'surplus': validated_data.get('surplus', ''),
            'rate': validated_data.get('rate', ''),
            'rate_unit': validated_data.get('rate_unit'),
            'approval': validated_data.get('approval'),
            'approval_against': validated_data.get('approval_against'),
            'remarks': validated_data.get('remarks', ''),
        }
        
        if validated_data.get('component'):
            raw_material_data['component_id'] = validated_data['component']
        
        raw_material = RawMaterial.objects.create(**raw_material_data)
        
        # Create work orders
        for wo_data in work_orders_data:
            wo_serializer = WorkOrderCreateSerializer(data=wo_data)
            if wo_serializer.is_valid():
                wo_result = wo_serializer.save()
                WorkOrder.objects.create(
                    raw_material=raw_material,
                    process_type=wo_result['process_type'],
                    process_note=wo_result['process_note'],
                    process_specific_data=wo_result['process_specific_data']
                )
        
        return raw_material


# =============================================================================
# STEP 3: CONSUMPTION MATERIALS (Trims & Accessories) - 30 Categories
# =============================================================================

class ConsumptionMaterialSerializer(serializers.ModelSerializer):
    """Read serializer for ConsumptionMaterial"""
    size = serializers.SerializerMethodField()
    category_specific_data = serializers.JSONField(read_only=True)
    
    class Meta:
        model = ConsumptionMaterial
        fields = [
            'id', 'factory_code', 'category', 'size',
            'testing_requirement', 'testing_requirement_file',
            'length_quantity', 'surplus', 'surplus_for_section',
            'approval', 'remarks', 'unit_additional',
            'category_specific_data', 'created_at'
        ]
    
    def get_size(self, obj):
        return {
            'width': obj.size_width,
            'length': obj.size_length,
            'height': obj.size_height,
            'unit': obj.size_unit
        }


class ConsumptionMaterialCreateSerializer(serializers.Serializer):
    """
    Create serializer for ConsumptionMaterial - handles all 30 trim categories
    
    Frontend sends flat fields for the selected category.
    We validate and pack category-specific fields into category_specific_data JSONField.
    """
    
    # Required field
    category = serializers.ChoiceField(choices=TrimAccessoryChoices.choices)
    
    # Common fields across all categories
    testingRequirement = serializers.CharField(required=False, allow_blank=True)
    testingRequirementFile = serializers.FileField(required=False, allow_null=True)
    lengthQuantity = serializers.CharField(required=False, allow_blank=True)
    surplus = serializers.CharField(required=False, allow_blank=True)
    surplusForSection = serializers.CharField(required=False, allow_blank=True)
    approval = serializers.ChoiceField(
        choices=ApprovalChoices.choices,
        required=False,
        allow_null=True
    )
    remarks = serializers.CharField(required=False, allow_blank=True)
    unitAdditional = serializers.CharField(required=False, allow_blank=True)
    
    # Size fields
    sizeWidth = serializers.CharField(required=False, allow_blank=True)
    sizeLength = serializers.CharField(required=False, allow_blank=True)
    sizeHeight = serializers.CharField(required=False, allow_blank=True)
    sizeUnit = serializers.ChoiceField(
        choices=SizeUnitChoices.choices,
        required=False,
        allow_null=True
    )
    
    # =========================================================================
    # CATEGORY-SPECIFIC FIELDS (30 categories)
    # =========================================================================
    
    # --- ZIPPERS ---
    zipNumber = serializers.CharField(required=False, allow_blank=True)
    zipType = serializers.CharField(required=False, allow_blank=True)
    zipMaterial = serializers.CharField(required=False, allow_blank=True)
    sliderType = serializers.CharField(required=False, allow_blank=True)
    zipColour = serializers.CharField(required=False, allow_blank=True)
    tapeColour = serializers.CharField(required=False, allow_blank=True)
    endType = serializers.CharField(required=False, allow_blank=True)
    
    # --- VELCRO ---
    velcroType = serializers.CharField(required=False, allow_blank=True)
    velcroMaterial = serializers.CharField(required=False, allow_blank=True)
    velcroWidth = serializers.CharField(required=False, allow_blank=True)
    velcroColour = serializers.CharField(required=False, allow_blank=True)
    adhesiveBacked = serializers.BooleanField(required=False, allow_null=True)
    hooksLoops = serializers.CharField(required=False, allow_blank=True)
    
    # --- STITCHING THREAD ---
    threadType = serializers.CharField(required=False, allow_blank=True)
    threadMaterial = serializers.CharField(required=False, allow_blank=True)
    threadCount = serializers.CharField(required=False, allow_blank=True)
    threadColour = serializers.CharField(required=False, allow_blank=True)
    strengthTenacity = serializers.CharField(required=False, allow_blank=True)
    finish = serializers.CharField(required=False, allow_blank=True)
    
    # --- BUTTONS ---
    buttonType = serializers.CharField(required=False, allow_blank=True)
    buttonMaterial = serializers.CharField(required=False, allow_blank=True)
    buttonSize = serializers.CharField(required=False, allow_blank=True)
    buttonColour = serializers.CharField(required=False, allow_blank=True)
    numberOfHoles = serializers.CharField(required=False, allow_blank=True)
    buttonFinish = serializers.CharField(required=False, allow_blank=True)
    logo = serializers.CharField(required=False, allow_blank=True)
    
    # --- RIVETS ---
    rivetType = serializers.CharField(required=False, allow_blank=True)
    rivetMaterial = serializers.CharField(required=False, allow_blank=True)
    rivetSize = serializers.CharField(required=False, allow_blank=True)
    rivetColour = serializers.CharField(required=False, allow_blank=True)
    rivetFinish = serializers.CharField(required=False, allow_blank=True)
    capDesign = serializers.CharField(required=False, allow_blank=True)
    
    # --- NIWAR (Webbing/Tapes) ---
    niwarType = serializers.CharField(required=False, allow_blank=True)
    niwarMaterial = serializers.CharField(required=False, allow_blank=True)
    niwarWidth = serializers.CharField(required=False, allow_blank=True)
    niwarColour = serializers.CharField(required=False, allow_blank=True)
    pattern = serializers.CharField(required=False, allow_blank=True)
    tensileStrength = serializers.CharField(required=False, allow_blank=True)
    
    # --- LACE ---
    laceType = serializers.CharField(required=False, allow_blank=True)
    laceMaterial = serializers.CharField(required=False, allow_blank=True)
    laceWidth = serializers.CharField(required=False, allow_blank=True)
    laceColour = serializers.CharField(required=False, allow_blank=True)
    lacePattern = serializers.CharField(required=False, allow_blank=True)
    edgeFinish = serializers.CharField(required=False, allow_blank=True)
    
    # --- INTERLINING/FUSING ---
    interliningType = serializers.CharField(required=False, allow_blank=True)
    interliningMaterial = serializers.CharField(required=False, allow_blank=True)
    weight = serializers.CharField(required=False, allow_blank=True)
    interliningColour = serializers.CharField(required=False, allow_blank=True)
    adhesiveType = serializers.CharField(required=False, allow_blank=True)
    fusingTemperature = serializers.CharField(required=False, allow_blank=True)
    
    # --- HOOKS & EYES ---
    hookEyeType = serializers.CharField(required=False, allow_blank=True)
    hookEyeMaterial = serializers.CharField(required=False, allow_blank=True)
    hookEyeSize = serializers.CharField(required=False, allow_blank=True)
    hookEyeColour = serializers.CharField(required=False, allow_blank=True)
    hookEyeFinish = serializers.CharField(required=False, allow_blank=True)
    closureStrength = serializers.CharField(required=False, allow_blank=True)
    
    # --- BUCKLES & ADJUSTERS ---
    buckleType = serializers.CharField(required=False, allow_blank=True)
    buckleMaterial = serializers.CharField(required=False, allow_blank=True)
    buckleSize = serializers.CharField(required=False, allow_blank=True)
    buckleColour = serializers.CharField(required=False, allow_blank=True)
    buckleFinish = serializers.CharField(required=False, allow_blank=True)
    strapWidth = serializers.CharField(required=False, allow_blank=True)
    
    # --- EYELETS & GROMMETS ---
    eyeletType = serializers.CharField(required=False, allow_blank=True)
    eyeletMaterial = serializers.CharField(required=False, allow_blank=True)
    innerDiameter = serializers.CharField(required=False, allow_blank=True)
    outerDiameter = serializers.CharField(required=False, allow_blank=True)
    eyeletColour = serializers.CharField(required=False, allow_blank=True)
    eyeletFinish = serializers.CharField(required=False, allow_blank=True)
    
    # --- ELASTIC ---
    elasticType = serializers.CharField(required=False, allow_blank=True)
    elasticMaterial = serializers.CharField(required=False, allow_blank=True)
    elasticWidth = serializers.CharField(required=False, allow_blank=True)
    elasticColour = serializers.CharField(required=False, allow_blank=True)
    stretchPercent = serializers.CharField(required=False, allow_blank=True)
    elasticFinish = serializers.CharField(required=False, allow_blank=True)
    
    # --- FELT ---
    feltType = serializers.CharField(required=False, allow_blank=True)
    feltMaterial = serializers.CharField(required=False, allow_blank=True)
    feltThickness = serializers.CharField(required=False, allow_blank=True)
    feltColour = serializers.CharField(required=False, allow_blank=True)
    feltDensity = serializers.CharField(required=False, allow_blank=True)
    feltFinish = serializers.CharField(required=False, allow_blank=True)
    
    # --- SHOULDER PADS ---
    padType = serializers.CharField(required=False, allow_blank=True)
    padMaterial = serializers.CharField(required=False, allow_blank=True)
    padSize = serializers.CharField(required=False, allow_blank=True)
    padThickness = serializers.CharField(required=False, allow_blank=True)
    padColour = serializers.CharField(required=False, allow_blank=True)
    padShape = serializers.CharField(required=False, allow_blank=True)
    covering = serializers.CharField(required=False, allow_blank=True)
    
    # --- TUBULAR KNITS / RIBBING ---
    tubularType = serializers.CharField(required=False, allow_blank=True)
    tubularMaterial = serializers.CharField(required=False, allow_blank=True)
    widthDiameter = serializers.CharField(required=False, allow_blank=True)
    weightDensity = serializers.CharField(required=False, allow_blank=True)
    tubularColour = serializers.CharField(required=False, allow_blank=True)
    # stretchPercent shared with ELASTIC
    cutting = serializers.CharField(required=False, allow_blank=True)
    
    # --- RFID / EAS TAGS ---
    rfidType = serializers.CharField(required=False, allow_blank=True)
    formFactor = serializers.CharField(required=False, allow_blank=True)
    frequency = serializers.CharField(required=False, allow_blank=True)
    chipIcType = serializers.CharField(required=False, allow_blank=True)
    rfidSize = serializers.CharField(required=False, allow_blank=True)
    coding = serializers.CharField(required=False, allow_blank=True)
    security = serializers.CharField(required=False, allow_blank=True)
    
    # --- PLASTIC CABLE TIES / LOOPS ---
    cableTieType = serializers.CharField(required=False, allow_blank=True)
    cableTieMaterial = serializers.CharField(required=False, allow_blank=True)
    cableTieSize = serializers.CharField(required=False, allow_blank=True)
    cableTieColour = serializers.CharField(required=False, allow_blank=True)
    cableTieTensileStrength = serializers.CharField(required=False, allow_blank=True)
    cableTieFinish = serializers.CharField(required=False, allow_blank=True)
    cableTieUsage = serializers.CharField(required=False, allow_blank=True)
    
    # --- FRINGE / TASSELS ---
    fringeType = serializers.CharField(required=False, allow_blank=True)
    fringeMaterial = serializers.CharField(required=False, allow_blank=True)
    dropLength = serializers.CharField(required=False, allow_blank=True)
    fringeTapeWidth = serializers.CharField(required=False, allow_blank=True)
    fringeColour = serializers.CharField(required=False, allow_blank=True)
    fringeFinish = serializers.CharField(required=False, allow_blank=True)
    construction = serializers.CharField(required=False, allow_blank=True)
    
    # --- PLASTIC PIPES / RODS ---
    pipeType = serializers.CharField(required=False, allow_blank=True)
    pipeMaterial = serializers.CharField(required=False, allow_blank=True)
    diameterDimensions = serializers.CharField(required=False, allow_blank=True)
    pipeLength = serializers.CharField(required=False, allow_blank=True)
    pipeColour = serializers.CharField(required=False, allow_blank=True)
    endCaps = serializers.CharField(required=False, allow_blank=True)
    flexibility = serializers.CharField(required=False, allow_blank=True)
    pipeUsage = serializers.CharField(required=False, allow_blank=True)
    
    # --- SEAM SEALING TAPE ---
    seamTapeType = serializers.CharField(required=False, allow_blank=True)
    seamTapeMaterial = serializers.CharField(required=False, allow_blank=True)
    seamTapeWidth = serializers.CharField(required=False, allow_blank=True)
    seamTapeColour = serializers.CharField(required=False, allow_blank=True)
    seamTapeAdhesiveType = serializers.CharField(required=False, allow_blank=True)
    applicationSpec = serializers.CharField(required=False, allow_blank=True)
    elasticity = serializers.CharField(required=False, allow_blank=True)
    
    # --- ADHESIVES / GUNNING ---
    adhesiveGunType = serializers.CharField(required=False, allow_blank=True)
    materialBase = serializers.CharField(required=False, allow_blank=True)
    adhesiveApplication = serializers.CharField(required=False, allow_blank=True)
    viscosity = serializers.CharField(required=False, allow_blank=True)
    settingTime = serializers.CharField(required=False, allow_blank=True)
    adhesiveColour = serializers.CharField(required=False, allow_blank=True)
    applicator = serializers.CharField(required=False, allow_blank=True)
    
    # --- PRE-CUT HEMS / BINDINGS ---
    hemType = serializers.CharField(required=False, allow_blank=True)
    hemMaterial = serializers.CharField(required=False, allow_blank=True)
    cutType = serializers.CharField(required=False, allow_blank=True)
    hemWidth = serializers.CharField(required=False, allow_blank=True)
    foldType = serializers.CharField(required=False, allow_blank=True)
    hemColour = serializers.CharField(required=False, allow_blank=True)
    hemPackaging = serializers.CharField(required=False, allow_blank=True)
    
    # --- REFLECTIVE TAPES / TRIMS ---
    reflectiveType = serializers.CharField(required=False, allow_blank=True)
    reflectiveMaterial = serializers.CharField(required=False, allow_blank=True)
    reflectiveWidth = serializers.CharField(required=False, allow_blank=True)
    reflectiveColour = serializers.CharField(required=False, allow_blank=True)
    certification = serializers.CharField(required=False, allow_blank=True)
    baseFabric = serializers.CharField(required=False, allow_blank=True)
    
    # --- FIRE RETARDANT (FR) TRIMS ---
    frType = serializers.CharField(required=False, allow_blank=True)
    frMaterial = serializers.CharField(required=False, allow_blank=True)
    complianceLevel = serializers.CharField(required=False, allow_blank=True)
    frColour = serializers.CharField(required=False, allow_blank=True)
    durability = serializers.CharField(required=False, allow_blank=True)
    frComponents = serializers.CharField(required=False, allow_blank=True)
    
    # --- REPAIR KITS / PATCHES ---
    repairKitType = serializers.CharField(required=False, allow_blank=True)
    repairKitMaterial = serializers.CharField(required=False, allow_blank=True)
    sizeShape = serializers.CharField(required=False, allow_blank=True)
    repairKitColour = serializers.CharField(required=False, allow_blank=True)
    repairKitPackaging = serializers.CharField(required=False, allow_blank=True)
    userApplication = serializers.CharField(required=False, allow_blank=True)
    contents = serializers.CharField(required=False, allow_blank=True)
    
    # --- CORD STOPS / CORD LOCKS / TOGGLES ---
    cordStopType = serializers.CharField(required=False, allow_blank=True)
    cordStopMaterial = serializers.CharField(required=False, allow_blank=True)
    cordStopSize = serializers.CharField(required=False, allow_blank=True)
    cordStopColour = serializers.CharField(required=False, allow_blank=True)
    lockingMechanism = serializers.CharField(required=False, allow_blank=True)
    cordStopFunction = serializers.CharField(required=False, allow_blank=True)
    
    # --- D-RINGS / O-RINGS / WEBBING LOOPS ---
    dRingType = serializers.CharField(required=False, allow_blank=True)
    dRingMaterial = serializers.CharField(required=False, allow_blank=True)
    dRingSize = serializers.CharField(required=False, allow_blank=True)
    thicknessGauge = serializers.CharField(required=False, allow_blank=True)
    dRingFinishPlating = serializers.CharField(required=False, allow_blank=True)
    loadRating = serializers.CharField(required=False, allow_blank=True)
    dRingApplication = serializers.CharField(required=False, allow_blank=True)
    
    # --- FOAM / WADDING (Pre-Cut Shapes) ---
    foamType = serializers.CharField(required=False, allow_blank=True)
    foamDensity = serializers.CharField(required=False, allow_blank=True)
    foamThickness = serializers.CharField(required=False, allow_blank=True)
    shapeId = serializers.CharField(required=False, allow_blank=True)
    foamColour = serializers.CharField(required=False, allow_blank=True)
    properties = serializers.CharField(required=False, allow_blank=True)
    foamAttachment = serializers.CharField(required=False, allow_blank=True)
    
    # --- PINS / TAGGING BARBS ---
    pinType = serializers.CharField(required=False, allow_blank=True)
    pinMaterial = serializers.CharField(required=False, allow_blank=True)
    pinSize = serializers.CharField(required=False, allow_blank=True)
    pinColour = serializers.CharField(required=False, allow_blank=True)
    pinTensileStrength = serializers.CharField(required=False, allow_blank=True)
    headType = serializers.CharField(required=False, allow_blank=True)
    pinApplication = serializers.CharField(required=False, allow_blank=True)
    
    # --- MAGNETIC CLOSURES / SNAPS ---
    magneticType = serializers.CharField(required=False, allow_blank=True)
    magneticMaterial = serializers.CharField(required=False, allow_blank=True)
    magneticSize = serializers.CharField(required=False, allow_blank=True)
    magneticStrength = serializers.CharField(required=False, allow_blank=True)
    polarity = serializers.CharField(required=False, allow_blank=True)
    magneticApplication = serializers.CharField(required=False, allow_blank=True)
    
    def _get_category_specific_fields(self, category, validated_data):
        """
        Extract category-specific fields based on the selected category.
        Returns a dict of the relevant fields for that category.
        """
        category_field_map = {
            'ZIPPERS': [
                'zipNumber', 'zipType', 'zipMaterial', 'sliderType',
                'zipColour', 'tapeColour', 'endType'
            ],
            'VELCRO': [
                'velcroType', 'velcroMaterial', 'velcroWidth', 'velcroColour',
                'adhesiveBacked', 'hooksLoops'
            ],
            'STITCHING THREAD': [
                'threadType', 'threadMaterial', 'threadCount', 'threadColour',
                'strengthTenacity', 'finish'
            ],
            'BUTTONS': [
                'buttonType', 'buttonMaterial', 'buttonSize', 'buttonColour',
                'numberOfHoles', 'buttonFinish', 'logo'
            ],
            'RIVETS': [
                'rivetType', 'rivetMaterial', 'rivetSize', 'rivetColour',
                'rivetFinish', 'capDesign'
            ],
            'NIWAR (Webbing/Tapes)': [
                'niwarType', 'niwarMaterial', 'niwarWidth', 'niwarColour',
                'pattern', 'tensileStrength'
            ],
            'LACE': [
                'laceType', 'laceMaterial', 'laceWidth', 'laceColour',
                'lacePattern', 'edgeFinish'
            ],
            'INTERLINING/FUSING': [
                'interliningType', 'interliningMaterial', 'weight', 'interliningColour',
                'adhesiveType', 'fusingTemperature'
            ],
            'HOOKS & EYES': [
                'hookEyeType', 'hookEyeMaterial', 'hookEyeSize', 'hookEyeColour',
                'hookEyeFinish', 'closureStrength'
            ],
            'BUCKLES & ADJUSTERS': [
                'buckleType', 'buckleMaterial', 'buckleSize', 'buckleColour',
                'buckleFinish', 'strapWidth'
            ],
            'EYELETS & GROMMETS': [
                'eyeletType', 'eyeletMaterial', 'innerDiameter', 'outerDiameter',
                'eyeletColour', 'eyeletFinish'
            ],
            'ELASTIC': [
                'elasticType', 'elasticMaterial', 'elasticWidth', 'elasticColour',
                'stretchPercent', 'elasticFinish'
            ],
            'FELT': [
                'feltType', 'feltMaterial', 'feltThickness', 'feltColour',
                'feltDensity', 'feltFinish'
            ],
            'SHOULDER PADS': [
                'padType', 'padMaterial', 'padSize', 'padThickness',
                'padColour', 'padShape', 'covering'
            ],
            'TUBULAR KNITS / RIBBING': [
                'tubularType', 'tubularMaterial', 'widthDiameter', 'weightDensity',
                'tubularColour', 'stretchPercent', 'cutting'
            ],
            'RFID / EAS TAGS': [
                'rfidType', 'formFactor', 'frequency', 'chipIcType',
                'rfidSize', 'coding', 'security'
            ],
            'PLASTIC CABLE TIES / LOOPS': [
                'cableTieType', 'cableTieMaterial', 'cableTieSize', 'cableTieColour',
                'cableTieTensileStrength', 'cableTieFinish', 'cableTieUsage'
            ],
            'FRINGE / TASSELS': [
                'fringeType', 'fringeMaterial', 'dropLength', 'fringeTapeWidth',
                'fringeColour', 'fringeFinish', 'construction'
            ],
            'PLASTIC PIPES / RODS': [
                'pipeType', 'pipeMaterial', 'diameterDimensions', 'pipeLength',
                'pipeColour', 'endCaps', 'flexibility', 'pipeUsage'
            ],
            'SEAM SEALING TAPE': [
                'seamTapeType', 'seamTapeMaterial', 'seamTapeWidth', 'seamTapeColour',
                'seamTapeAdhesiveType', 'applicationSpec', 'elasticity'
            ],
            'ADHESIVES / GUNNING': [
                'adhesiveGunType', 'materialBase', 'adhesiveApplication', 'viscosity',
                'settingTime', 'adhesiveColour', 'applicator'
            ],
            'PRE-CUT HEMS / BINDINGS': [
                'hemType', 'hemMaterial', 'cutType', 'hemWidth',
                'foldType', 'hemColour', 'hemPackaging'
            ],
            'REFLECTIVE TAPES / TRIMS': [
                'reflectiveType', 'reflectiveMaterial', 'reflectiveWidth', 'reflectiveColour',
                'certification', 'baseFabric'
            ],
            'FIRE RETARDANT (FR) TRIMS': [
                'frType', 'frMaterial', 'complianceLevel', 'frColour',
                'durability', 'frComponents'
            ],
            'REPAIR KITS / PATCHES': [
                'repairKitType', 'repairKitMaterial', 'sizeShape', 'repairKitColour',
                'repairKitPackaging', 'userApplication', 'contents'
            ],
            'CORD STOPS / CORD LOCKS / TOGGLES': [
                'cordStopType', 'cordStopMaterial', 'cordStopSize', 'cordStopColour',
                'lockingMechanism', 'cordStopFunction'
            ],
            'D-RINGS / O-RINGS / WEBBING LOOPS': [
                'dRingType', 'dRingMaterial', 'dRingSize', 'thicknessGauge',
                'dRingFinishPlating', 'loadRating', 'dRingApplication'
            ],
            'FOAM / WADDING (Pre-Cut Shapes)': [
                'foamType', 'foamDensity', 'foamThickness', 'shapeId',
                'foamColour', 'properties', 'foamAttachment'
            ],
            'PINS / TAGGING BARBS': [
                'pinType', 'pinMaterial', 'pinSize', 'pinColour',
                'pinTensileStrength', 'headType', 'pinApplication'
            ],
            'MAGNETIC CLOSURES / SNAPS': [
                'magneticType', 'magneticMaterial', 'magneticSize', 'magneticStrength',
                'polarity', 'magneticApplication'
            ]
        }
        
        fields = category_field_map.get(category, [])
        return {field: validated_data.get(field, '') for field in fields if field in validated_data}
    
    def create(self, validated_data):
        category = validated_data['category']
        
        # Extract category-specific fields
        category_specific_data = self._get_category_specific_fields(category, validated_data)
        
        # Build model data
        model_data = {
            'factory_code_id': self.context.get('factory_code_id'),
            'category': category,
            'testing_requirement': validated_data.get('testingRequirement', ''),
            'testing_requirement_file': validated_data.get('testingRequirementFile'),
            'length_quantity': validated_data.get('lengthQuantity', ''),
            'surplus': validated_data.get('surplus', ''),
            'surplus_for_section': validated_data.get('surplusForSection', ''),
            'approval': validated_data.get('approval'),
            'remarks': validated_data.get('remarks', ''),
            'unit_additional': validated_data.get('unitAdditional', ''),
            'size_width': validated_data.get('sizeWidth', ''),
            'size_length': validated_data.get('sizeLength', ''),
            'size_height': validated_data.get('sizeHeight', ''),
            'size_unit': validated_data.get('sizeUnit'),
            'category_specific_data': category_specific_data
        }
        
        return ConsumptionMaterial.objects.create(**model_data)


# =============================================================================
# STEP 4: ARTWORK MATERIALS - 18 Categories
# =============================================================================

class ArtworkMaterialSerializer(serializers.ModelSerializer):
    """Read serializer for ArtworkMaterial"""
    size = serializers.SerializerMethodField()
    category_specific_data = serializers.JSONField(read_only=True)
    
    class Meta:
        model = ArtworkMaterial
        fields = [
            'id', 'factory_code', 'category', 'size',
            'surplus', 'surplus_for_section', 'usage',
            'approval', 'remarks', 'reference_image',
            'category_specific_data', 'created_at'
        ]
    
    def get_size(self, obj):
        return {
            'width': obj.size_width,
            'length': obj.size_length,
            'height': obj.size_height,
            'unit': obj.size_unit
        }


class ArtworkMaterialCreateSerializer(serializers.Serializer):
    """
    Create serializer for ArtworkMaterial - handles all 18 artwork categories
    """
    
    # Required field
    category = serializers.ChoiceField(choices=ArtworkCategoryChoices.choices)
    
    # Common fields
    surplus = serializers.CharField(required=False, allow_blank=True)
    surplusForSection = serializers.CharField(required=False, allow_blank=True)
    usage = serializers.CharField(required=False, allow_blank=True)
    approval = serializers.ChoiceField(
        choices=ApprovalChoices.choices,
        required=False,
        allow_null=True
    )
    remarks = serializers.CharField(required=False, allow_blank=True)
    referenceImage = serializers.FileField(required=False, allow_null=True)
    
    # Size fields
    sizeWidth = serializers.CharField(required=False, allow_blank=True)
    sizeLength = serializers.CharField(required=False, allow_blank=True)
    sizeHeight = serializers.CharField(required=False, allow_blank=True)
    sizeUnit = serializers.ChoiceField(
        choices=SizeUnitChoices.choices,
        required=False,
        allow_null=True
    )
    
    # =========================================================================
    # CATEGORY-SPECIFIC FIELDS (18 categories)
    # =========================================================================
    
    # Common artwork fields used across multiple categories
    specificType = serializers.CharField(required=False, allow_blank=True)
    material = serializers.CharField(required=False, allow_blank=True)
    sizeShape = serializers.CharField(required=False, allow_blank=True)
    colours = serializers.CharField(required=False, allow_blank=True)
    finishing = serializers.CharField(required=False, allow_blank=True)
    permanence = serializers.CharField(required=False, allow_blank=True)
    permanenceFile = serializers.FileField(required=False, allow_null=True)
    
    # Category-specific additional fields
    content = serializers.CharField(required=False, allow_blank=True)  # Labels, Tags, Insert Cards
    ribbonWidth = serializers.CharField(required=False, allow_blank=True)  # Ribbons
    printingMethod = serializers.CharField(required=False, allow_blank=True)  # Various print categories
    fabricType = serializers.CharField(required=False, allow_blank=True)  # Printed Fabric Labels
    sealType = serializers.CharField(required=False, allow_blank=True)  # Security Seals
    serialization = serializers.CharField(required=False, allow_blank=True)  # Security Seals
    tamperEvidence = serializers.CharField(required=False, allow_blank=True)  # Security Seals
    printingSpec = serializers.CharField(required=False, allow_blank=True)  # Heat Transfers
    adhesiveStrength = serializers.CharField(required=False, allow_blank=True)  # Heat Transfers, Stickers
    strapWidth = serializers.CharField(required=False, allow_blank=True)  # Straps/Belts
    buckleType = serializers.CharField(required=False, allow_blank=True)  # Straps/Belts
    badgeType = serializers.CharField(required=False, allow_blank=True)  # Embroidered Badges
    borderFinish = serializers.CharField(required=False, allow_blank=True)  # Embroidered Badges
    patchSize = serializers.CharField(required=False, allow_blank=True)  # Leather/PU Patches
    embossDeboss = serializers.CharField(required=False, allow_blank=True)  # Leather/PU Patches
    attachmentMethod = serializers.CharField(required=False, allow_blank=True)  # Leather/PU Patches
    charmSize = serializers.CharField(required=False, allow_blank=True)  # Metal Charms
    metalFinish = serializers.CharField(required=False, allow_blank=True)  # Metal Charms
    engraving = serializers.CharField(required=False, allow_blank=True)  # Metal Charms
    joiningType = serializers.CharField(required=False, allow_blank=True)  # Metal Charms
    threadColours = serializers.CharField(required=False, allow_blank=True)  # Embroidery Thread
    stitchDensity = serializers.CharField(required=False, allow_blank=True)  # Embroidery Thread
    backingType = serializers.CharField(required=False, allow_blank=True)  # Embroidery Thread
    screenCount = serializers.CharField(required=False, allow_blank=True)  # Screen Print Transfers
    inkType = serializers.CharField(required=False, allow_blank=True)  # Screen Print Transfers
    applicationMethod = serializers.CharField(required=False, allow_blank=True)  # Screen Print Transfers
    tagType = serializers.CharField(required=False, allow_blank=True)  # Price Tags
    attachmentType = serializers.CharField(required=False, allow_blank=True)  # Price Tags
    qrBarcode = serializers.CharField(required=False, allow_blank=True)  # Price Tags
    
    def _get_category_specific_fields(self, category, validated_data):
        """Extract category-specific fields based on the selected artwork category."""
        
        # Base fields common to most artwork categories
        base_artwork_fields = [
            'specificType', 'material', 'sizeShape', 'colours', 'finishing', 'permanence'
        ]
        
        category_additional_fields = {
            'MAIN LABELS': ['content'],
            'CARE LABELS': ['content'],
            'SIZE LABELS': ['content'],
            'FLAG LABELS': ['content'],
            'HANG TAGS': ['content'],
            'BARCODE STICKERS': ['content'],
            'PRINTED FABRIC LABELS': ['content', 'fabricType', 'printingMethod'],
            'WOVEN LABELS': ['content'],
            'INSERT CARDS': ['content'],
            'RIBBONS': ['ribbonWidth'],
            'SECURITY SEALS / TAMPER TAGS': ['sealType', 'serialization', 'tamperEvidence'],
            'HEAT TRANSFER LABELS / PRINTS': ['printingSpec', 'adhesiveStrength', 'applicationMethod'],
            'PRINTED / BRANDED STRAPS / BELTS': ['strapWidth', 'buckleType'],
            'EMBROIDERED BADGES / PATCHES': ['badgeType', 'borderFinish'],
            'LEATHER / PU PATCHES': ['patchSize', 'embossDeboss', 'attachmentMethod'],
            'METAL CHARMS / LOGO PLATES': ['charmSize', 'metalFinish', 'engraving', 'joiningType'],
            'EMBROIDERY THREAD / DESIGN': ['threadColours', 'stitchDensity', 'backingType'],
            'SCREEN PRINT / TRANSFERS': ['screenCount', 'inkType', 'applicationMethod'],
            'PRICE TAGS / JOKER TAGS': ['tagType', 'attachmentType', 'qrBarcode']
        }
        
        # Get additional fields for this category
        additional = category_additional_fields.get(category, [])
        all_fields = base_artwork_fields + additional
        
        return {field: validated_data.get(field, '') for field in all_fields if field in validated_data}
    
    def create(self, validated_data):
        category = validated_data['category']
        
        # Extract category-specific fields
        category_specific_data = self._get_category_specific_fields(category, validated_data)
        
        # Handle permanence file if present
        if validated_data.get('permanenceFile'):
            category_specific_data['permanenceFile'] = 'uploaded'  # Actual file handling in view
        
        # Build model data
        model_data = {
            'factory_code_id': self.context.get('factory_code_id'),
            'category': category,
            'surplus': validated_data.get('surplus', ''),
            'surplus_for_section': validated_data.get('surplusForSection', ''),
            'usage': validated_data.get('usage', ''),
            'approval': validated_data.get('approval'),
            'remarks': validated_data.get('remarks', ''),
            'reference_image': validated_data.get('referenceImage'),
            'size_width': validated_data.get('sizeWidth', ''),
            'size_length': validated_data.get('sizeLength', ''),
            'size_height': validated_data.get('sizeHeight', ''),
            'size_unit': validated_data.get('sizeUnit'),
            'category_specific_data': category_specific_data
        }
        
        return ArtworkMaterial.objects.create(**model_data)


# =============================================================================
# STEP 5: PACKAGING
# =============================================================================

class PackagingMaterialSerializer(serializers.ModelSerializer):
    """Read serializer for PackagingMaterial"""
    size = serializers.SerializerMethodField()
    material_specific_data = serializers.JSONField(read_only=True)
    
    class Meta:
        model = PackagingMaterial
        fields = [
            'id', 'packaging', 'material_type', 'size',
            'colour', 'printing', 'printing_ref',
            'material_specific_data', 'created_at'
        ]
    
    def get_size(self, obj):
        return {
            'width': obj.size_width,
            'length': obj.size_length,
            'height': obj.size_height,
            'unit': obj.size_unit
        }


class PackagingMaterialCreateSerializer(serializers.Serializer):
    """
    Create serializer for PackagingMaterial with conditional fields based on material type
    """
    
    # Required field
    materialType = serializers.ChoiceField(
        choices=PackagingMaterialTypeChoices.choices,
        source='material_type'
    )
    
    # Common fields
    colour = serializers.CharField(required=False, allow_blank=True)
    printing = serializers.CharField(required=False, allow_blank=True)
    printingRef = serializers.FileField(required=False, allow_null=True)
    
    # Size fields
    sizeWidth = serializers.CharField(required=False, allow_blank=True)
    sizeLength = serializers.CharField(required=False, allow_blank=True)
    sizeHeight = serializers.CharField(required=False, allow_blank=True)
    sizeUnit = serializers.ChoiceField(
        choices=SizeUnitChoices.choices,
        required=False,
        allow_null=True
    )
    
    # Material-specific fields
    # CARTONS/CORRUGATED BOX
    noOfPlys = serializers.CharField(required=False, allow_blank=True)
    jointType = serializers.CharField(required=False, allow_blank=True)
    burstingStrength = serializers.CharField(required=False, allow_blank=True)
    
    # POLY BAG WITH FLAP
    guage = serializers.CharField(required=False, allow_blank=True)
    gummingQuality = serializers.CharField(required=False, allow_blank=True)
    punchHoles = serializers.CharField(required=False, allow_blank=True)
    
    # POLYSHEET / BALE WRAP
    guageGsm = serializers.CharField(required=False, allow_blank=True)
    rollWidth = serializers.CharField(required=False, allow_blank=True)
    rollWidthUnit = serializers.CharField(required=False, allow_blank=True)
    
    # POLY BAG WITH FLAP
    flapSize = serializers.CharField(required=False, allow_blank=True)
    
    # TAPE
    tapeWidth = serializers.CharField(required=False, allow_blank=True)
    tapeWidthUnit = serializers.CharField(required=False, allow_blank=True)
    
    def _get_material_specific_fields(self, material_type, validated_data):
        """Extract material-specific fields based on the selected material type."""
        
        material_field_map = {
            'CARTONS/CORRUGATED BOX': ['noOfPlys', 'jointType', 'burstingStrength'],
            'MASTER CARTONS': ['noOfPlys', 'jointType', 'burstingStrength'],
            'INNER CARTONS': ['noOfPlys', 'jointType', 'burstingStrength'],
            'POLY BAG WITH FLAP': ['guage', 'gummingQuality', 'punchHoles', 'flapSize'],
            'POLYSHEET': ['guageGsm', 'rollWidth', 'rollWidthUnit'],
            'BALE WRAP': ['guageGsm', 'rollWidth', 'rollWidthUnit'],
            'TAPE': ['guage', 'gummingQuality', 'tapeWidth', 'tapeWidthUnit'],
            'TISSUE / WRAPPING PAPER': []
        }
        
        fields = material_field_map.get(material_type, [])
        return {field: validated_data.get(field, '') for field in fields if field in validated_data}
    
    def create(self, validated_data):
        material_type = validated_data['material_type']
        
        # Extract material-specific fields
        material_specific_data = self._get_material_specific_fields(material_type, validated_data)
        
        # Build model data
        model_data = {
            'packaging_id': self.context.get('packaging_id'),
            'material_type': material_type,
            'colour': validated_data.get('colour', ''),
            'printing': validated_data.get('printing', ''),
            'printing_ref': validated_data.get('printingRef'),
            'size_width': validated_data.get('sizeWidth', ''),
            'size_length': validated_data.get('sizeLength', ''),
            'size_height': validated_data.get('sizeHeight', ''),
            'size_unit': validated_data.get('sizeUnit'),
            'material_specific_data': material_specific_data
        }
        
        return PackagingMaterial.objects.create(**model_data)


class PackagingSerializer(serializers.ModelSerializer):
    """Read serializer for Packaging with nested materials"""
    materials = PackagingMaterialSerializer(many=True, read_only=True)
    
    class Meta:
        model = Packaging
        fields = [
            'id', 'factory_code', 'packing_method', 'polybag_type',
            'silica_gel', 'remarks', 'materials', 'created_at'
        ]


class PackagingCreateSerializer(serializers.ModelSerializer):
    """Create serializer for Packaging"""
    materials = PackagingMaterialCreateSerializer(many=True, required=False)
    
    class Meta:
        model = Packaging
        fields = ['packing_method', 'polybag_type', 'silica_gel', 'remarks', 'materials']
    
    def create(self, validated_data):
        materials_data = validated_data.pop('materials', [])
        factory_code_id = self.context.get('factory_code_id')
        
        packaging = Packaging.objects.create(
            factory_code_id=factory_code_id,
            **validated_data
        )
        
        for mat_data in materials_data:
            mat_serializer = PackagingMaterialCreateSerializer(
                data=mat_data,
                context={'packaging_id': packaging.id}
            )
            if mat_serializer.is_valid():
                mat_serializer.save()
        
        return packaging


# =============================================================================
# COMPLETE FACTORY CODE WIZARD SERIALIZER
# =============================================================================

class FactoryCodeCompleteSerializer(serializers.ModelSerializer):
    """
    Complete read serializer for entire Factory Code with all nested data.
    Used for retrieving the complete factory code specification.
    """
    products = ProductSerializer(many=True, read_only=True)
    consumption_materials = ConsumptionMaterialSerializer(many=True, read_only=True)
    artwork_materials = ArtworkMaterialSerializer(many=True, read_only=True)
    packaging = PackagingSerializer(read_only=True)
    
    class Meta:
        model = FactoryCode
        fields = [
            'id', 'code', 'type', 'buyer', 'style_no', 'style_name',
            'size', 'gsm', 'article_description', 'colour',
            'reference_image', 'products', 'consumption_materials',
            'artwork_materials', 'packaging',
            'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at', 'created_by']


class FactoryCodeWizardCreateSerializer(serializers.Serializer):
    """
    Complete wizard create serializer - accepts the entire 6-step form data
    and creates all related objects in a single transaction.
    """
    
    # Step 0: Product Identification
    step0 = FactoryCodeCreateSerializer()
    
    # Step 1: Cut & Sew
    products = ProductCreateSerializer(many=True, required=False)
    
    # Step 2: Raw Materials (nested within products/components)
    rawMaterials = RawMaterialCreateSerializer(many=True, required=False)
    
    # Step 3: Consumption Materials
    consumptionMaterials = ConsumptionMaterialCreateSerializer(many=True, required=False)
    
    # Step 4: Artwork Materials
    artworkMaterials = ArtworkMaterialCreateSerializer(many=True, required=False)
    
    # Step 5: Packaging
    packaging = PackagingCreateSerializer(required=False)
    
    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        
        # Step 0: Create Factory Code
        step0_data = validated_data['step0']
        step0_data['tenant'] = request.user.tenant
        step0_data['created_by'] = request.user
        factory_code = FactoryCode.objects.create(**step0_data)
        
        # Step 1: Create Products and Components
        products_data = validated_data.get('products', [])
        for prod_data in products_data:
            components_data = prod_data.pop('components', [])
            product = Product.objects.create(factory_code=factory_code, **prod_data)
            for comp_data in components_data:
                Component.objects.create(product=product, **comp_data)
        
        # Step 2: Raw Materials would be created per component
        # (simplified - in real implementation, would link to components)
        raw_materials_data = validated_data.get('rawMaterials', [])
        for rm_data in raw_materials_data:
            rm_serializer = RawMaterialCreateSerializer(data=rm_data)
            if rm_serializer.is_valid():
                rm_serializer.save()
        
        # Step 3: Consumption Materials
        consumption_data = validated_data.get('consumptionMaterials', [])
        for cm_data in consumption_data:
            cm_serializer = ConsumptionMaterialCreateSerializer(
                data=cm_data,
                context={'factory_code_id': factory_code.id}
            )
            if cm_serializer.is_valid():
                cm_serializer.save()
        
        # Step 4: Artwork Materials
        artwork_data = validated_data.get('artworkMaterials', [])
        for am_data in artwork_data:
            am_serializer = ArtworkMaterialCreateSerializer(
                data=am_data,
                context={'factory_code_id': factory_code.id}
            )
            if am_serializer.is_valid():
                am_serializer.save()
        
        # Step 5: Packaging
        packaging_data = validated_data.get('packaging')
        if packaging_data:
            pkg_serializer = PackagingCreateSerializer(
                data=packaging_data,
                context={'factory_code_id': factory_code.id}
            )
            if pkg_serializer.is_valid():
                pkg_serializer.save()
        
        return factory_code


# =============================================================================
# INTERNAL PURCHASE ORDER SERIALIZERS
# =============================================================================

class InternalPurchaseOrderSerializer(serializers.ModelSerializer):
    """Read serializer for IPO"""
    buyer_code_display = serializers.CharField(source='buyer_code.code', read_only=True, default='')
    
    class Meta:
        model = InternalPurchaseOrder
        fields = [
            'id', 'ipo_code', 'order_type', 'buyer_code', 'buyer_code_text',
            'buyer_code_display', 'company_type', 'program_name', 'po_sr_no',
            'tenant', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'ipo_code', 'created_at', 'updated_at']


class InternalPurchaseOrderCreateSerializer(serializers.ModelSerializer):
    """Create serializer for IPO (code auto-generated)"""
    
    class Meta:
        model = InternalPurchaseOrder
        fields = [
            'id', 'ipo_code', 'order_type', 'buyer_code', 'buyer_code_text',
            'company_type', 'program_name', 'po_sr_no', 'tenant'
        ]
        read_only_fields = ['id', 'ipo_code']

    def validate_program_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Program name is required")
        return value.strip()

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        if 'tenant' not in validated_data and user and hasattr(user, 'tenant') and user.tenant:
            validated_data['tenant'] = user.tenant
        
        # Auto-calculate sr_no if not provided
        if 'po_sr_no' not in validated_data or not validated_data['po_sr_no']:
            validated_data['po_sr_no'] = InternalPurchaseOrder.get_next_sr_no(
                validated_data.get('program_name', ''),
                validated_data.get('tenant')
            )
        
        return InternalPurchaseOrder.objects.create(
            **validated_data,
            created_by=user
        )


# =============================================================================
# PURCHASE ORDER SERIALIZERS
# =============================================================================

class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Read serializer for PO"""
    buyer_display = serializers.CharField(source='buyer.code', read_only=True, default='')
    vendor_display = serializers.CharField(source='vendor.code', read_only=True, default='')
    buyer_name = serializers.CharField(source='buyer.buyer_name', read_only=True, default='')
    vendor_name = serializers.CharField(source='vendor.vendor_name', read_only=True, default='')
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_code', 'order_date', 'order_time', 'factory_po_number',
            'buyer', 'vendor', 'buyer_display', 'vendor_display',
            'buyer_name', 'vendor_name',
            'product_category', 'category_code', 'po_description', 'particulars',
            'quantity', 'unit_rate', 'amount', 'delivery_date', 'payment_terms',
            'remarks', 'last_po_number',
            'tenant', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'po_code', 'created_at', 'updated_at']


class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    """Create serializer for PO (code auto-generated)"""
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_code', 'order_date', 'order_time', 'factory_po_number',
            'buyer', 'vendor', 'product_category', 'category_code',
            'po_description', 'particulars', 'quantity', 'unit_rate', 'amount',
            'delivery_date', 'payment_terms', 'remarks', 'last_po_number', 'tenant'
        ]
        read_only_fields = ['id', 'po_code']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        if 'tenant' not in validated_data and user and hasattr(user, 'tenant') and user.tenant:
            validated_data['tenant'] = user.tenant
        
        return PurchaseOrder.objects.create(
            **validated_data,
            created_by=user
        )


# =============================================================================
# COMPANY ESSENTIAL SERIALIZERS
# =============================================================================

class CompanyEssentialSerializer(serializers.ModelSerializer):
    """Read serializer for CompanyEssential"""
    
    class Meta:
        model = CompanyEssential
        fields = [
            'id', 'category', 'code', 'entry_date', 'department', 'sr_no',
            'item_description', 'item', 'machine_type', 'component_spec',
            'quantity', 'amount', 'unit', 'for_field', 'remarks', 'reference_image',
            'tenant', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'code', 'sr_no', 'created_at', 'updated_at']


class CompanyEssentialCreateSerializer(serializers.ModelSerializer):
    """Create serializer for CompanyEssential (code auto-generated)"""
    
    class Meta:
        model = CompanyEssential
        fields = [
            'id', 'category', 'code', 'entry_date', 'department', 'sr_no',
            'item_description', 'item', 'machine_type', 'component_spec',
            'quantity', 'amount', 'unit', 'for_field', 'remarks', 'reference_image',
            'tenant'
        ]
        read_only_fields = ['id', 'code', 'sr_no']

    def validate_category(self, value):
        valid = [c[0] for c in CompanyEssential.CATEGORY_CHOICES]
        if value not in valid:
            raise serializers.ValidationError(f"Invalid category. Must be one of: {valid}")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        if 'tenant' not in validated_data and user and hasattr(user, 'tenant') and user.tenant:
            validated_data['tenant'] = user.tenant
        
        return CompanyEssential.objects.create(
            **validated_data,
            created_by=user
        )


class CompanyEssentialBulkCreateSerializer(serializers.Serializer):
    """Bulk create multiple company essentials"""
    items = CompanyEssentialCreateSerializer(many=True)

    def create(self, validated_data):
        request = self.context.get('request')
        created = []
        for item_data in validated_data['items']:
            serializer = CompanyEssentialCreateSerializer(
                data=item_data,
                context=self.context
            )
            serializer.is_valid(raise_exception=True)
            created.append(serializer.save())
        return created