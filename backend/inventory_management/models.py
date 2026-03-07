# from django.db import models
# from django.utils import timezone
# from django.db.models import Max
# import uuid


# class Department(models.Model):
#     """
#     Department Model
#     Represents different departments in the inventory management system
#     """
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     # Department Information
#     code = models.CharField(max_length=50, unique=True, db_index=True)  # e.g., 'chd-code', 'chd-po'
#     name = models.CharField(max_length=255)  # e.g., 'CHD CODE CREATION', 'CHD PO ISSUE'
#     description = models.TextField(blank=True, null=True)
    
#     # Display Order
#     display_order = models.IntegerField(default=0, help_text="Order in which department appears in menu")
    
#     # Status
#     is_active = models.BooleanField(default=True)
    
#     # Tenant Relationship (optional - can be shared across tenants)
#     tenant = models.ForeignKey(
#         'auth_service.Tenant',
#         on_delete=models.CASCADE,
#         related_name='departments',
#         null=True,
#         blank=True
#     )
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         'auth_service.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='created_departments'
#     )
    
#     class Meta:
#         db_table = 'departments'
#         verbose_name = 'Department'
#         verbose_name_plural = 'Departments'
#         ordering = ['display_order', 'name']
#         indexes = [
#             models.Index(fields=['code']),
#             models.Index(fields=['tenant', 'is_active']),
#         ]
    
#     def __str__(self):
#         return f"{self.name} ({self.code})"


# class Segment(models.Model):
#     """
#     Segment Model
#     Represents segments/sub-menus within a department
#     """
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     # Segment Information
#     code = models.CharField(max_length=50, db_index=True)  # e.g., 'buyer', 'vendor', 'factory'
#     name = models.CharField(max_length=255)  # e.g., 'BUYER', 'VENDOR', 'FACTORY'
#     description = models.TextField(blank=True, null=True)
    
#     # Department Relationship
#     department = models.ForeignKey(
#         Department,
#         on_delete=models.CASCADE,
#         related_name='segments'
#     )
    
#     # Display Order
#     display_order = models.IntegerField(default=0, help_text="Order in which segment appears in submenu")
    
#     # Status
#     is_active = models.BooleanField(default=True)
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         'auth_service.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='created_segments'
#     )
    
#     class Meta:
#         db_table = 'segments'
#         verbose_name = 'Segment'
#         verbose_name_plural = 'Segments'
#         ordering = ['department', 'display_order', 'name']
#         unique_together = [['department', 'code']]  # Code must be unique within a department
#         indexes = [
#             models.Index(fields=['department', 'code']),
#             models.Index(fields=['department', 'is_active']),
#         ]
    
#     def __str__(self):
#         return f"{self.department.name} - {self.name} ({self.code})"


# class BuyerCode(models.Model):
#     """
#     Buyer Code Model
#     Stores buyer information with auto-generated sequential codes (101A, 102A, etc.)
#     """
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     # Auto-generated code (101A, 102A, 103A, etc.)
#     code = models.CharField(max_length=20, unique=True, db_index=True)
    
#     # Buyer Information
#     buyer_name = models.CharField(max_length=255)
#     buyer_address = models.TextField()
#     contact_person = models.CharField(max_length=255)
#     retailer = models.CharField(max_length=255)
    
#     # Tenant Relationship
#     tenant = models.ForeignKey(
#         'auth_service.Tenant',
#         on_delete=models.CASCADE,
#         related_name='buyer_codes',
#         null=True,
#         blank=True
#     )
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         'auth_service.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='created_buyer_codes'
#     )
    
#     class Meta:
#         db_table = 'buyer_codes'
#         verbose_name = 'Buyer Code'
#         verbose_name_plural = 'Buyer Codes'
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['code']),
#             models.Index(fields=['tenant', 'created_at']),
#             models.Index(fields=['buyer_name']),
#         ]
    
#     def __str__(self):
#         return f"{self.code} - {self.buyer_name}"
    
#     @classmethod
#     def generate_next_code(cls, tenant=None):
#         """
#         Generate the next buyer code in sequence (101A, 102A, etc.)
#         Starts from 101A if no codes exist
#         """
#         # Filter by tenant if provided, otherwise get all
#         queryset = cls.objects.all()
#         if tenant:
#             queryset = queryset.filter(tenant=tenant)
        
#         # Get the highest existing code number
#         last_code = queryset.aggregate(Max('code'))['code__max']
        
#         if last_code:
#             # Extract number from code (e.g., "101A" -> 101)
#             try:
#                 # Remove 'A' suffix and convert to int
#                 last_number = int(last_code.replace('A', ''))
#                 next_number = last_number + 1
#             except (ValueError, AttributeError):
#                 # If parsing fails, start from 101
#                 next_number = 101
#         else:
#             # No codes exist, start from 101
#             next_number = 101
        
#         # Format as "XXXA"
#         return f"{next_number}A"
    
#     def save(self, *args, **kwargs):
#         """Auto-generate code if not provided"""
#         if not self.code:
#             self.code = self.generate_next_code(tenant=self.tenant)
#         super().save(*args, **kwargs)


# class VendorCode(models.Model):
#     """
#     Vendor Code Model
#     Stores vendor information with auto-generated sequential numeric codes (101, 102, etc.)
#     """
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     # Auto-generated code (101, 102, 103, etc.)
#     code = models.CharField(max_length=20, unique=True, db_index=True)
    
#     # Vendor Information
#     vendor_name = models.CharField(max_length=255)
#     address = models.TextField()
#     gst = models.CharField(max_length=15, db_index=True)  # GST Number
#     contact_person = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255, db_index=True)
#     whatsapp_number = models.CharField(max_length=15)
#     alt_whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    
#     # Banking Details
#     bank_name = models.CharField(max_length=255)
#     account_number = models.CharField(max_length=50)
#     ifsc_code = models.CharField(max_length=11)
    
#     # Job Work Details
#     job_work_category = models.CharField(max_length=255)
#     job_work_sub_category = models.CharField(max_length=255)
    
#     # Payment Terms
#     payment_terms = models.TextField()
    
#     # Tenant Relationship
#     tenant = models.ForeignKey(
#         'auth_service.Tenant',
#         on_delete=models.CASCADE,
#         related_name='vendor_codes',
#         null=True,
#         blank=True
#     )
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         'auth_service.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='created_vendor_codes'
#     )
    
#     class Meta:
#         db_table = 'vendor_codes'
#         verbose_name = 'Vendor Code'
#         verbose_name_plural = 'Vendor Codes'
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['code']),
#             models.Index(fields=['tenant', 'created_at']),
#             models.Index(fields=['vendor_name']),
#             models.Index(fields=['gst']),
#             models.Index(fields=['email']),
#         ]
    
#     def __str__(self):
#         return f"{self.code} - {self.vendor_name}"
    
#     @classmethod
#     def generate_next_code(cls, tenant=None):
#         """
#         Generate the next vendor code in sequence (101, 102, etc.)
#         Starts from 101 if no codes exist
#         """
#         # Filter by tenant if provided, otherwise get all
#         queryset = cls.objects.all()
#         if tenant:
#             queryset = queryset.filter(tenant=tenant)
        
#         # Get the highest existing code number
#         last_code = queryset.aggregate(Max('code'))['code__max']
        
#         if last_code:
#             # Extract number from code (e.g., "101" -> 101)
#             try:
#                 last_number = int(last_code)
#                 next_number = last_number + 1
#             except (ValueError, AttributeError):
#                 # If parsing fails, start from 101
#                 next_number = 101
#         else:
#             # No codes exist, start from 101
#             next_number = 101
        
#         # Return as string
#         return str(next_number)
    
#     def save(self, *args, **kwargs):
#         """Auto-generate code if not provided"""
#         if not self.code:
#             self.code = self.generate_next_code(tenant=self.tenant)
#         super().save(*args, **kwargs)


# """
# Factory Code Models for Inventory Management System - V2
# =========================================================

# UPDATED: Comprehensive expansion based on frontend GenerateFactoryCode.jsx

# This module defines Django models for the 6-step Factory Code generation wizard:
# - Step 0: Product Identification (FactoryCode)
# - Step 1: Cut & Sew Specification (Product, Component)
# - Step 2: Raw Material Sourcing (RawMaterial, WorkOrder)
# - Step 3: Trims & Accessories (ConsumptionMaterial) - EXPANDED with 30 categories
# - Step 4: Artwork & Labeling (ArtworkMaterial) - EXPANDED with 18 categories
# - Step 5: Packaging (Packaging, PackagingMaterial) - EXPANDED with conditional fields

# Design Principles:
# - All models use UUID primary keys (consistent with existing IMS patterns)
# - Multi-tenant support via tenant ForeignKey
# - Audit trail via created_by, created_at, updated_at
# - JSONField for category-specific conditional fields (reduces table complexity)
# - Auto-generated sequential codes for FactoryCode
# """

# from django.db import models
# from django.utils import timezone
# from django.db.models import Max
# import uuid


# # =============================================================================
# # ENUM CHOICES
# # =============================================================================

# class UnitChoices(models.TextChoices):
#     """Unit of measurement choices"""
#     R_METERS = 'R METERS', 'R METERS'
#     CM = 'CM', 'CM'
#     INCHES = 'Inches', 'Inches'
#     METER = 'Meter', 'Meter'
#     KGS = 'KGS', 'KGS'
#     PC = 'Pc', 'Pc'
#     SET = 'Set', 'Set'
#     ROLL = 'Roll', 'Roll'


# class SizeUnitChoices(models.TextChoices):
#     """Size unit choices"""
#     CMS = 'CMS', 'CMS'
#     INCHES = 'INCHES', 'INCHES'
#     MM = 'MM', 'MM'


# class WorkOrderTypeChoices(models.TextChoices):
#     """Work order process types"""
#     WEAVING = 'WEAVING', 'WEAVING'
#     TUFTING = 'TUFTING', 'TUFTING'
#     QUILTING = 'QUILTING', 'QUILTING'
#     PRINTING = 'PRINTING', 'PRINTING'
#     KNITTING = 'KNITTING', 'KNITTING'
#     EMBROIDERY = 'EMBROIDERY', 'EMBROIDERY'
#     DYEING = 'DYEING', 'DYEING'
#     BRAIDING = 'BRAIDING', 'BRAIDING'
#     CARPET = 'CARPET', 'CARPET'
#     CUTTING = 'CUTTING', 'CUTTING'
#     STITCHING = 'STITCHING', 'STITCHING'
#     SEWING = 'Sewing', 'Sewing'
#     PACKAGING = 'PACKAGING', 'PACKAGING'
#     OTHERS = 'OTHERS', 'OTHERS'


# class ApprovalChoices(models.TextChoices):
#     """Approval reference types"""
#     BUYERS = "BUYER'S", "BUYER'S"
#     INITIAL = 'INITIAL', 'INITIAL'
#     IPP = 'IPP', 'IPP'
#     PP = 'PP', 'PP'
#     TOP = 'TOP', 'TOP'


# class ApprovalAgainstChoices(models.TextChoices):
#     """Approval against reference types"""
#     BUYERS_SAMPLE = "BUYER'S SAMPLE", "BUYER'S SAMPLE"
#     INITIAL_SAMPLE = 'INITIAL SAMPLE', 'INITIAL SAMPLE'
#     PP_SAMPLE = 'PP SAMPLE', 'PP SAMPLE'


# class TrimAccessoryChoices(models.TextChoices):
#     """
#     Trim & Accessory category types - 30 categories
#     Each category has specific conditional fields stored in category_specific_data JSONField
#     """
#     ZIPPERS = 'ZIPPERS', 'ZIPPERS'
#     VELCRO = 'VELCRO', 'VELCRO'
#     STITCHING_THREAD = 'STITCHING THREAD', 'STITCHING THREAD'
#     BUTTONS = 'BUTTONS', 'BUTTONS'
#     RIVETS = 'RIVETS', 'RIVETS'
#     NIWAR = 'NIWAR (Webbing/Tapes)', 'NIWAR (Webbing/Tapes)'
#     LACE = 'LACE', 'LACE'
#     INTERLINING_FUSING = 'INTERLINING/FUSING', 'INTERLINING/FUSING'
#     HOOKS_EYES = 'HOOKS & EYES', 'HOOKS & EYES'
#     BUCKLES_ADJUSTERS = 'BUCKLES & ADJUSTERS', 'BUCKLES & ADJUSTERS'
#     EYELETS_GROMMETS = 'EYELETS & GROMMETS', 'EYELETS & GROMMETS'
#     ELASTIC = 'ELASTIC', 'ELASTIC'
#     FELT = 'FELT', 'FELT'
#     SHOULDER_PADS_CUPS = 'SHOULDER PADS / CUPS', 'SHOULDER PADS / CUPS'
#     TUBULAR_KNITS_RIBBING = 'TUBULAR KNITS / RIBBING', 'TUBULAR KNITS / RIBBING'
#     RFID_EAS_TAGS = 'RFID / EAS TAGS', 'RFID / EAS TAGS'
#     PLASTIC_CABLE_TIES = 'PLASTIC CABLE TIES / LOOPS', 'PLASTIC CABLE TIES / LOOPS'
#     FRINGE_TASSELS = 'FRINGE / TASSELS', 'FRINGE / TASSELS'
#     PLASTIC_PIPES_RODS = 'PLASTIC PIPES / RODS', 'PLASTIC PIPES / RODS'
#     SEAM_SEALING_TAPE = 'SEAM SEALING TAPE', 'SEAM SEALING TAPE'
#     ADHESIVES_GUNNING = 'ADHESIVES / GUNNING', 'ADHESIVES / GUNNING'
#     PRE_CUT_HEMS_BINDINGS = 'PRE-CUT HEMS / BINDINGS', 'PRE-CUT HEMS / BINDINGS'
#     REFLECTIVE_TAPES = 'REFLECTIVE TAPES / TRIMS', 'REFLECTIVE TAPES / TRIMS'
#     FIRE_RETARDANT_TRIMS = 'FIRE RETARDANT (FR) TRIMS', 'FIRE RETARDANT (FR) TRIMS'
#     REPAIR_KITS_PATCHES = 'REPAIR KITS / PATCHES', 'REPAIR KITS / PATCHES'
#     CORD_STOPS_LOCKS = 'CORD STOPS / CORD LOCKS / TOGGLES', 'CORD STOPS / CORD LOCKS / TOGGLES'
#     D_RINGS_O_RINGS = 'D-RINGS / O-RINGS / WEBBING LOOPS', 'D-RINGS / O-RINGS / WEBBING LOOPS'
#     FOAM_WADDING = 'FOAM / WADDING (Pre-Cut Shapes)', 'FOAM / WADDING (Pre-Cut Shapes)'
#     PINS_TAGGING_BARBS = 'PINS / TAGGING BARBS', 'PINS / TAGGING BARBS'
#     MAGNETIC_CLOSURES = 'MAGNETIC CLOSURES / SNAPS', 'MAGNETIC CLOSURES / SNAPS'


# class ArtworkCategoryChoices(models.TextChoices):
#     """
#     Artwork & Labeling category types - 18 categories
#     Each category has specific conditional fields stored in category_specific_data JSONField
#     """
#     LABELS_BRAND_MAIN = 'LABELS (BRAND/MAIN)', 'LABELS (BRAND/MAIN)'
#     CARE_COMPOSITION = 'CARE & COMPOSITION', 'CARE & COMPOSITION'
#     TAGS_SPECIAL_LABELS = 'TAGS & SPECIAL LABELS', 'TAGS & SPECIAL LABELS'
#     FLAMMABILITY_SAFETY = 'FLAMMABILITY / SAFETY LABELS', 'FLAMMABILITY / SAFETY LABELS'
#     RFID_SECURITY_TAGS = 'RFID / SECURITY TAGS', 'RFID / SECURITY TAGS'
#     LAW_LABEL_CONTENTS = 'LAW LABEL / CONTENTS TAG', 'LAW LABEL / CONTENTS TAG'
#     HANG_TAG_SEALS = 'HANG TAG SEALS / STRINGS', 'HANG TAG SEALS / STRINGS'
#     PRICE_TICKET_BARCODE = 'PRICE TICKET / BARCODE TAG', 'PRICE TICKET / BARCODE TAG'
#     HEAT_TRANSFER_LABELS = 'HEAT TRANSFER LABELS', 'HEAT TRANSFER LABELS'
#     UPC_LABEL_BARCODE = 'UPC LABEL / BARCODE STICKER', 'UPC LABEL / BARCODE STICKER'
#     SIZE_LABELS = 'SIZE LABELS (INDIVIDUAL)', 'SIZE LABELS (INDIVIDUAL)'
#     ANTI_COUNTERFEIT = 'ANTI-COUNTERFEIT & HOLOGRAMS', 'ANTI-COUNTERFEIT & HOLOGRAMS'
#     QC_INSPECTION = 'QC / INSPECTION LABELS', 'QC / INSPECTION LABELS'
#     BELLY_BAND = 'BELLY BAND / WRAPPER', 'BELLY BAND / WRAPPER'
#     TYVEK_LABELS = 'TYVEK LABELS', 'TYVEK LABELS'
#     TAFFETA_LABELS = 'TAFFETA LABELS', 'TAFFETA LABELS'
#     INSERT_CARDS = 'INSERT CARDS', 'INSERT CARDS'
#     RIBBONS = 'RIBBONS', 'RIBBONS'


# class PackagingMaterialTypeChoices(models.TextChoices):
#     """Packaging material type choices - 8 types"""
#     CARTONS_CORRUGATED = 'CARTONS/CORRUGATED BOX', 'CARTONS/CORRUGATED BOX'
#     PACKAGING_ACCESSORIES = 'PACKAGING ACCESSORIES', 'PACKAGING ACCESSORIES'
#     TAPE = 'TAPE', 'TAPE'
#     POLYBAG = 'POLYBAG', 'POLYBAG'
#     POLY_BAG_FLAP = 'POLY BAG WITH FLAP', 'POLY BAG WITH FLAP'
#     POLYSHEET = 'POLYSHEET', 'POLYSHEET'
#     BALE_WRAP = 'BALE WRAP', 'BALE WRAP'
#     OTHER = 'OTHER', 'OTHER'


# class PackagingTypeChoices(models.TextChoices):
#     """Packaging configuration type"""
#     STANDARD = 'STANDARD', 'STANDARD'
#     ASSORTED = 'ASSORTED', 'ASSORTED (LINK IPC#)'


# # =============================================================================
# # STEP 0: FACTORY CODE (Main Entity)
# # =============================================================================

# class FactoryCode(models.Model):
#     """
#     Main Factory Code entity - Step 0: Product Identification
    
#     Auto-generates sequential codes like FC-101, FC-102, etc.
#     Central entity linking all steps of the factory code wizard.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     # Tenant relationship (for multi-tenant support)
#     tenant = models.ForeignKey(
#         'auth_service.Tenant',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='factory_codes'
#     )
    
#     # Auto-generated code
#     code = models.CharField(max_length=50, unique=True, editable=False)
    
#     # Step 0 fields
#     sku = models.CharField(max_length=100, blank=True, null=True)
#     product_name = models.CharField(max_length=255, blank=True, null=True)
#     buyer_code = models.ForeignKey(
#         'BuyerCode',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='factory_codes'
#     )
    
#     # Status tracking
#     STATUS_CHOICES = [
#         ('draft', 'Draft'),
#         ('pending', 'Pending Approval'),
#         ('approved', 'Approved'),
#         ('in_production', 'In Production'),
#         ('completed', 'Completed'),
#     ]
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
#     # Metadata
#     is_active = models.BooleanField(default=True)
#     notes = models.TextField(blank=True, null=True)
    
#     # Audit fields
#     created_by = models.ForeignKey(
#         'auth_service.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='created_factory_codes'
#     )
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_codes'
#         ordering = ['-created_at']
#         verbose_name = 'Factory Code'
#         verbose_name_plural = 'Factory Codes'
    
#     def save(self, *args, **kwargs):
#         if not self.code:
#             # Generate sequential code FC-101, FC-102, etc.
#             last_code = FactoryCode.objects.aggregate(Max('code'))['code__max']
#             if last_code:
#                 try:
#                     last_num = int(last_code.split('-')[1])
#                     self.code = f"FC-{last_num + 1}"
#                 except (IndexError, ValueError):
#                     self.code = "FC-101"
#             else:
#                 self.code = "FC-101"
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return f"{self.code} - {self.product_name or 'Unnamed'}"


# # =============================================================================
# # STEP 1: CUT & SEW SPECIFICATION (Product & Components)
# # =============================================================================

# class Product(models.Model):
#     """
#     Product definition within a Factory Code - Step 1
    
#     A factory code can have multiple products (e.g., COMFORTER, PILLOW, BAG).
#     Each product has multiple components.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     factory_code = models.ForeignKey(
#         FactoryCode,
#         on_delete=models.CASCADE,
#         related_name='products'
#     )
    
#     # Product info
#     name = models.CharField(max_length=255)
#     sequence = models.PositiveIntegerField(default=1)
    
#     # Optional specs
#     description = models.TextField(blank=True, null=True)
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_products'
#         ordering = ['factory_code', 'sequence']
#         unique_together = ['factory_code', 'name']
    
#     def __str__(self):
#         return f"{self.factory_code.code} - {self.name}"


# class Component(models.Model):
#     """
#     Component within a Product - Step 1
    
#     Components define parts of a product (e.g., Front Panel, Back Panel, Border).
#     Each component links to raw materials and has sewing specifications.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='components'
#     )
    
#     # Component info
#     name = models.CharField(max_length=255)
#     sequence = models.PositiveIntegerField(default=1)
    
#     # Size specifications
#     length = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
#     width = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
#     height = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
#     size_unit = models.CharField(
#         max_length=10,
#         choices=SizeUnitChoices.choices,
#         default=SizeUnitChoices.INCHES,
#         blank=True
#     )
    
#     # Additional specs (JSONField for flexibility)
#     specifications = models.JSONField(default=dict, blank=True)
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_components'
#         ordering = ['product', 'sequence']
    
#     def __str__(self):
#         return f"{self.product.name} - {self.name}"


# # =============================================================================
# # STEP 2: RAW MATERIAL SOURCING
# # =============================================================================

# class RawMaterial(models.Model):
#     """
#     Raw Material Specification - Step 2
    
#     Links to Product and Component, defines material requirements.
#     Has nested WorkOrders for manufacturing processes.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     factory_code = models.ForeignKey(
#         FactoryCode,
#         on_delete=models.CASCADE,
#         related_name='raw_materials'
#     )
    
#     # Links
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='raw_materials',
#         null=True,
#         blank=True
#     )
#     component = models.ForeignKey(
#         Component,
#         on_delete=models.CASCADE,
#         related_name='raw_materials',
#         null=True,
#         blank=True
#     )
    
#     # Material info
#     product_name = models.CharField(max_length=255, blank=True, null=True)
#     component_name = models.CharField(max_length=255, blank=True, null=True)
#     material_description = models.CharField(max_length=500, blank=True, null=True)
    
#     # Consumption
#     net_consumption = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
#     unit = models.CharField(
#         max_length=20,
#         choices=UnitChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Additional data
#     specifications = models.JSONField(default=dict, blank=True)
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_raw_materials'
#         ordering = ['factory_code', 'created_at']
    
#     def __str__(self):
#         return f"{self.factory_code.code} - {self.material_description or 'Material'}"


# class WorkOrder(models.Model):
#     """
#     Work Order within Raw Material - Step 2
    
#     Defines manufacturing processes (WEAVING, DYEING, CUTTING, etc.)
#     Each raw material can have multiple work orders.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     raw_material = models.ForeignKey(
#         RawMaterial,
#         on_delete=models.CASCADE,
#         related_name='work_orders'
#     )
    
#     # Work order type
#     work_order = models.CharField(
#         max_length=50,
#         choices=WorkOrderTypeChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Common fields
#     wastage = models.CharField(max_length=50, blank=True, null=True)  # Percentage
#     for_field = models.CharField(max_length=255, blank=True, null=True)  # FOR section
#     for_section = models.CharField(max_length=255, blank=True, null=True)
    
#     # Machine/Type specific
#     machine_type = models.CharField(max_length=100, blank=True, null=True)
#     quilting_type = models.CharField(max_length=100, blank=True, null=True)
#     printing_type = models.CharField(max_length=100, blank=True, null=True)
#     dyeing_type = models.CharField(max_length=100, blank=True, null=True)
    
#     # Design
#     design = models.CharField(max_length=255, blank=True, null=True)
    
#     # Image reference
#     image_ref = models.FileField(upload_to='work_orders/images/', blank=True, null=True)
    
#     # Approval
#     approval_against = models.CharField(
#         max_length=50,
#         choices=ApprovalAgainstChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     remarks = models.TextField(blank=True, null=True)
    
#     # Process-specific data (JSONField for WEAVING, KNITTING, DYEING conditional fields)
#     process_specific_data = models.JSONField(
#         default=dict,
#         blank=True,
#         help_text="""
#         Stores process-specific fields:
        
#         WEAVING: {
#             "reed": "", "pick": "",
#             "warp": true/false, "weft": true/false,
#             "ratioWarp": "", "ratioWeft": "",
#             "ratioWeightWarp": ""
#         }
        
#         KNITTING: {
#             "wales": true/false, "courses": true/false,
#             "ratioWales": "", "ratioCourses": "",
#             "ratioWeightWales": ""
#         }
        
#         DYEING: {
#             "receivedColorReference": "PANTONE/ARS/CSI/PMS",
#             "referenceType": "TPG/TCX/COATED/UNCOAT",
#             "shrinkageWidth": true/false, "shrinkageLength": true/false,
#             "shrinkageWidthPercent": "", "shrinkageLengthPercent": "",
#             "ratioWidth": "", "ratioLength": ""
#         }
        
#         TUFTING/CARPET: {
#             "pileHeight": "", "tpi": ""
#         }
        
#         CUTTING: {
#             "cutType": "LAYERED/PANEL", "cutSize": ""
#         }
#         """
#     )
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_work_orders'
#         ordering = ['raw_material', 'created_at']
    
#     def __str__(self):
#         return f"{self.raw_material} - {self.work_order or 'Work Order'}"


# # =============================================================================
# # STEP 3: TRIMS & ACCESSORIES (CONSUMPTION MATERIALS)
# # =============================================================================

# class ConsumptionMaterial(models.Model):
#     """
#     Consumption Material (Trims & Accessories) - Step 3
    
#     EXPANDED: 30 trim/accessory categories with conditional fields.
#     Category-specific fields stored in category_specific_data JSONField.
    
#     Common fields for ALL trim types:
#     - testingRequirement, testingRequirementFile
#     - lengthQuantity
#     - surplus, surplusForSection
#     - approval
#     - remarks
#     - unitAdditional (for width/length)
    
#     Size object:
#     - size.width, size.length, size.height, size.unit
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     factory_code = models.ForeignKey(
#         FactoryCode,
#         on_delete=models.CASCADE,
#         related_name='consumption_materials'
#     )
    
#     # Links
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='consumption_materials',
#         null=True,
#         blank=True
#     )
#     component = models.ForeignKey(
#         Component,
#         on_delete=models.CASCADE,
#         related_name='consumption_materials',
#         null=True,
#         blank=True
#     )
    
#     # Material info
#     product_name = models.CharField(max_length=255, blank=True, null=True)
#     component_name = models.CharField(max_length=255, blank=True, null=True)
#     material_description = models.CharField(max_length=500, blank=True, null=True)
    
#     # Consumption
#     net_consumption = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
#     unit = models.CharField(
#         max_length=20,
#         choices=UnitChoices.choices,
#         blank=True,
#         null=True
#     )
#     unit_additional = models.CharField(max_length=20, blank=True, null=True)  # mm/in/cm
    
#     # Trim/Accessory category
#     trim_accessory = models.CharField(
#         max_length=100,
#         choices=TrimAccessoryChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Size (nested object)
#     size_width = models.CharField(max_length=50, blank=True, null=True)
#     size_length = models.CharField(max_length=50, blank=True, null=True)
#     size_height = models.CharField(max_length=50, blank=True, null=True)
#     size_unit = models.CharField(
#         max_length=10,
#         choices=SizeUnitChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Common fields for all trims
#     testing_requirement = models.CharField(max_length=500, blank=True, null=True)
#     testing_requirement_file = models.FileField(
#         upload_to='consumption_materials/testing/',
#         blank=True,
#         null=True
#     )
#     length_quantity = models.CharField(max_length=255, blank=True, null=True)
#     surplus = models.CharField(max_length=50, blank=True, null=True)  # Percentage
#     surplus_for_section = models.CharField(max_length=255, blank=True, null=True)
#     approval = models.CharField(max_length=100, blank=True, null=True)
#     remarks = models.TextField(blank=True, null=True)
    
#     # Work order
#     work_order = models.CharField(
#         max_length=50,
#         choices=WorkOrderTypeChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Category-specific data (JSONField)
#     category_specific_data = models.JSONField(
#         default=dict,
#         blank=True,
#         help_text="See TRIM_CATEGORY_FIELDS_SCHEMA for structure"
#     )
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_consumption_materials'
#         ordering = ['factory_code', 'created_at']
    
#     def __str__(self):
#         return f"{self.factory_code.code} - {self.trim_accessory or self.material_description or 'Material'}"


# # =============================================================================
# # STEP 4: ARTWORK & LABELING
# # =============================================================================

# class ArtworkMaterial(models.Model):
#     """
#     Artwork & Labeling Material - Step 4
    
#     EXPANDED: 18 artwork categories with conditional fields.
#     Category-specific fields stored in category_specific_data JSONField.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     factory_code = models.ForeignKey(
#         FactoryCode,
#         on_delete=models.CASCADE,
#         related_name='artwork_materials'
#     )
    
#     # Component info
#     components = models.CharField(max_length=255, blank=True, null=True)
#     material_description = models.CharField(max_length=500, blank=True, null=True)
    
#     # Consumption
#     net_consumption = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
#     unit = models.CharField(
#         max_length=20,
#         choices=UnitChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Placement
#     placement = models.CharField(max_length=500, blank=True, null=True)
    
#     # Work order
#     work_order = models.CharField(
#         max_length=50,
#         choices=WorkOrderTypeChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Artwork category
#     artwork_category = models.CharField(
#         max_length=100,
#         choices=ArtworkCategoryChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Size fields
#     size_width = models.CharField(max_length=50, blank=True, null=True)
#     size_length = models.CharField(max_length=50, blank=True, null=True)
#     size_height = models.CharField(max_length=50, blank=True, null=True)
#     size_unit = models.CharField(
#         max_length=10,
#         choices=SizeUnitChoices.choices,
#         blank=True,
#         null=True
#     )
#     size_artwork_id = models.CharField(max_length=100, blank=True, null=True)
    
#     # Common fields
#     testing_requirement = models.CharField(max_length=500, blank=True, null=True)
#     reference_image = models.FileField(
#         upload_to='artwork_materials/references/',
#         blank=True,
#         null=True
#     )
#     length_quantity = models.CharField(max_length=255, blank=True, null=True)
#     length_quantity_for_section = models.CharField(max_length=255, blank=True, null=True)
#     surplus = models.CharField(max_length=50, blank=True, null=True)
#     surplus_for_section = models.CharField(max_length=255, blank=True, null=True)
#     approval = models.CharField(
#         max_length=20,
#         choices=ApprovalChoices.choices,
#         blank=True,
#         null=True
#     )
#     remarks = models.TextField(blank=True, null=True)
    
#     # Specific type (common across many categories)
#     specific_type = models.CharField(max_length=255, blank=True, null=True)
#     material = models.CharField(max_length=255, blank=True, null=True)
#     colours = models.CharField(max_length=255, blank=True, null=True)
#     finishing = models.CharField(max_length=255, blank=True, null=True)
#     permanence = models.CharField(max_length=255, blank=True, null=True)
#     permanence_file = models.FileField(
#         upload_to='artwork_materials/permanence/',
#         blank=True,
#         null=True
#     )
    
#     # Category-specific data (JSONField)
#     category_specific_data = models.JSONField(
#         default=dict,
#         blank=True,
#         help_text="See ARTWORK_CATEGORY_FIELDS_SCHEMA for structure"
#     )
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_artwork_materials'
#         ordering = ['factory_code', 'created_at']
    
#     def __str__(self):
#         return f"{self.factory_code.code} - {self.artwork_category or self.material_description or 'Artwork'}"


# # =============================================================================
# # STEP 5: PACKAGING
# # =============================================================================

# class Packaging(models.Model):
#     """
#     Packaging Configuration - Step 5 Header
    
#     Main packaging settings for a factory code.
#     Has nested PackagingMaterial items.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     factory_code = models.OneToOneField(
#         FactoryCode,
#         on_delete=models.CASCADE,
#         related_name='packaging'
#     )
    
#     # Header configuration
#     product_selection = models.CharField(max_length=500, blank=True, null=True)
#     packaging_type = models.CharField(
#         max_length=50,
#         choices=PackagingTypeChoices.choices,
#         default=PackagingTypeChoices.STANDARD
#     )
#     casepack_qty = models.PositiveIntegerField(null=True, blank=True)
#     assorted_sku_link = models.CharField(max_length=100, blank=True, null=True)
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_packaging'
    
#     def __str__(self):
#         return f"{self.factory_code.code} - Packaging"


# class PackagingMaterial(models.Model):
#     """
#     Packaging Material - Step 5 Materials
    
#     EXPANDED: 8 packaging material types with conditional fields.
#     Material-specific fields stored in material_specific_data JSONField.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     packaging = models.ForeignKey(
#         Packaging,
#         on_delete=models.CASCADE,
#         related_name='materials'
#     )
    
#     # Basic info
#     components = models.CharField(max_length=255, blank=True, null=True)
#     product = models.CharField(max_length=255, blank=True, null=True)  # Material description
#     net_consumption_per_pc = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
#     unit = models.CharField(
#         max_length=20,
#         choices=UnitChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Work order
#     work_order = models.CharField(max_length=100, blank=True, null=True)
    
#     # Placement
#     placement = models.CharField(max_length=500, blank=True, null=True)
    
#     # Size
#     size_width = models.CharField(max_length=50, blank=True, null=True)
#     size_length = models.CharField(max_length=50, blank=True, null=True)
#     size_height = models.CharField(max_length=50, blank=True, null=True)
#     size_unit = models.CharField(
#         max_length=10,
#         choices=SizeUnitChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Packaging material type
#     packaging_material_type = models.CharField(
#         max_length=100,
#         choices=PackagingMaterialTypeChoices.choices,
#         blank=True,
#         null=True
#     )
    
#     # Common fields
#     surplus = models.CharField(max_length=50, blank=True, null=True)
#     surplus_for_section = models.CharField(max_length=255, blank=True, null=True)
#     approval_against = models.CharField(max_length=255, blank=True, null=True)
#     remarks = models.TextField(blank=True, null=True)
    
#     # Type-specific fields (kept as columns for common use)
#     no_of_plys = models.CharField(max_length=50, blank=True, null=True)  # CARTONS
#     joint_type = models.CharField(max_length=100, blank=True, null=True)  # CARTONS
#     bursting_strength = models.CharField(max_length=100, blank=True, null=True)  # CARTONS
#     guage = models.CharField(max_length=50, blank=True, null=True)  # POLY BAG, TAPE
#     printing_ref = models.FileField(
#         upload_to='packaging_materials/printing/',
#         blank=True,
#         null=True
#     )
#     gumming_quality = models.CharField(max_length=100, blank=True, null=True)  # POLY BAG, TAPE
#     punch_holes = models.CharField(max_length=100, blank=True, null=True)  # POLY BAG WITH FLAP
#     flap_size = models.CharField(max_length=50, blank=True, null=True)  # POLY BAG WITH FLAP
#     guage_gsm = models.CharField(max_length=50, blank=True, null=True)  # POLYSHEET, BALE WRAP
#     roll_width = models.CharField(max_length=50, blank=True, null=True)  # POLYSHEET, BALE WRAP
#     roll_width_unit = models.CharField(max_length=20, blank=True, null=True)
#     tape_width = models.CharField(max_length=50, blank=True, null=True)  # TAPE
#     tape_width_unit = models.CharField(max_length=20, blank=True, null=True)
    
#     # Material-specific data (JSONField for any additional fields)
#     material_specific_data = models.JSONField(
#         default=dict,
#         blank=True,
#         help_text="See PACKAGING_MATERIAL_FIELDS_SCHEMA for structure"
#     )
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_packaging_materials'
#         ordering = ['packaging', 'created_at']
    
#     def __str__(self):
#         return f"{self.packaging.factory_code.code} - {self.packaging_material_type or self.product or 'Material'}"


# class PackagingWorkOrder(models.Model):
#     """
#     Work Order for Packaging Material - Step 5
    
#     Each packaging material can have work orders.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     packaging_material = models.ForeignKey(
#         PackagingMaterial,
#         on_delete=models.CASCADE,
#         related_name='work_orders'
#     )
    
#     work_order = models.CharField(max_length=100, blank=True, null=True)
    
#     # Additional work order data
#     work_order_data = models.JSONField(default=dict, blank=True)
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'factory_code_packaging_work_orders'
    
#     def __str__(self):
#         return f"{self.packaging_material} - {self.work_order or 'Work Order'}"


# # =============================================================================
# # JSON FIELD SCHEMAS (For Documentation & Validation)
# # =============================================================================

# TRIM_CATEGORY_FIELDS_SCHEMA = {
#     "ZIPPERS": {
#         "fields": [
#             "zipNumber", "zipType", "brand", "teeth", "puller",
#             "pullerType", "length"
#         ],
#         "options": {
#             "zipType": ["Concealed", "Open", "Closed-End"],
#             "brand": ["YKK", "RIRI", "SBS"],
#             "teeth": ["Coil", "Plastic", "Metal"],
#             "pullerType": ["Lockable", "Non-Lockable"]
#         }
#     },
#     "VELCRO": {
#         "fields": [
#             "velcroType", "velcroMaterial", "width", "colour",
#             "hookDensityLoopType", "cycleLife", "attachmentMethod"
#         ],
#         "options": {
#             "velcroType": ["Sew-on", "Adhesive", "Die-Cut", "ONE-WRAP"],
#             "velcroMaterial": ["Nylon", "Polyester"]
#         }
#     },
#     "STITCHING THREAD": {
#         "fields": [
#             "threadType", "fibreContent", "countTicketNo", "ply",
#             "colour", "threadFinish", "usage"
#         ],
#         "options": {
#             "threadType": ["Spun Polyester", "Cotton", "Core Spun"],
#             "threadFinish": ["Bonded", "Lubricated", "Matte"]
#         }
#     },
#     "BUTTONS": {
#         "fields": [
#             "buttonType", "buttonMaterial", "sizeLigne", "finishColour",
#             "buttonAttachmentMethod", "function"
#         ],
#         "options": {
#             "buttonType": ["Sewing", "Snap", "Tack"],
#             "buttonMaterial": ["Polyester", "Metal", "Natural"],
#             "sizeLigne": ["14L", "16L", "20L", "24L"]
#         }
#     },
#     "RIVETS": {
#         "fields": [
#             "rivetType", "rivetMaterial", "capSize", "postHeightLength",
#             "finishPlating", "pullerStrength", "rivetPullerType"
#         ],
#         "options": {
#             "rivetType": ["Open-End", "Close-End", "Blind"],
#             "rivetMaterial": ["Brass", "Copper", "Zinc", "Steel"],
#             "capSize": ["8mm", "9mm", "10mm"]
#         }
#     },
#     "NIWAR (Webbing/Tapes)": {
#         "fields": [
#             "niwarType", "niwarMaterial", "niwarWidth", "niwarThickness",
#             "niwarColour", "finishCoating", "tensileStrength"
#         ],
#         "options": {
#             "niwarType": ["Woven", "Knitted"]
#         }
#     },
#     "LACE": {
#         "fields": [
#             "laceType", "laceMaterial", "laceWidth", "laceColour",
#             "laceFinishing", "laceUsage", "designReference"
#         ],
#         "options": {
#             "laceType": ["Woven", "Braided", "Crochet", "Knit"]
#         }
#     },
#     "INTERLINING/FUSING": {
#         "fields": [
#             "interliningType", "interliningMaterial", "gsmWeight",
#             "adhesive", "interliningColour", "fusingSpec"
#         ],
#         "options": {
#             "interliningType": ["Woven", "Non-woven", "Knitted", "Fusible"],
#             "adhesive": ["PA", "PES", "EVA"]
#         }
#     },
#     "HOOKS & EYES": {
#         "fields": [
#             "hookEyeType", "hookEyeMaterial", "hookEyeSize", "hookEyeColour",
#             "hookEyeFinish", "strength", "application"
#         ],
#         "options": {
#             "hookEyeMaterial": ["Brass", "Steel", "Nickel"],
#             "hookEyeSize": ["#1", "#2", "#3"]
#         }
#     },
#     "BUCKLES & ADJUSTERS": {
#         "fields": [
#             "buckleType", "buckleMaterial", "buckleSize", "buckleFinishColour",
#             "buckleFunction", "buckleTensileStrength"
#         ],
#         "options": {
#             "buckleType": ["Side Release", "Center Bar", "Ladder Lock"],
#             "buckleMaterial": ["Plastic", "Metal", "Nylon"]
#         }
#     },
#     "EYELETS & GROMMETS": {
#         "fields": [
#             "eyeletType", "eyeletMaterial", "innerDiameter", "outerDiameter",
#             "eyeletColour", "eyeletApplication", "tooling"
#         ]
#     },
#     "ELASTIC": {
#         "fields": [
#             "elasticType", "elasticMaterial", "elasticWidth", "elasticColour",
#             "stretchTension", "elasticPacking"
#         ],
#         "options": {
#             "elasticType": ["Woven", "Braided", "Knitted"],
#             "elasticMaterial": ["Rubber", "Spandex", "Latex"]
#         }
#     },
#     "FELT": {
#         "fields": [
#             "feltType", "feltMaterial", "feltThickness", "densityGsm",
#             "feltColour", "feltFinishForm", "feltApplication"
#         ],
#         "options": {
#             "feltType": ["Wool", "Synthetic", "Blended"],
#             "feltThickness": ["2mm", "3mm", "5mm"]
#         }
#     },
#     "SHOULDER PADS / CUPS": {
#         "fields": [
#             "shoulderPadType", "shoulderPadMaterial", "shoulderPadSize",
#             "shape", "covering", "shoulderPadAttachment", "weight"
#         ],
#         "options": {
#             "shoulderPadMaterial": ["Polyurethane", "Polyester", "Cotton"]
#         }
#     },
#     "TUBULAR KNITS / RIBBING": {
#         "fields": [
#             "tubularType", "tubularMaterial", "widthDiameter", "weightDensity",
#             "tubularColour", "stretchPercent", "cutting"
#         ],
#         "options": {
#             "tubularType": ["1x1 Rib", "2x2 Rib", "Interlock", "Jersey"]
#         }
#     },
#     "RFID / EAS TAGS": {
#         "fields": [
#             "rfidType", "formFactor", "frequency", "chipIcType",
#             "rfidSize", "coding", "security"
#         ],
#         "options": {
#             "rfidType": ["UHF RFID", "HF RFID", "LF RFID", "EAS Tag"],
#             "formFactor": ["Label", "Sticker", "Hard Tag", "Inlay"]
#         }
#     },
#     "PLASTIC CABLE TIES / LOOPS": {
#         "fields": [
#             "cableTieType", "cableTieMaterial", "cableTieSize", "cableTieColour",
#             "cableTieTensileStrength", "cableTieFinish", "cableTieUsage"
#         ],
#         "options": {
#             "cableTieType": ["Standard", "Releasable", "Beaded", "Loop"],
#             "cableTieMaterial": ["Nylon 6/6", "Polypropylene", "Stainless Steel"]
#         }
#     },
#     "FRINGE / TASSELS": {
#         "fields": [
#             "fringeType", "fringeMaterial", "dropLength", "tapeWidth",
#             "fringeColour", "fringeFinish", "construction"
#         ],
#         "options": {
#             "fringeType": ["Fringe", "Tassel", "Pom-pom", "Bullion"],
#             "fringeMaterial": ["Cotton", "Polyester", "Rayon", "Wool", "Blend"]
#         }
#     },
#     "PLASTIC PIPES / RODS": {
#         "fields": [
#             "pipeType", "pipeMaterial", "diameterDimensions", "pipeLength",
#             "pipeColour", "endCaps", "flexibility", "pipeUsage"
#         ],
#         "options": {
#             "pipeType": ["Round Pipe", "Square Rod", "Flat Bar", "Custom Shape"],
#             "pipeMaterial": ["PVC", "Polypropylene", "Nylon", "ABS", "Polyethylene"],
#             "flexibility": ["Rigid", "Semi-flexible", "Flexible"]
#         }
#     },
#     "SEAM SEALING TAPE": {
#         "fields": [
#             "seamTapeType", "seamTapeMaterial", "seamTapeWidth", "seamTapeColour",
#             "seamTapeAdhesiveType", "applicationSpec", "elasticity"
#         ],
#         "options": {
#             "seamTapeType": ["PU Tape", "TPU Tape", "Hot Melt"],
#             "seamTapeAdhesiveType": ["Hot Melt", "Pressure Sensitive", "Heat Activated"]
#         }
#     },
#     "ADHESIVES / GUNNING": {
#         "fields": [
#             "adhesiveType", "materialBase", "adhesiveApplication", "viscosity",
#             "settingTime", "adhesiveColour", "applicator"
#         ],
#         "options": {
#             "adhesiveType": ["Hot Melt", "Contact Adhesive", "Spray Adhesive"],
#             "materialBase": ["EVA", "PU", "Polyamide", "Acrylic", "Rubber-based"]
#         }
#     },
#     "PRE-CUT HEMS / BINDINGS": {
#         "fields": [
#             "hemType", "hemMaterial", "cutType", "hemWidth",
#             "foldType", "hemColour", "hemPackaging"
#         ],
#         "options": {
#             "hemType": ["Bias Binding", "Straight Cut", "Curved Hem"],
#             "cutType": ["Straight", "Bias (45°)", "Curved"],
#             "foldType": ["Single fold", "Double fold", "Unfolded"]
#         }
#     },
#     "REFLECTIVE TAPES / TRIMS": {
#         "fields": [
#             "reflectiveType", "reflectiveMaterial", "reflectiveWidth",
#             "reflectiveColour", "certification", "baseFabric"
#         ],
#         "options": {
#             "reflectiveType": ["Glass Bead", "Prismatic", "Microprismatic"],
#             "certification": ["EN ISO 20471", "ANSI/ISEA 107", "CSA Z96"]
#         }
#     },
#     "FIRE RETARDANT (FR) TRIMS": {
#         "fields": [
#             "frType", "frMaterial", "complianceLevel", "frColour",
#             "durability", "frComponents"
#         ],
#         "options": {
#             "frMaterial": ["Nomex", "Kevlar", "FR Cotton", "FR Polyester"],
#             "complianceLevel": ["NFPA 701", "EN 11612", "ASTM D6413", "CPAI-84"]
#         }
#     },
#     "REPAIR KITS / PATCHES": {
#         "fields": [
#             "repairKitType", "repairKitMaterial", "sizeShape", "repairKitColour",
#             "repairKitPackaging", "userApplication", "contents"
#         ],
#         "options": {
#             "repairKitType": ["Patch Kit", "Repair Tape", "Adhesive Patch"],
#             "userApplication": ["Heat press", "Iron-on", "Adhesive", "Sew-on"]
#         }
#     },
#     "CORD STOPS / CORD LOCKS / TOGGLES": {
#         "fields": [
#             "cordStopType", "cordStopMaterial", "cordStopSize", "cordStopColour",
#             "lockingMechanism", "cordStopFunction"
#         ],
#         "options": {
#             "cordStopType": ["Cord Stop", "Cord Lock", "Toggle", "Spring Lock"],
#             "cordStopMaterial": ["Nylon", "Acetal", "POM", "Plastic"],
#             "lockingMechanism": ["Spring-loaded", "Friction", "Cam lock", "Push-pull"]
#         }
#     },
#     "D-RINGS / O-RINGS / WEBBING LOOPS": {
#         "fields": [
#             "dRingType", "dRingMaterial", "dRingSize", "thicknessGauge",
#             "dRingFinishPlating", "loadRating", "dRingApplication"
#         ],
#         "options": {
#             "dRingType": ["D-Ring", "O-Ring", "Webbing Loop", "Triangle Ring"],
#             "dRingMaterial": ["Steel", "Stainless Steel", "Brass", "Aluminium", "Plastic"]
#         }
#     },
#     "FOAM / WADDING (Pre-Cut Shapes)": {
#         "fields": [
#             "foamType", "foamDensity", "foamThickness", "shapeId",
#             "foamColour", "properties", "foamAttachment"
#         ],
#         "options": {
#             "foamType": ["Polyurethane", "Polyethylene", "EVA", "Memory Foam"],
#             "foamAttachment": ["Adhesive-backed", "Sewn-in", "Velcro", "Snap-on"]
#         }
#     },
#     "PINS / TAGGING BARBS": {
#         "fields": [
#             "pinType", "pinMaterial", "pinSize", "pinColour",
#             "pinTensileStrength", "headType", "pinApplication"
#         ],
#         "options": {
#             "pinType": ["Tagging Pin", "Safety Pin", "T-Pin", "U-Pin"],
#             "pinMaterial": ["Stainless Steel", "Nickel-plated", "Brass", "Plastic"],
#             "headType": ["Round head", "Flat head", "Ball head", "T-head"]
#         }
#     },
#     "MAGNETIC CLOSURES / SNAPS": {
#         "fields": [
#             "magneticType", "magneticMaterial", "magneticSize", "magneticStrength",
#             "polarity", "magneticApplication"
#         ],
#         "options": {
#             "magneticType": ["Magnetic Snap", "Magnetic Button", "Magnetic Closure"],
#             "magneticMaterial": ["Neodymium", "Ferrite", "Samarium Cobalt", "Plastic housing"]
#         }
#     }
# }

# ARTWORK_CATEGORY_FIELDS_SCHEMA = {
#     "LABELS (BRAND/MAIN)": {
#         "fields": [
#             "specificType", "material", "sizeArtworkId", "foldType",
#             "colours", "finishing", "placement"
#         ],
#         "options": {
#             "specificType": ["Woven (Damask, Taffeta, Satin)", "Printed (Satin, Cotton)", "Heat Transfer", "Leather", "Metal"],
#             "foldType": ["End-fold", "Center-fold", "Miter-fold", "Straight Cut"]
#         }
#     },
#     "CARE & COMPOSITION": {
#         "fields": [
#             "specificType", "material", "countryOfOrigin", "manufacturerId",
#             "symbol", "language", "permanence"
#         ],
#         "options": {
#             "specificType": ["Woven", "Printed", "Heat Transfer"]
#         }
#     },
#     "TAGS & SPECIAL LABELS": {
#         "fields": [
#             "specificType", "material", "sizeArtworkId", "attachment",
#             "content", "finishing", "placement"
#         ],
#         "options": {
#             "specificType": ["Hang Tag (Paper/Card)", "Price Tag", "Size Label", "Flag"]
#         }
#     },
#     "FLAMMABILITY / SAFETY LABELS": {
#         "fields": [
#             "specificType", "content", "symbol", "certificationId",
#             "language", "placement"
#         ],
#         "options": {
#             "specificType": ["Permanent Sew-in Label", "Removable Hang Tag"]
#         }
#     },
#     "RFID / SECURITY TAGS": {
#         "fields": [
#             "specificType", "formFactor", "chipFrequency", "coding",
#             "adhesive", "security", "sizeArtworkId"
#         ],
#         "options": {
#             "specificType": ["Soft EAS Label", "UHF RFID Sticker", "Hard Tag"],
#             "formFactor": ["Adhesive Label", "Integrated Woven Label"]
#         }
#     },
#     "LAW LABEL / CONTENTS TAG": {
#         "fields": [
#             "lawLabelType", "lawLabelMaterial", "fillingMaterials",
#             "newUsedStatus", "registrationLicenses", "permanence",
#             "permanenceFile", "testingRequirement", "lengthQuantity",
#             "lengthQuantityForSection", "surplus"
#         ]
#     },
#     "HANG TAG SEALS / STRINGS": {
#         "fields": [
#             "hangTagType", "hangTagMaterial", "sealShape", "fastening",
#             "preStringing", "application", "colours", "sizeArtworkId"
#         ]
#     },
#     "PRICE TICKET / BARCODE TAG": {
#         "fields": [
#             "priceTicketType", "priceTicketMaterial", "content",
#             "barcodeType", "adhesive", "finishing", "sizeArtworkId"
#         ],
#         "options": {
#             "priceTicketType": ["Adhesive Sticker", "Printed Area", "Dedicated Small Tag"]
#         }
#     },
#     "HEAT TRANSFER LABELS": {
#         "fields": [
#             "heatTransferType", "heatTransferMaterialBase", "applicationSpec",
#             "colours", "finishHandFeel", "placement", "sizeArtworkId"
#         ],
#         "options": {
#             "heatTransferType": ["Brand Logo", "Size Tag", "Minimal Care", "Instructions", "Reflective"]
#         }
#     },
#     "UPC LABEL / BARCODE STICKER": {
#         "fields": [
#             "upcType", "upcMaterial", "content", "quality",
#             "adhesive", "placement", "sizeArtworkId"
#         ],
#         "options": {
#             "upcType": ["Adhesive Sticker", "Pre-Printed Barcode Area"]
#         }
#     },
#     "SIZE LABELS (INDIVIDUAL)": {
#         "fields": [
#             "sizeLabelType", "sizeLabelMaterial", "finishing",
#             "colours", "placement", "permanence", "sizeArtworkId"
#         ],
#         "options": {
#             "sizeLabelType": ["Woven Flag Label", "Printed Flag Label", "Heat Transfer", "Small Sticker"]
#         }
#     },
#     "ANTI-COUNTERFEIT & HOLOGRAMS": {
#         "fields": [
#             "antiCounterfeitType", "antiCounterfeitMaterial", "securityFeature",
#             "application", "placement", "verification", "sizeArtworkId"
#         ],
#         "options": {
#             "antiCounterfeitType": ["Hologram Sticker", "Void/Tamper-Evident Label", "Authenticity Patch", "Invisible Ink Print"]
#         }
#     },
#     "QC / INSPECTION LABELS": {
#         "fields": [
#             "qcLabelType", "qcLabelMaterial", "content",
#             "application", "removal", "traceability", "sizeArtworkId"
#         ],
#         "options": {
#             "qcLabelType": ["Passed/Inspected Sticker", "Hold/Defective Sticker", "Audit Sample Tag"]
#         }
#     },
#     "BELLY BAND / WRAPPER": {
#         "fields": [
#             "bellyBandType", "bellyBandMaterial", "closure",
#             "content", "closureFinish", "durability", "sizeArtworkId"
#         ],
#         "options": {
#             "bellyBandType": ["Cardboard Sleeve", "Printed Paper Band", "Plastic Film Wrapper"]
#         }
#     },
#     "TYVEK LABELS": {
#         "fields": [
#             "tyvekType", "tyvekMaterial", "content",
#             "inkType", "durability", "permanence", "sizeArtworkId"
#         ],
#         "options": {
#             "tyvekType": ["Law Label", "Shipping Tag", "Permanent Industrial/Outdoor Care Label"]
#         }
#     },
#     "TAFFETA LABELS": {
#         "fields": [
#             "taffetaType", "taffetaMaterial", "content",
#             "printQuality", "durability", "finishing", "sizeArtworkId"
#         ],
#         "options": {
#             "taffetaType": ["Printed Care Label", "Composition Label", "Temporary Size Label"]
#         }
#     },
#     "INSERT CARDS": {
#         "fields": [
#             "specificType", "material", "sizeShape", "content",
#             "finishing", "permanence"
#         ],
#         "options": {
#             "specificType": ["Shirt Board", "Neck Support", "Tissue Paper Insert", "Promotional Insert Card"]
#         }
#     },
#     "RIBBONS": {
#         "fields": [
#             "specificType", "material", "ribbonWidth", "colours",
#             "finishing", "usage"
#         ],
#         "options": {
#             "specificType": ["Satin", "Grosgrain", "Sheer Organza", "Printed Polyester", "Woven Edge"]
#         }
#     }
# }

# PACKAGING_MATERIAL_FIELDS_SCHEMA = {
#     "CARTONS/CORRUGATED BOX": {
#         "fields": ["noOfPlys", "jointType", "burstingStrength"],
#         "placeholders": {
#             "noOfPlys": "5 PLY/7 PLY",
#             "jointType": "STAPLE/BINDED",
#             "burstingStrength": "175 LBS"
#         }
#     },
#     "POLY BAG WITH FLAP": {
#         "fields": ["guage", "gummingQuality", "punchHoles", "printingRef"],
#         "placeholders": {
#             "guage": "200",
#             "gummingQuality": "High/Standard",
#             "punchHoles": "e.g., 2 holes"
#         }
#     },
#     "POLYSHEET": {
#         "fields": ["guageGsm", "rollWidth", "rollWidthUnit"],
#         "placeholders": {
#             "guageGsm": "200",
#             "rollWidth": "60"
#         }
#     },
#     "BALE WRAP": {
#         "fields": ["guageGsm", "rollWidth", "rollWidthUnit"],
#         "placeholders": {
#             "guageGsm": "200",
#             "rollWidth": "60"
#         }
#     },
#     "TAPE": {
#         "fields": ["guage", "gummingQuality", "tapeWidth", "tapeWidthUnit", "printingRef"],
#         "placeholders": {
#             "guage": "200",
#             "gummingQuality": "Strong/Standard",
#             "tapeWidth": "3"
#         }
#     }
# }

from django.db import models
from django.utils import timezone
from django.db.models import Max
import uuid


class Department(models.Model):
    """
    Department Model
    Represents different departments in the inventory management system
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Department Information
    code = models.CharField(max_length=50, unique=True, db_index=True)  # e.g., 'chd-code', 'chd-po'
    name = models.CharField(max_length=255)  # e.g., 'CHD CODE CREATION', 'CHD PO ISSUE'
    description = models.TextField(blank=True, null=True)
    
    # Display Order
    display_order = models.IntegerField(default=0, help_text="Order in which department appears in menu")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Tenant Relationship (optional - can be shared across tenants)
    tenant = models.ForeignKey(
        'auth_service.Tenant',
        on_delete=models.CASCADE,
        related_name='departments',
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth_service.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_departments'
    )
    
    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['tenant', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Segment(models.Model):
    """
    Segment Model
    Represents segments/sub-menus within a department
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Segment Information
    code = models.CharField(max_length=50, db_index=True)  # e.g., 'buyer', 'vendor', 'factory'
    name = models.CharField(max_length=255)  # e.g., 'BUYER', 'VENDOR', 'FACTORY'
    description = models.TextField(blank=True, null=True)
    
    # Department Relationship
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='segments'
    )
    
    # Display Order
    display_order = models.IntegerField(default=0, help_text="Order in which segment appears in submenu")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth_service.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_segments'
    )
    
    class Meta:
        db_table = 'segments'
        verbose_name = 'Segment'
        verbose_name_plural = 'Segments'
        ordering = ['department', 'display_order', 'name']
        unique_together = [['department', 'code']]  # Code must be unique within a department
        indexes = [
            models.Index(fields=['department', 'code']),
            models.Index(fields=['department', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.department.name} - {self.name} ({self.code})"


class BuyerCode(models.Model):
    """
    Buyer Code Model
    Stores buyer information with auto-generated sequential codes (101A, 102A, etc.)
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Auto-generated code (101A, 102A, 103A, etc.)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Buyer Information
    buyer_name = models.CharField(max_length=255)
    buyer_address = models.TextField()
    contact_person = models.CharField(max_length=255)
    retailer = models.CharField(max_length=255)
    
    # Tenant Relationship
    tenant = models.ForeignKey(
        'auth_service.Tenant',
        on_delete=models.CASCADE,
        related_name='buyer_codes',
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth_service.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_buyer_codes'
    )
    
    class Meta:
        db_table = 'buyer_codes'
        verbose_name = 'Buyer Code'
        verbose_name_plural = 'Buyer Codes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['tenant', 'created_at']),
            models.Index(fields=['buyer_name']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.buyer_name}"
    
    @classmethod
    def generate_next_code(cls, tenant=None):
        """
        Generate the next buyer code in sequence (101A, 102A, etc.)
        Starts from 101A if no codes exist
        """
        # Filter by tenant if provided, otherwise get all
        queryset = cls.objects.all()
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        
        # Get the highest existing code number
        last_code = queryset.aggregate(Max('code'))['code__max']
        
        if last_code:
            # Extract number from code (e.g., "101A" -> 101)
            try:
                # Remove 'A' suffix and convert to int
                last_number = int(last_code.replace('A', ''))
                next_number = last_number + 1
            except (ValueError, AttributeError):
                # If parsing fails, start from 101
                next_number = 101
        else:
            # No codes exist, start from 101
            next_number = 101
        
        # Format as "XXXA"
        return f"{next_number}A"
    
    def save(self, *args, **kwargs):
        """Auto-generate code if not provided"""
        if not self.code:
            self.code = self.generate_next_code(tenant=self.tenant)
        super().save(*args, **kwargs)


class VendorCode(models.Model):
    """
    Vendor Code Model
    Stores vendor information with auto-generated sequential numeric codes (101, 102, etc.)
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Auto-generated code (101, 102, 103, etc.)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Vendor Information
    vendor_name = models.CharField(max_length=255)
    address = models.TextField()
    gst = models.CharField(max_length=15, db_index=True)  # GST Number
    contact_person = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, db_index=True)
    whatsapp_number = models.CharField(max_length=15)
    alt_whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Banking Details
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=11)
    
    # Job Work Details
    job_work_category = models.CharField(max_length=255)
    job_work_sub_category = models.CharField(max_length=255)
    
    # Payment Terms
    payment_terms = models.TextField()
    
    # Tenant Relationship
    tenant = models.ForeignKey(
        'auth_service.Tenant',
        on_delete=models.CASCADE,
        related_name='vendor_codes',
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth_service.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_vendor_codes'
    )
    
    class Meta:
        db_table = 'vendor_codes'
        verbose_name = 'Vendor Code'
        verbose_name_plural = 'Vendor Codes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['tenant', 'created_at']),
            models.Index(fields=['vendor_name']),
            models.Index(fields=['gst']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.vendor_name}"
    
    @classmethod
    def generate_next_code(cls, tenant=None):
        """
        Generate the next vendor code in sequence (101, 102, etc.)
        Starts from 101 if no codes exist
        """
        # Filter by tenant if provided, otherwise get all
        queryset = cls.objects.all()
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        
        # Get the highest existing code number
        last_code = queryset.aggregate(Max('code'))['code__max']
        
        if last_code:
            # Extract number from code (e.g., "101" -> 101)
            try:
                last_number = int(last_code)
                next_number = last_number + 1
            except (ValueError, AttributeError):
                # If parsing fails, start from 101
                next_number = 101
        else:
            # No codes exist, start from 101
            next_number = 101
        
        # Return as string
        return str(next_number)
    
    def save(self, *args, **kwargs):
        """Auto-generate code if not provided"""
        if not self.code:
            self.code = self.generate_next_code(tenant=self.tenant)
        super().save(*args, **kwargs)


"""
Factory Code Models for Inventory Management System - V2
=========================================================

UPDATED: Comprehensive expansion based on frontend GenerateFactoryCode.jsx

This module defines Django models for the 6-step Factory Code generation wizard:
- Step 0: Product Identification (FactoryCode)
- Step 1: Cut & Sew Specification (Product, Component)
- Step 2: Raw Material Sourcing (RawMaterial, WorkOrder)
- Step 3: Trims & Accessories (ConsumptionMaterial) - EXPANDED with 30 categories
- Step 4: Artwork & Labeling (ArtworkMaterial) - EXPANDED with 18 categories
- Step 5: Packaging (Packaging, PackagingMaterial) - EXPANDED with conditional fields

Design Principles:
- All models use UUID primary keys (consistent with existing IMS patterns)
- Multi-tenant support via tenant ForeignKey
- Audit trail via created_by, created_at, updated_at
- JSONField for category-specific conditional fields (reduces table complexity)
- Auto-generated sequential codes for FactoryCode
"""

from django.db import models
from django.utils import timezone
from django.db.models import Max
import uuid


# =============================================================================
# ENUM CHOICES
# =============================================================================

class UnitChoices(models.TextChoices):
    """Unit of measurement choices"""
    R_METERS = 'R METERS', 'R METERS'
    CM = 'CM', 'CM'
    INCHES = 'Inches', 'Inches'
    METER = 'Meter', 'Meter'
    KGS = 'KGS', 'KGS'
    PC = 'Pc', 'Pc'
    SET = 'Set', 'Set'
    ROLL = 'Roll', 'Roll'


class SizeUnitChoices(models.TextChoices):
    """Size unit choices"""
    CMS = 'CMS', 'CMS'
    INCHES = 'INCHES', 'INCHES'
    MM = 'MM', 'MM'


class WorkOrderTypeChoices(models.TextChoices):
    """Work order process types"""
    WEAVING = 'WEAVING', 'WEAVING'
    TUFTING = 'TUFTING', 'TUFTING'
    QUILTING = 'QUILTING', 'QUILTING'
    PRINTING = 'PRINTING', 'PRINTING'
    KNITTING = 'KNITTING', 'KNITTING'
    EMBROIDERY = 'EMBROIDERY', 'EMBROIDERY'
    DYEING = 'DYEING', 'DYEING'
    BRAIDING = 'BRAIDING', 'BRAIDING'
    CARPET = 'CARPET', 'CARPET'
    CUTTING = 'CUTTING', 'CUTTING'
    STITCHING = 'STITCHING', 'STITCHING'
    SEWING = 'Sewing', 'Sewing'
    PACKAGING = 'PACKAGING', 'PACKAGING'
    OTHERS = 'OTHERS', 'OTHERS'


class ApprovalChoices(models.TextChoices):
    """Approval reference types"""
    BUYERS = "BUYER'S", "BUYER'S"
    INITIAL = 'INITIAL', 'INITIAL'
    IPP = 'IPP', 'IPP'
    PP = 'PP', 'PP'
    TOP = 'TOP', 'TOP'


class ApprovalAgainstChoices(models.TextChoices):
    """Approval against reference types"""
    BUYERS_SAMPLE = "BUYER'S SAMPLE", "BUYER'S SAMPLE"
    INITIAL_SAMPLE = 'INITIAL SAMPLE', 'INITIAL SAMPLE'
    PP_SAMPLE = 'PP SAMPLE', 'PP SAMPLE'


class TrimAccessoryChoices(models.TextChoices):
    """
    Trim & Accessory category types - 30 categories
    Each category has specific conditional fields stored in category_specific_data JSONField
    """
    ZIPPERS = 'ZIPPERS', 'ZIPPERS'
    VELCRO = 'VELCRO', 'VELCRO'
    STITCHING_THREAD = 'STITCHING THREAD', 'STITCHING THREAD'
    BUTTONS = 'BUTTONS', 'BUTTONS'
    RIVETS = 'RIVETS', 'RIVETS'
    NIWAR = 'NIWAR (Webbing/Tapes)', 'NIWAR (Webbing/Tapes)'
    LACE = 'LACE', 'LACE'
    INTERLINING_FUSING = 'INTERLINING/FUSING', 'INTERLINING/FUSING'
    HOOKS_EYES = 'HOOKS & EYES', 'HOOKS & EYES'
    BUCKLES_ADJUSTERS = 'BUCKLES & ADJUSTERS', 'BUCKLES & ADJUSTERS'
    EYELETS_GROMMETS = 'EYELETS & GROMMETS', 'EYELETS & GROMMETS'
    ELASTIC = 'ELASTIC', 'ELASTIC'
    FELT = 'FELT', 'FELT'
    SHOULDER_PADS_CUPS = 'SHOULDER PADS / CUPS', 'SHOULDER PADS / CUPS'
    TUBULAR_KNITS_RIBBING = 'TUBULAR KNITS / RIBBING', 'TUBULAR KNITS / RIBBING'
    RFID_EAS_TAGS = 'RFID / EAS TAGS', 'RFID / EAS TAGS'
    PLASTIC_CABLE_TIES = 'PLASTIC CABLE TIES / LOOPS', 'PLASTIC CABLE TIES / LOOPS'
    FRINGE_TASSELS = 'FRINGE / TASSELS', 'FRINGE / TASSELS'
    PLASTIC_PIPES_RODS = 'PLASTIC PIPES / RODS', 'PLASTIC PIPES / RODS'
    SEAM_SEALING_TAPE = 'SEAM SEALING TAPE', 'SEAM SEALING TAPE'
    ADHESIVES_GUNNING = 'ADHESIVES / GUNNING', 'ADHESIVES / GUNNING'
    PRE_CUT_HEMS_BINDINGS = 'PRE-CUT HEMS / BINDINGS', 'PRE-CUT HEMS / BINDINGS'
    REFLECTIVE_TAPES = 'REFLECTIVE TAPES / TRIMS', 'REFLECTIVE TAPES / TRIMS'
    FIRE_RETARDANT_TRIMS = 'FIRE RETARDANT (FR) TRIMS', 'FIRE RETARDANT (FR) TRIMS'
    REPAIR_KITS_PATCHES = 'REPAIR KITS / PATCHES', 'REPAIR KITS / PATCHES'
    CORD_STOPS_LOCKS = 'CORD STOPS / CORD LOCKS / TOGGLES', 'CORD STOPS / CORD LOCKS / TOGGLES'
    D_RINGS_O_RINGS = 'D-RINGS / O-RINGS / WEBBING LOOPS', 'D-RINGS / O-RINGS / WEBBING LOOPS'
    FOAM_WADDING = 'FOAM / WADDING (Pre-Cut Shapes)', 'FOAM / WADDING (Pre-Cut Shapes)'
    PINS_TAGGING_BARBS = 'PINS / TAGGING BARBS', 'PINS / TAGGING BARBS'
    MAGNETIC_CLOSURES = 'MAGNETIC CLOSURES / SNAPS', 'MAGNETIC CLOSURES / SNAPS'


class ArtworkCategoryChoices(models.TextChoices):
    """
    Artwork & Labeling category types - 18 categories
    Each category has specific conditional fields stored in category_specific_data JSONField
    """
    LABELS_BRAND_MAIN = 'LABELS (BRAND/MAIN)', 'LABELS (BRAND/MAIN)'
    CARE_COMPOSITION = 'CARE & COMPOSITION', 'CARE & COMPOSITION'
    TAGS_SPECIAL_LABELS = 'TAGS & SPECIAL LABELS', 'TAGS & SPECIAL LABELS'
    FLAMMABILITY_SAFETY = 'FLAMMABILITY / SAFETY LABELS', 'FLAMMABILITY / SAFETY LABELS'
    RFID_SECURITY_TAGS = 'RFID / SECURITY TAGS', 'RFID / SECURITY TAGS'
    LAW_LABEL_CONTENTS = 'LAW LABEL / CONTENTS TAG', 'LAW LABEL / CONTENTS TAG'
    HANG_TAG_SEALS = 'HANG TAG SEALS / STRINGS', 'HANG TAG SEALS / STRINGS'
    PRICE_TICKET_BARCODE = 'PRICE TICKET / BARCODE TAG', 'PRICE TICKET / BARCODE TAG'
    HEAT_TRANSFER_LABELS = 'HEAT TRANSFER LABELS', 'HEAT TRANSFER LABELS'
    UPC_LABEL_BARCODE = 'UPC LABEL / BARCODE STICKER', 'UPC LABEL / BARCODE STICKER'
    SIZE_LABELS = 'SIZE LABELS (INDIVIDUAL)', 'SIZE LABELS (INDIVIDUAL)'
    ANTI_COUNTERFEIT = 'ANTI-COUNTERFEIT & HOLOGRAMS', 'ANTI-COUNTERFEIT & HOLOGRAMS'
    QC_INSPECTION = 'QC / INSPECTION LABELS', 'QC / INSPECTION LABELS'
    BELLY_BAND = 'BELLY BAND / WRAPPER', 'BELLY BAND / WRAPPER'
    TYVEK_LABELS = 'TYVEK LABELS', 'TYVEK LABELS'
    TAFFETA_LABELS = 'TAFFETA LABELS', 'TAFFETA LABELS'
    INSERT_CARDS = 'INSERT CARDS', 'INSERT CARDS'
    RIBBONS = 'RIBBONS', 'RIBBONS'


class PackagingMaterialTypeChoices(models.TextChoices):
    """Packaging material type choices - 8 types"""
    CARTONS_CORRUGATED = 'CARTONS/CORRUGATED BOX', 'CARTONS/CORRUGATED BOX'
    PACKAGING_ACCESSORIES = 'PACKAGING ACCESSORIES', 'PACKAGING ACCESSORIES'
    TAPE = 'TAPE', 'TAPE'
    POLYBAG = 'POLYBAG', 'POLYBAG'
    POLY_BAG_FLAP = 'POLY BAG WITH FLAP', 'POLY BAG WITH FLAP'
    POLYSHEET = 'POLYSHEET', 'POLYSHEET'
    BALE_WRAP = 'BALE WRAP', 'BALE WRAP'
    OTHER = 'OTHER', 'OTHER'


class PackagingTypeChoices(models.TextChoices):
    """Packaging configuration type"""
    STANDARD = 'STANDARD', 'STANDARD'
    ASSORTED = 'ASSORTED', 'ASSORTED (LINK IPC#)'


# =============================================================================
# STEP 0: FACTORY CODE (Main Entity)
# =============================================================================

class FactoryCode(models.Model):
    """
    Main Factory Code entity - Step 0: Product Identification
    
    Auto-generates sequential codes like FC-101, FC-102, etc.
    Central entity linking all steps of the factory code wizard.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Tenant relationship (for multi-tenant support)
    tenant = models.ForeignKey(
        'auth_service.Tenant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='factory_codes'
    )
    
    # Auto-generated code
    code = models.CharField(max_length=50, unique=True, editable=False)
    
    # Step 0 fields
    sku = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    buyer_code = models.ForeignKey(
        'BuyerCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='factory_codes'
    )
    
    # Status tracking
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('in_production', 'In Production'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Metadata
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    
    # Audit fields
    created_by = models.ForeignKey(
        'auth_service.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_factory_codes'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_codes'
        ordering = ['-created_at']
        verbose_name = 'Factory Code'
        verbose_name_plural = 'Factory Codes'
    
    def save(self, *args, **kwargs):
        if not self.code:
            # Generate sequential code FC-101, FC-102, etc.
            last_code = FactoryCode.objects.aggregate(Max('code'))['code__max']
            if last_code:
                try:
                    last_num = int(last_code.split('-')[1])
                    self.code = f"FC-{last_num + 1}"
                except (IndexError, ValueError):
                    self.code = "FC-101"
            else:
                self.code = "FC-101"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.code} - {self.product_name or 'Unnamed'}"


# =============================================================================
# STEP 1: CUT & SEW SPECIFICATION (Product & Components)
# =============================================================================

class Product(models.Model):
    """
    Product definition within a Factory Code - Step 1
    
    A factory code can have multiple products (e.g., COMFORTER, PILLOW, BAG).
    Each product has multiple components.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    factory_code = models.ForeignKey(
        FactoryCode,
        on_delete=models.CASCADE,
        related_name='products'
    )
    
    # Product info
    name = models.CharField(max_length=255)
    sequence = models.PositiveIntegerField(default=1)
    
    # Optional specs
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_products'
        ordering = ['factory_code', 'sequence']
        unique_together = ['factory_code', 'name']
    
    def __str__(self):
        return f"{self.factory_code.code} - {self.name}"


class Component(models.Model):
    """
    Component within a Product - Step 1
    
    Components define parts of a product (e.g., Front Panel, Back Panel, Border).
    Each component links to raw materials and has sewing specifications.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='components'
    )
    
    # Component info
    name = models.CharField(max_length=255)
    sequence = models.PositiveIntegerField(default=1)
    
    # Size specifications
    length = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    size_unit = models.CharField(
        max_length=10,
        choices=SizeUnitChoices.choices,
        default=SizeUnitChoices.INCHES,
        blank=True
    )
    
    # Additional specs (JSONField for flexibility)
    specifications = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_components'
        ordering = ['product', 'sequence']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"


# =============================================================================
# STEP 2: RAW MATERIAL SOURCING
# =============================================================================

class RawMaterial(models.Model):
    """
    Raw Material Specification - Step 2
    
    Links to Product and Component, defines material requirements.
    Has nested WorkOrders for manufacturing processes.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    factory_code = models.ForeignKey(
        FactoryCode,
        on_delete=models.CASCADE,
        related_name='raw_materials'
    )
    
    # Links
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='raw_materials',
        null=True,
        blank=True
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name='raw_materials',
        null=True,
        blank=True
    )
    
    # Material info
    product_name = models.CharField(max_length=255, blank=True, null=True)
    component_name = models.CharField(max_length=255, blank=True, null=True)
    material_description = models.CharField(max_length=500, blank=True, null=True)
    
    # Consumption
    net_consumption = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    unit = models.CharField(
        max_length=20,
        choices=UnitChoices.choices,
        blank=True,
        null=True
    )
    
    # Additional data
    specifications = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_raw_materials'
        ordering = ['factory_code', 'created_at']
    
    def __str__(self):
        return f"{self.factory_code.code} - {self.material_description or 'Material'}"


class WorkOrder(models.Model):
    """
    Work Order within Raw Material - Step 2
    
    Defines manufacturing processes (WEAVING, DYEING, CUTTING, etc.)
    Each raw material can have multiple work orders.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    raw_material = models.ForeignKey(
        RawMaterial,
        on_delete=models.CASCADE,
        related_name='work_orders'
    )
    
    # Work order type
    work_order = models.CharField(
        max_length=50,
        choices=WorkOrderTypeChoices.choices,
        blank=True,
        null=True
    )
    
    # Common fields
    wastage = models.CharField(max_length=50, blank=True, null=True)  # Percentage
    for_field = models.CharField(max_length=255, blank=True, null=True)  # FOR section
    for_section = models.CharField(max_length=255, blank=True, null=True)
    
    # Machine/Type specific
    machine_type = models.CharField(max_length=100, blank=True, null=True)
    quilting_type = models.CharField(max_length=100, blank=True, null=True)
    printing_type = models.CharField(max_length=100, blank=True, null=True)
    dyeing_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Design
    design = models.CharField(max_length=255, blank=True, null=True)
    
    # Image reference
    image_ref = models.FileField(upload_to='work_orders/images/', blank=True, null=True)
    
    # Approval
    approval_against = models.CharField(
        max_length=50,
        choices=ApprovalAgainstChoices.choices,
        blank=True,
        null=True
    )
    
    remarks = models.TextField(blank=True, null=True)
    
    # Process-specific data (JSONField for WEAVING, KNITTING, DYEING conditional fields)
    process_specific_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Stores process-specific fields:
        
        WEAVING: {
            "reed": "", "pick": "",
            "warp": true/false, "weft": true/false,
            "ratioWarp": "", "ratioWeft": "",
            "ratioWeightWarp": ""
        }
        
        KNITTING: {
            "wales": true/false, "courses": true/false,
            "ratioWales": "", "ratioCourses": "",
            "ratioWeightWales": ""
        }
        
        DYEING: {
            "receivedColorReference": "PANTONE/ARS/CSI/PMS",
            "referenceType": "TPG/TCX/COATED/UNCOAT",
            "shrinkageWidth": true/false, "shrinkageLength": true/false,
            "shrinkageWidthPercent": "", "shrinkageLengthPercent": "",
            "ratioWidth": "", "ratioLength": ""
        }
        
        TUFTING/CARPET: {
            "pileHeight": "", "tpi": ""
        }
        
        CUTTING: {
            "cutType": "LAYERED/PANEL", "cutSize": ""
        }
        """
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_work_orders'
        ordering = ['raw_material', 'created_at']
    
    def __str__(self):
        return f"{self.raw_material} - {self.work_order or 'Work Order'}"


# =============================================================================
# STEP 3: TRIMS & ACCESSORIES (CONSUMPTION MATERIALS)
# =============================================================================

class ConsumptionMaterial(models.Model):
    """
    Consumption Material (Trims & Accessories) - Step 3
    
    EXPANDED: 30 trim/accessory categories with conditional fields.
    Category-specific fields stored in category_specific_data JSONField.
    
    Common fields for ALL trim types:
    - testingRequirement, testingRequirementFile
    - lengthQuantity
    - surplus, surplusForSection
    - approval
    - remarks
    - unitAdditional (for width/length)
    
    Size object:
    - size.width, size.length, size.height, size.unit
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    factory_code = models.ForeignKey(
        FactoryCode,
        on_delete=models.CASCADE,
        related_name='consumption_materials'
    )
    
    # Links
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='consumption_materials',
        null=True,
        blank=True
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name='consumption_materials',
        null=True,
        blank=True
    )
    
    # Material info
    product_name = models.CharField(max_length=255, blank=True, null=True)
    component_name = models.CharField(max_length=255, blank=True, null=True)
    material_description = models.CharField(max_length=500, blank=True, null=True)
    
    # Consumption
    net_consumption = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    unit = models.CharField(
        max_length=20,
        choices=UnitChoices.choices,
        blank=True,
        null=True
    )
    unit_additional = models.CharField(max_length=20, blank=True, null=True)  # mm/in/cm
    
    # Trim/Accessory category
    trim_accessory = models.CharField(
        max_length=100,
        choices=TrimAccessoryChoices.choices,
        blank=True,
        null=True
    )
    
    # Size (nested object)
    size_width = models.CharField(max_length=50, blank=True, null=True)
    size_length = models.CharField(max_length=50, blank=True, null=True)
    size_height = models.CharField(max_length=50, blank=True, null=True)
    size_unit = models.CharField(
        max_length=10,
        choices=SizeUnitChoices.choices,
        blank=True,
        null=True
    )
    
    # Common fields for all trims
    testing_requirement = models.CharField(max_length=500, blank=True, null=True)
    testing_requirement_file = models.FileField(
        upload_to='consumption_materials/testing/',
        blank=True,
        null=True
    )
    length_quantity = models.CharField(max_length=255, blank=True, null=True)
    surplus = models.CharField(max_length=50, blank=True, null=True)  # Percentage
    surplus_for_section = models.CharField(max_length=255, blank=True, null=True)
    approval = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    # Work order
    work_order = models.CharField(
        max_length=50,
        choices=WorkOrderTypeChoices.choices,
        blank=True,
        null=True
    )
    
    # Category-specific data (JSONField)
    category_specific_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="See TRIM_CATEGORY_FIELDS_SCHEMA for structure"
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_consumption_materials'
        ordering = ['factory_code', 'created_at']
    
    def __str__(self):
        return f"{self.factory_code.code} - {self.trim_accessory or self.material_description or 'Material'}"


# =============================================================================
# STEP 4: ARTWORK & LABELING
# =============================================================================

class ArtworkMaterial(models.Model):
    """
    Artwork & Labeling Material - Step 4
    
    EXPANDED: 18 artwork categories with conditional fields.
    Category-specific fields stored in category_specific_data JSONField.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    factory_code = models.ForeignKey(
        FactoryCode,
        on_delete=models.CASCADE,
        related_name='artwork_materials'
    )
    
    # Component info
    components = models.CharField(max_length=255, blank=True, null=True)
    material_description = models.CharField(max_length=500, blank=True, null=True)
    
    # Consumption
    net_consumption = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    unit = models.CharField(
        max_length=20,
        choices=UnitChoices.choices,
        blank=True,
        null=True
    )
    
    # Placement
    placement = models.CharField(max_length=500, blank=True, null=True)
    
    # Work order
    work_order = models.CharField(
        max_length=50,
        choices=WorkOrderTypeChoices.choices,
        blank=True,
        null=True
    )
    
    # Artwork category
    artwork_category = models.CharField(
        max_length=100,
        choices=ArtworkCategoryChoices.choices,
        blank=True,
        null=True
    )
    
    # Size fields
    size_width = models.CharField(max_length=50, blank=True, null=True)
    size_length = models.CharField(max_length=50, blank=True, null=True)
    size_height = models.CharField(max_length=50, blank=True, null=True)
    size_unit = models.CharField(
        max_length=10,
        choices=SizeUnitChoices.choices,
        blank=True,
        null=True
    )
    size_artwork_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Common fields
    testing_requirement = models.CharField(max_length=500, blank=True, null=True)
    reference_image = models.FileField(
        upload_to='artwork_materials/references/',
        blank=True,
        null=True
    )
    length_quantity = models.CharField(max_length=255, blank=True, null=True)
    length_quantity_for_section = models.CharField(max_length=255, blank=True, null=True)
    surplus = models.CharField(max_length=50, blank=True, null=True)
    surplus_for_section = models.CharField(max_length=255, blank=True, null=True)
    approval = models.CharField(
        max_length=20,
        choices=ApprovalChoices.choices,
        blank=True,
        null=True
    )
    remarks = models.TextField(blank=True, null=True)
    
    # Specific type (common across many categories)
    specific_type = models.CharField(max_length=255, blank=True, null=True)
    material = models.CharField(max_length=255, blank=True, null=True)
    colours = models.CharField(max_length=255, blank=True, null=True)
    finishing = models.CharField(max_length=255, blank=True, null=True)
    permanence = models.CharField(max_length=255, blank=True, null=True)
    permanence_file = models.FileField(
        upload_to='artwork_materials/permanence/',
        blank=True,
        null=True
    )
    
    # Category-specific data (JSONField)
    category_specific_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="See ARTWORK_CATEGORY_FIELDS_SCHEMA for structure"
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_artwork_materials'
        ordering = ['factory_code', 'created_at']
    
    def __str__(self):
        return f"{self.factory_code.code} - {self.artwork_category or self.material_description or 'Artwork'}"


# =============================================================================
# STEP 5: PACKAGING
# =============================================================================

class Packaging(models.Model):
    """
    Packaging Configuration - Step 5 Header
    
    Main packaging settings for a factory code.
    Has nested PackagingMaterial items.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    factory_code = models.OneToOneField(
        FactoryCode,
        on_delete=models.CASCADE,
        related_name='packaging'
    )
    
    # Header configuration
    product_selection = models.CharField(max_length=500, blank=True, null=True)
    packaging_type = models.CharField(
        max_length=50,
        choices=PackagingTypeChoices.choices,
        default=PackagingTypeChoices.STANDARD
    )
    casepack_qty = models.PositiveIntegerField(null=True, blank=True)
    assorted_sku_link = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_packaging'
    
    def __str__(self):
        return f"{self.factory_code.code} - Packaging"


class PackagingMaterial(models.Model):
    """
    Packaging Material - Step 5 Materials
    
    EXPANDED: 8 packaging material types with conditional fields.
    Material-specific fields stored in material_specific_data JSONField.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    packaging = models.ForeignKey(
        Packaging,
        on_delete=models.CASCADE,
        related_name='materials'
    )
    
    # Basic info
    components = models.CharField(max_length=255, blank=True, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)  # Material description
    net_consumption_per_pc = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    unit = models.CharField(
        max_length=20,
        choices=UnitChoices.choices,
        blank=True,
        null=True
    )
    
    # Work order
    work_order = models.CharField(max_length=100, blank=True, null=True)
    
    # Placement
    placement = models.CharField(max_length=500, blank=True, null=True)
    
    # Size
    size_width = models.CharField(max_length=50, blank=True, null=True)
    size_length = models.CharField(max_length=50, blank=True, null=True)
    size_height = models.CharField(max_length=50, blank=True, null=True)
    size_unit = models.CharField(
        max_length=10,
        choices=SizeUnitChoices.choices,
        blank=True,
        null=True
    )
    
    # Packaging material type
    packaging_material_type = models.CharField(
        max_length=100,
        choices=PackagingMaterialTypeChoices.choices,
        blank=True,
        null=True
    )
    
    # Common fields
    surplus = models.CharField(max_length=50, blank=True, null=True)
    surplus_for_section = models.CharField(max_length=255, blank=True, null=True)
    approval_against = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    # Type-specific fields (kept as columns for common use)
    no_of_plys = models.CharField(max_length=50, blank=True, null=True)  # CARTONS
    joint_type = models.CharField(max_length=100, blank=True, null=True)  # CARTONS
    bursting_strength = models.CharField(max_length=100, blank=True, null=True)  # CARTONS
    guage = models.CharField(max_length=50, blank=True, null=True)  # POLY BAG, TAPE
    printing_ref = models.FileField(
        upload_to='packaging_materials/printing/',
        blank=True,
        null=True
    )
    gumming_quality = models.CharField(max_length=100, blank=True, null=True)  # POLY BAG, TAPE
    punch_holes = models.CharField(max_length=100, blank=True, null=True)  # POLY BAG WITH FLAP
    flap_size = models.CharField(max_length=50, blank=True, null=True)  # POLY BAG WITH FLAP
    guage_gsm = models.CharField(max_length=50, blank=True, null=True)  # POLYSHEET, BALE WRAP
    roll_width = models.CharField(max_length=50, blank=True, null=True)  # POLYSHEET, BALE WRAP
    roll_width_unit = models.CharField(max_length=20, blank=True, null=True)
    tape_width = models.CharField(max_length=50, blank=True, null=True)  # TAPE
    tape_width_unit = models.CharField(max_length=20, blank=True, null=True)
    
    # Material-specific data (JSONField for any additional fields)
    material_specific_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="See PACKAGING_MATERIAL_FIELDS_SCHEMA for structure"
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_packaging_materials'
        ordering = ['packaging', 'created_at']
    
    def __str__(self):
        return f"{self.packaging.factory_code.code} - {self.packaging_material_type or self.product or 'Material'}"


class PackagingWorkOrder(models.Model):
    """
    Work Order for Packaging Material - Step 5
    
    Each packaging material can have work orders.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    packaging_material = models.ForeignKey(
        PackagingMaterial,
        on_delete=models.CASCADE,
        related_name='work_orders'
    )
    
    work_order = models.CharField(max_length=100, blank=True, null=True)
    
    # Additional work order data
    work_order_data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'factory_code_packaging_work_orders'
    
    def __str__(self):
        return f"{self.packaging_material} - {self.work_order or 'Work Order'}"


# =============================================================================
# JSON FIELD SCHEMAS (For Documentation & Validation)
# =============================================================================

TRIM_CATEGORY_FIELDS_SCHEMA = {
    "ZIPPERS": {
        "fields": [
            "zipNumber", "zipType", "brand", "teeth", "puller",
            "pullerType", "length"
        ],
        "options": {
            "zipType": ["Concealed", "Open", "Closed-End"],
            "brand": ["YKK", "RIRI", "SBS"],
            "teeth": ["Coil", "Plastic", "Metal"],
            "pullerType": ["Lockable", "Non-Lockable"]
        }
    },
    "VELCRO": {
        "fields": [
            "velcroType", "velcroMaterial", "width", "colour",
            "hookDensityLoopType", "cycleLife", "attachmentMethod"
        ],
        "options": {
            "velcroType": ["Sew-on", "Adhesive", "Die-Cut", "ONE-WRAP"],
            "velcroMaterial": ["Nylon", "Polyester"]
        }
    },
    "STITCHING THREAD": {
        "fields": [
            "threadType", "fibreContent", "countTicketNo", "ply",
            "colour", "threadFinish", "usage"
        ],
        "options": {
            "threadType": ["Spun Polyester", "Cotton", "Core Spun"],
            "threadFinish": ["Bonded", "Lubricated", "Matte"]
        }
    },
    "BUTTONS": {
        "fields": [
            "buttonType", "buttonMaterial", "sizeLigne", "finishColour",
            "buttonAttachmentMethod", "function"
        ],
        "options": {
            "buttonType": ["Sewing", "Snap", "Tack"],
            "buttonMaterial": ["Polyester", "Metal", "Natural"],
            "sizeLigne": ["14L", "16L", "20L", "24L"]
        }
    },
    "RIVETS": {
        "fields": [
            "rivetType", "rivetMaterial", "capSize", "postHeightLength",
            "finishPlating", "pullerStrength", "rivetPullerType"
        ],
        "options": {
            "rivetType": ["Open-End", "Close-End", "Blind"],
            "rivetMaterial": ["Brass", "Copper", "Zinc", "Steel"],
            "capSize": ["8mm", "9mm", "10mm"]
        }
    },
    "NIWAR (Webbing/Tapes)": {
        "fields": [
            "niwarType", "niwarMaterial", "niwarWidth", "niwarThickness",
            "niwarColour", "finishCoating", "tensileStrength"
        ],
        "options": {
            "niwarType": ["Woven", "Knitted"]
        }
    },
    "LACE": {
        "fields": [
            "laceType", "laceMaterial", "laceWidth", "laceColour",
            "laceFinishing", "laceUsage", "designReference"
        ],
        "options": {
            "laceType": ["Woven", "Braided", "Crochet", "Knit"]
        }
    },
    "INTERLINING/FUSING": {
        "fields": [
            "interliningType", "interliningMaterial", "gsmWeight",
            "adhesive", "interliningColour", "fusingSpec"
        ],
        "options": {
            "interliningType": ["Woven", "Non-woven", "Knitted", "Fusible"],
            "adhesive": ["PA", "PES", "EVA"]
        }
    },
    "HOOKS & EYES": {
        "fields": [
            "hookEyeType", "hookEyeMaterial", "hookEyeSize", "hookEyeColour",
            "hookEyeFinish", "strength", "application"
        ],
        "options": {
            "hookEyeMaterial": ["Brass", "Steel", "Nickel"],
            "hookEyeSize": ["#1", "#2", "#3"]
        }
    },
    "BUCKLES & ADJUSTERS": {
        "fields": [
            "buckleType", "buckleMaterial", "buckleSize", "buckleFinishColour",
            "buckleFunction", "buckleTensileStrength"
        ],
        "options": {
            "buckleType": ["Side Release", "Center Bar", "Ladder Lock"],
            "buckleMaterial": ["Plastic", "Metal", "Nylon"]
        }
    },
    "EYELETS & GROMMETS": {
        "fields": [
            "eyeletType", "eyeletMaterial", "innerDiameter", "outerDiameter",
            "eyeletColour", "eyeletApplication", "tooling"
        ]
    },
    "ELASTIC": {
        "fields": [
            "elasticType", "elasticMaterial", "elasticWidth", "elasticColour",
            "stretchTension", "elasticPacking"
        ],
        "options": {
            "elasticType": ["Woven", "Braided", "Knitted"],
            "elasticMaterial": ["Rubber", "Spandex", "Latex"]
        }
    },
    "FELT": {
        "fields": [
            "feltType", "feltMaterial", "feltThickness", "densityGsm",
            "feltColour", "feltFinishForm", "feltApplication"
        ],
        "options": {
            "feltType": ["Wool", "Synthetic", "Blended"],
            "feltThickness": ["2mm", "3mm", "5mm"]
        }
    },
    "SHOULDER PADS / CUPS": {
        "fields": [
            "shoulderPadType", "shoulderPadMaterial", "shoulderPadSize",
            "shape", "covering", "shoulderPadAttachment", "weight"
        ],
        "options": {
            "shoulderPadMaterial": ["Polyurethane", "Polyester", "Cotton"]
        }
    },
    "TUBULAR KNITS / RIBBING": {
        "fields": [
            "tubularType", "tubularMaterial", "widthDiameter", "weightDensity",
            "tubularColour", "stretchPercent", "cutting"
        ],
        "options": {
            "tubularType": ["1x1 Rib", "2x2 Rib", "Interlock", "Jersey"]
        }
    },
    "RFID / EAS TAGS": {
        "fields": [
            "rfidType", "formFactor", "frequency", "chipIcType",
            "rfidSize", "coding", "security"
        ],
        "options": {
            "rfidType": ["UHF RFID", "HF RFID", "LF RFID", "EAS Tag"],
            "formFactor": ["Label", "Sticker", "Hard Tag", "Inlay"]
        }
    },
    "PLASTIC CABLE TIES / LOOPS": {
        "fields": [
            "cableTieType", "cableTieMaterial", "cableTieSize", "cableTieColour",
            "cableTieTensileStrength", "cableTieFinish", "cableTieUsage"
        ],
        "options": {
            "cableTieType": ["Standard", "Releasable", "Beaded", "Loop"],
            "cableTieMaterial": ["Nylon 6/6", "Polypropylene", "Stainless Steel"]
        }
    },
    "FRINGE / TASSELS": {
        "fields": [
            "fringeType", "fringeMaterial", "dropLength", "tapeWidth",
            "fringeColour", "fringeFinish", "construction"
        ],
        "options": {
            "fringeType": ["Fringe", "Tassel", "Pom-pom", "Bullion"],
            "fringeMaterial": ["Cotton", "Polyester", "Rayon", "Wool", "Blend"]
        }
    },
    "PLASTIC PIPES / RODS": {
        "fields": [
            "pipeType", "pipeMaterial", "diameterDimensions", "pipeLength",
            "pipeColour", "endCaps", "flexibility", "pipeUsage"
        ],
        "options": {
            "pipeType": ["Round Pipe", "Square Rod", "Flat Bar", "Custom Shape"],
            "pipeMaterial": ["PVC", "Polypropylene", "Nylon", "ABS", "Polyethylene"],
            "flexibility": ["Rigid", "Semi-flexible", "Flexible"]
        }
    },
    "SEAM SEALING TAPE": {
        "fields": [
            "seamTapeType", "seamTapeMaterial", "seamTapeWidth", "seamTapeColour",
            "seamTapeAdhesiveType", "applicationSpec", "elasticity"
        ],
        "options": {
            "seamTapeType": ["PU Tape", "TPU Tape", "Hot Melt"],
            "seamTapeAdhesiveType": ["Hot Melt", "Pressure Sensitive", "Heat Activated"]
        }
    },
    "ADHESIVES / GUNNING": {
        "fields": [
            "adhesiveType", "materialBase", "adhesiveApplication", "viscosity",
            "settingTime", "adhesiveColour", "applicator"
        ],
        "options": {
            "adhesiveType": ["Hot Melt", "Contact Adhesive", "Spray Adhesive"],
            "materialBase": ["EVA", "PU", "Polyamide", "Acrylic", "Rubber-based"]
        }
    },
    "PRE-CUT HEMS / BINDINGS": {
        "fields": [
            "hemType", "hemMaterial", "cutType", "hemWidth",
            "foldType", "hemColour", "hemPackaging"
        ],
        "options": {
            "hemType": ["Bias Binding", "Straight Cut", "Curved Hem"],
            "cutType": ["Straight", "Bias (45°)", "Curved"],
            "foldType": ["Single fold", "Double fold", "Unfolded"]
        }
    },
    "REFLECTIVE TAPES / TRIMS": {
        "fields": [
            "reflectiveType", "reflectiveMaterial", "reflectiveWidth",
            "reflectiveColour", "certification", "baseFabric"
        ],
        "options": {
            "reflectiveType": ["Glass Bead", "Prismatic", "Microprismatic"],
            "certification": ["EN ISO 20471", "ANSI/ISEA 107", "CSA Z96"]
        }
    },
    "FIRE RETARDANT (FR) TRIMS": {
        "fields": [
            "frType", "frMaterial", "complianceLevel", "frColour",
            "durability", "frComponents"
        ],
        "options": {
            "frMaterial": ["Nomex", "Kevlar", "FR Cotton", "FR Polyester"],
            "complianceLevel": ["NFPA 701", "EN 11612", "ASTM D6413", "CPAI-84"]
        }
    },
    "REPAIR KITS / PATCHES": {
        "fields": [
            "repairKitType", "repairKitMaterial", "sizeShape", "repairKitColour",
            "repairKitPackaging", "userApplication", "contents"
        ],
        "options": {
            "repairKitType": ["Patch Kit", "Repair Tape", "Adhesive Patch"],
            "userApplication": ["Heat press", "Iron-on", "Adhesive", "Sew-on"]
        }
    },
    "CORD STOPS / CORD LOCKS / TOGGLES": {
        "fields": [
            "cordStopType", "cordStopMaterial", "cordStopSize", "cordStopColour",
            "lockingMechanism", "cordStopFunction"
        ],
        "options": {
            "cordStopType": ["Cord Stop", "Cord Lock", "Toggle", "Spring Lock"],
            "cordStopMaterial": ["Nylon", "Acetal", "POM", "Plastic"],
            "lockingMechanism": ["Spring-loaded", "Friction", "Cam lock", "Push-pull"]
        }
    },
    "D-RINGS / O-RINGS / WEBBING LOOPS": {
        "fields": [
            "dRingType", "dRingMaterial", "dRingSize", "thicknessGauge",
            "dRingFinishPlating", "loadRating", "dRingApplication"
        ],
        "options": {
            "dRingType": ["D-Ring", "O-Ring", "Webbing Loop", "Triangle Ring"],
            "dRingMaterial": ["Steel", "Stainless Steel", "Brass", "Aluminium", "Plastic"]
        }
    },
    "FOAM / WADDING (Pre-Cut Shapes)": {
        "fields": [
            "foamType", "foamDensity", "foamThickness", "shapeId",
            "foamColour", "properties", "foamAttachment"
        ],
        "options": {
            "foamType": ["Polyurethane", "Polyethylene", "EVA", "Memory Foam"],
            "foamAttachment": ["Adhesive-backed", "Sewn-in", "Velcro", "Snap-on"]
        }
    },
    "PINS / TAGGING BARBS": {
        "fields": [
            "pinType", "pinMaterial", "pinSize", "pinColour",
            "pinTensileStrength", "headType", "pinApplication"
        ],
        "options": {
            "pinType": ["Tagging Pin", "Safety Pin", "T-Pin", "U-Pin"],
            "pinMaterial": ["Stainless Steel", "Nickel-plated", "Brass", "Plastic"],
            "headType": ["Round head", "Flat head", "Ball head", "T-head"]
        }
    },
    "MAGNETIC CLOSURES / SNAPS": {
        "fields": [
            "magneticType", "magneticMaterial", "magneticSize", "magneticStrength",
            "polarity", "magneticApplication"
        ],
        "options": {
            "magneticType": ["Magnetic Snap", "Magnetic Button", "Magnetic Closure"],
            "magneticMaterial": ["Neodymium", "Ferrite", "Samarium Cobalt", "Plastic housing"]
        }
    }
}

ARTWORK_CATEGORY_FIELDS_SCHEMA = {
    "LABELS (BRAND/MAIN)": {
        "fields": [
            "specificType", "material", "sizeArtworkId", "foldType",
            "colours", "finishing", "placement"
        ],
        "options": {
            "specificType": ["Woven (Damask, Taffeta, Satin)", "Printed (Satin, Cotton)", "Heat Transfer", "Leather", "Metal"],
            "foldType": ["End-fold", "Center-fold", "Miter-fold", "Straight Cut"]
        }
    },
    "CARE & COMPOSITION": {
        "fields": [
            "specificType", "material", "countryOfOrigin", "manufacturerId",
            "symbol", "language", "permanence"
        ],
        "options": {
            "specificType": ["Woven", "Printed", "Heat Transfer"]
        }
    },
    "TAGS & SPECIAL LABELS": {
        "fields": [
            "specificType", "material", "sizeArtworkId", "attachment",
            "content", "finishing", "placement"
        ],
        "options": {
            "specificType": ["Hang Tag (Paper/Card)", "Price Tag", "Size Label", "Flag"]
        }
    },
    "FLAMMABILITY / SAFETY LABELS": {
        "fields": [
            "specificType", "content", "symbol", "certificationId",
            "language", "placement"
        ],
        "options": {
            "specificType": ["Permanent Sew-in Label", "Removable Hang Tag"]
        }
    },
    "RFID / SECURITY TAGS": {
        "fields": [
            "specificType", "formFactor", "chipFrequency", "coding",
            "adhesive", "security", "sizeArtworkId"
        ],
        "options": {
            "specificType": ["Soft EAS Label", "UHF RFID Sticker", "Hard Tag"],
            "formFactor": ["Adhesive Label", "Integrated Woven Label"]
        }
    },
    "LAW LABEL / CONTENTS TAG": {
        "fields": [
            "lawLabelType", "lawLabelMaterial", "fillingMaterials",
            "newUsedStatus", "registrationLicenses", "permanence",
            "permanenceFile", "testingRequirement", "lengthQuantity",
            "lengthQuantityForSection", "surplus"
        ]
    },
    "HANG TAG SEALS / STRINGS": {
        "fields": [
            "hangTagType", "hangTagMaterial", "sealShape", "fastening",
            "preStringing", "application", "colours", "sizeArtworkId"
        ]
    },
    "PRICE TICKET / BARCODE TAG": {
        "fields": [
            "priceTicketType", "priceTicketMaterial", "content",
            "barcodeType", "adhesive", "finishing", "sizeArtworkId"
        ],
        "options": {
            "priceTicketType": ["Adhesive Sticker", "Printed Area", "Dedicated Small Tag"]
        }
    },
    "HEAT TRANSFER LABELS": {
        "fields": [
            "heatTransferType", "heatTransferMaterialBase", "applicationSpec",
            "colours", "finishHandFeel", "placement", "sizeArtworkId"
        ],
        "options": {
            "heatTransferType": ["Brand Logo", "Size Tag", "Minimal Care", "Instructions", "Reflective"]
        }
    },
    "UPC LABEL / BARCODE STICKER": {
        "fields": [
            "upcType", "upcMaterial", "content", "quality",
            "adhesive", "placement", "sizeArtworkId"
        ],
        "options": {
            "upcType": ["Adhesive Sticker", "Pre-Printed Barcode Area"]
        }
    },
    "SIZE LABELS (INDIVIDUAL)": {
        "fields": [
            "sizeLabelType", "sizeLabelMaterial", "finishing",
            "colours", "placement", "permanence", "sizeArtworkId"
        ],
        "options": {
            "sizeLabelType": ["Woven Flag Label", "Printed Flag Label", "Heat Transfer", "Small Sticker"]
        }
    },
    "ANTI-COUNTERFEIT & HOLOGRAMS": {
        "fields": [
            "antiCounterfeitType", "antiCounterfeitMaterial", "securityFeature",
            "application", "placement", "verification", "sizeArtworkId"
        ],
        "options": {
            "antiCounterfeitType": ["Hologram Sticker", "Void/Tamper-Evident Label", "Authenticity Patch", "Invisible Ink Print"]
        }
    },
    "QC / INSPECTION LABELS": {
        "fields": [
            "qcLabelType", "qcLabelMaterial", "content",
            "application", "removal", "traceability", "sizeArtworkId"
        ],
        "options": {
            "qcLabelType": ["Passed/Inspected Sticker", "Hold/Defective Sticker", "Audit Sample Tag"]
        }
    },
    "BELLY BAND / WRAPPER": {
        "fields": [
            "bellyBandType", "bellyBandMaterial", "closure",
            "content", "closureFinish", "durability", "sizeArtworkId"
        ],
        "options": {
            "bellyBandType": ["Cardboard Sleeve", "Printed Paper Band", "Plastic Film Wrapper"]
        }
    },
    "TYVEK LABELS": {
        "fields": [
            "tyvekType", "tyvekMaterial", "content",
            "inkType", "durability", "permanence", "sizeArtworkId"
        ],
        "options": {
            "tyvekType": ["Law Label", "Shipping Tag", "Permanent Industrial/Outdoor Care Label"]
        }
    },
    "TAFFETA LABELS": {
        "fields": [
            "taffetaType", "taffetaMaterial", "content",
            "printQuality", "durability", "finishing", "sizeArtworkId"
        ],
        "options": {
            "taffetaType": ["Printed Care Label", "Composition Label", "Temporary Size Label"]
        }
    },
    "INSERT CARDS": {
        "fields": [
            "specificType", "material", "sizeShape", "content",
            "finishing", "permanence"
        ],
        "options": {
            "specificType": ["Shirt Board", "Neck Support", "Tissue Paper Insert", "Promotional Insert Card"]
        }
    },
    "RIBBONS": {
        "fields": [
            "specificType", "material", "ribbonWidth", "colours",
            "finishing", "usage"
        ],
        "options": {
            "specificType": ["Satin", "Grosgrain", "Sheer Organza", "Printed Polyester", "Woven Edge"]
        }
    }
}

PACKAGING_MATERIAL_FIELDS_SCHEMA = {
    "CARTONS/CORRUGATED BOX": {
        "fields": ["noOfPlys", "jointType", "burstingStrength"],
        "placeholders": {
            "noOfPlys": "5 PLY/7 PLY",
            "jointType": "STAPLE/BINDED",
            "burstingStrength": "175 LBS"
        }
    },
    "POLY BAG WITH FLAP": {
        "fields": ["guage", "gummingQuality", "punchHoles", "printingRef"],
        "placeholders": {
            "guage": "200",
            "gummingQuality": "High/Standard",
            "punchHoles": "e.g., 2 holes"
        }
    },
    "POLYSHEET": {
        "fields": ["guageGsm", "rollWidth", "rollWidthUnit"],
        "placeholders": {
            "guageGsm": "200",
            "rollWidth": "60"
        }
    },
    "BALE WRAP": {
        "fields": ["guageGsm", "rollWidth", "rollWidthUnit"],
        "placeholders": {
            "guageGsm": "200",
            "rollWidth": "60"
        }
    },
    "TAPE": {
        "fields": ["guage", "gummingQuality", "tapeWidth", "tapeWidthUnit", "printingRef"],
        "placeholders": {
            "guage": "200",
            "gummingQuality": "Strong/Standard",
            "tapeWidth": "3"
        }
    }
}


# =============================================================================
# INTERNAL PURCHASE ORDER (IPO) MODEL
# =============================================================================

class InternalPurchaseOrder(models.Model):
    """
    Internal Purchase Order (IPO) Model
    Auto-generates IPO codes like: CHD/PD/101A/PROGRAM1/1
    """
    ORDER_TYPE_CHOICES = [
        ('STOCK', 'Stock'),
        ('SAM', 'Sample'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ipo_code = models.CharField(max_length=100, unique=True, db_index=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='STOCK')
    buyer_code = models.ForeignKey(
        'BuyerCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ipos'
    )
    buyer_code_text = models.CharField(max_length=50, blank=True, default='')
    company_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, null=True, blank=True)
    program_name = models.CharField(max_length=255)
    po_sr_no = models.IntegerField(default=1)

    # Tenant & Audit
    tenant = models.ForeignKey(
        'auth_service.Tenant',
        on_delete=models.CASCADE,
        related_name='ipos',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        'auth_service.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_ipos'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'internal_purchase_orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'program_name']),
            models.Index(fields=['ipo_code']),
        ]

    def __str__(self):
        return self.ipo_code

    @classmethod
    def get_next_sr_no(cls, program_name, tenant=None):
        """Get next sequential SR number for a given program."""
        qs = cls.objects.filter(program_name__iexact=program_name)
        if tenant:
            qs = qs.filter(tenant=tenant)
        last_sr = qs.aggregate(Max('po_sr_no'))['po_sr_no__max']
        return (last_sr or 0) + 1

    def save(self, *args, **kwargs):
        if not self.ipo_code:
            location = 'CHD'
            dept = 'PD'
            buyer = self.buyer_code_text or (self.buyer_code.code if self.buyer_code else '000')
            program = self.program_name.upper().replace(' ', '')
            sr = self.po_sr_no
            self.ipo_code = f"{location}/{dept}/{buyer}/{program}/{sr}"
        super().save(*args, **kwargs)


# =============================================================================
# PURCHASE ORDER MODEL
# =============================================================================

class PurchaseOrder(models.Model):
    """
    Purchase Order Model
    Auto-generates PO codes like: PO1001, PO1002, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po_code = models.CharField(max_length=50, unique=True, db_index=True)
    order_date = models.DateField()
    order_time = models.TimeField()
    factory_po_number = models.CharField(max_length=100, blank=True, default='')
    buyer = models.ForeignKey(
        'BuyerCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_orders'
    )
    vendor = models.ForeignKey(
        'VendorCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_orders'
    )
    product_category = models.CharField(max_length=100, blank=True, default='')
    category_code = models.CharField(max_length=50, blank=True, default='')
    po_description = models.TextField(blank=True, default='')
    particulars = models.TextField(blank=True, default='')
    quantity = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    unit_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    delivery_date = models.DateField(null=True, blank=True)
    payment_terms = models.TextField(blank=True, default='')
    remarks = models.TextField(blank=True, default='')
    last_po_number = models.CharField(max_length=100, blank=True, default='')

    # Tenant & Audit
    tenant = models.ForeignKey(
        'auth_service.Tenant',
        on_delete=models.CASCADE,
        related_name='purchase_orders',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        'auth_service.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_purchase_orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchase_orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['po_code']),
        ]

    def __str__(self):
        return self.po_code

    @classmethod
    def generate_next_code(cls, tenant=None):
        """Generate next sequential PO code (PO1001, PO1002, ...)."""
        qs = cls.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        last = qs.order_by('-created_at').first()
        if last and last.po_code.startswith('PO'):
            try:
                last_num = int(last.po_code.replace('PO', ''))
                return f"PO{last_num + 1}"
            except ValueError:
                pass
        return "PO1001"

    def save(self, *args, **kwargs):
        if not self.po_code:
            self.po_code = self.generate_next_code(tenant=self.tenant)
        super().save(*args, **kwargs)


# =============================================================================
# COMPANY ESSENTIAL MODEL (Unified for 12 categories)
# =============================================================================

class CompanyEssential(models.Model):
    """
    Company Essential Model - Unified model for 12 categories:
    Stationary, Pantry, Machinery, Housekeeping, Electricals, Hardware & Chemicals,
    Audit & Compliance, IT, QC Tools, Travel & Expense, Repair, Maintenance
    
    Auto-generates codes like: CHD/E/STATIONARY/26-27/PO-1
    """
    CATEGORY_CHOICES = [
        ('STATIONARY', 'Stationary'),
        ('PANTRY', 'Pantry'),
        ('MACHINERY', 'Machinery'),
        ('HOUSEKEEPING', 'Housekeeping'),
        ('ELECTRICALS', 'Electricals'),
        ('HARDWARE_CHEMICALS', 'Hardware & Chemicals'),
        ('AUDIT_COMPLIANCE', 'Audit & Compliance'),
        ('IT', 'IT'),
        ('QC_TOOLS', 'QC Tools'),
        ('TRAVEL_EXPENSE', 'Travel & Expense'),
        ('REPAIR', 'Repair'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    code = models.CharField(max_length=100, db_index=True)
    entry_date = models.DateField()
    department = models.CharField(max_length=100, blank=True, default='')
    sr_no = models.IntegerField(default=1)

    # Flexible fields (different categories use different subsets)
    item_description = models.TextField(blank=True, null=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    machine_type = models.CharField(max_length=100, blank=True, null=True)
    component_spec = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    for_field = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    reference_image = models.FileField(upload_to='company_essentials/', blank=True, null=True)

    # Tenant & Audit
    tenant = models.ForeignKey(
        'auth_service.Tenant',
        on_delete=models.CASCADE,
        related_name='company_essentials',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        'auth_service.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_company_essentials'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_essentials'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'tenant']),
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.category} - {self.code}"

    @classmethod
    def get_next_po_number(cls, category, tenant=None):
        """Get next PO number for a given category."""
        qs = cls.objects.filter(category=category)
        if tenant:
            qs = qs.filter(tenant=tenant)
        last_sr = qs.aggregate(Max('sr_no'))['sr_no__max']
        return (last_sr or 0) + 1

    def save(self, *args, **kwargs):
        if not self.code:
            year = self.entry_date.strftime('%y') if self.entry_date else timezone.now().strftime('%y')
            next_year = str(int(year) + 1).zfill(2)
            po_num = self.get_next_po_number(self.category, self.tenant)
            self.sr_no = po_num
            self.code = f"CHD/E/{self.category}/{year}-{next_year}/PO-{po_num}"
        super().save(*args, **kwargs)