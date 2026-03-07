# from django.contrib import admin
# from unfold.admin import ModelAdmin
# from .models import Department, Segment, BuyerCode, VendorCode


# @admin.register(Department)
# class DepartmentAdmin(ModelAdmin):
#     """Admin interface for Department model"""
    
#     list_display = ['name', 'code', 'display_order', 'is_active', 'segments_count', 'tenant', 'created_at']
#     list_filter = ['is_active', 'tenant', 'created_at']
#     search_fields = ['name', 'code', 'description']
#     ordering = ['display_order', 'name']
#     readonly_fields = ['id', 'created_at', 'updated_at']
    
#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('id', 'code', 'name', 'description', 'display_order')
#         }),
#         ('Status', {
#             'fields': ('is_active',)
#         }),
#         ('Relationships', {
#             'fields': ('tenant', 'created_by')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def segments_count(self, obj):
#         """Display count of segments"""
#         return obj.segments.count()
#     segments_count.short_description = 'Segments'
    
#     def get_queryset(self, request):
#         """Optimize queryset"""
#         qs = super().get_queryset(request)
#         return qs.prefetch_related('segments').select_related('tenant', 'created_by')


# @admin.register(Segment)
# class SegmentAdmin(ModelAdmin):
#     """Admin interface for Segment model"""
    
#     list_display = ['name', 'code', 'department', 'display_order', 'is_active', 'created_at']
#     list_filter = ['is_active', 'department', 'created_at']
#     search_fields = ['name', 'code', 'description', 'department__name']
#     ordering = ['department', 'display_order', 'name']
#     readonly_fields = ['id', 'created_at', 'updated_at']
    
#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('id', 'code', 'name', 'description', 'display_order')
#         }),
#         ('Relationships', {
#             'fields': ('department', 'created_by')
#         }),
#         ('Status', {
#             'fields': ('is_active',)
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def get_queryset(self, request):
#         """Optimize queryset"""
#         qs = super().get_queryset(request)
#         return qs.select_related('department', 'department__tenant', 'created_by')


# @admin.register(BuyerCode)
# class BuyerCodeAdmin(ModelAdmin):
#     """Admin interface for BuyerCode model"""
    
#     list_display = ['code', 'buyer_name', 'retailer', 'contact_person', 'tenant', 'created_at']
#     list_filter = ['tenant', 'created_at']
#     search_fields = ['code', 'buyer_name', 'retailer', 'contact_person', 'buyer_address']
#     ordering = ['-created_at']
#     readonly_fields = ['id', 'code', 'created_at', 'updated_at']
    
#     fieldsets = (
#         ('Code Information', {
#             'fields': ('id', 'code')
#         }),
#         ('Buyer Information', {
#             'fields': ('buyer_name', 'buyer_address', 'contact_person', 'retailer')
#         }),
#         ('Relationships', {
#             'fields': ('tenant', 'created_by')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def get_queryset(self, request):
#         """Optimize queryset"""
#         qs = super().get_queryset(request)
#         return qs.select_related('tenant', 'created_by')
    
#     def has_change_permission(self, request, obj=None):
#         """Allow editing buyer information but not the code"""
#         return True
    
#     def has_delete_permission(self, request, obj=None):
#         """Allow deletion"""
#         return True


# @admin.register(VendorCode)
# class VendorCodeAdmin(ModelAdmin):
#     """Admin interface for VendorCode model"""
    
#     list_display = ['code', 'vendor_name', 'gst', 'job_work_category', 'contact_person', 'email', 'tenant', 'created_at']
#     list_filter = ['tenant', 'job_work_category', 'created_at']
#     search_fields = ['code', 'vendor_name', 'gst', 'email', 'contact_person', 'job_work_category', 'address']
#     ordering = ['-created_at']
#     readonly_fields = ['id', 'code', 'created_at', 'updated_at']
    
#     fieldsets = (
#         ('Code Information', {
#             'fields': ('id', 'code')
#         }),
#         ('Vendor Information', {
#             'fields': ('vendor_name', 'address', 'gst', 'contact_person', 'email', 'whatsapp_number', 'alt_whatsapp_number')
#         }),
#         ('Banking Details', {
#             'fields': ('bank_name', 'account_number', 'ifsc_code')
#         }),
#         ('Job Work Details', {
#             'fields': ('job_work_category', 'job_work_sub_category')
#         }),
#         ('Payment Terms', {
#             'fields': ('payment_terms',)
#         }),
#         ('Relationships', {
#             'fields': ('tenant', 'created_by')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def get_queryset(self, request):
#         """Optimize queryset"""
#         qs = super().get_queryset(request)
#         return qs.select_related('tenant', 'created_by')
    
#     def has_change_permission(self, request, obj=None):
#         """Allow editing vendor information but not the code"""
#         return True
    
#     def has_delete_permission(self, request, obj=None):
#         """Allow deletion"""
#         return True


from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from django.utils.html import format_html
import json

from .models import (
    # Existing models
    Department, Segment, BuyerCode, VendorCode,
    # Factory Code models
    FactoryCode, Product, Component, RawMaterial, WorkOrder,
    ConsumptionMaterial, ArtworkMaterial, Packaging, PackagingMaterial,
    PackagingWorkOrder
)


# =============================================================================
# EXISTING ADMINS (Department, Segment, BuyerCode, VendorCode)
# =============================================================================

@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    """Admin interface for Department model"""
    
    list_display = ['name', 'code', 'display_order', 'is_active', 'segments_count', 'tenant', 'created_at']
    list_filter = ['is_active', 'tenant', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['display_order', 'name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'code', 'name', 'description', 'display_order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Relationships', {
            'fields': ('tenant', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def segments_count(self, obj):
        """Display count of segments"""
        return obj.segments.count()
    segments_count.short_description = 'Segments'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('segments').select_related('tenant', 'created_by')


@admin.register(Segment)
class SegmentAdmin(ModelAdmin):
    """Admin interface for Segment model"""
    
    list_display = ['name', 'code', 'department', 'display_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'department', 'created_at']
    search_fields = ['name', 'code', 'description', 'department__name']
    ordering = ['department', 'display_order', 'name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'code', 'name', 'description', 'display_order')
        }),
        ('Relationships', {
            'fields': ('department', 'created_by')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('department', 'department__tenant', 'created_by')


@admin.register(BuyerCode)
class BuyerCodeAdmin(ModelAdmin):
    """Admin interface for BuyerCode model"""
    
    list_display = ['code', 'buyer_name', 'retailer', 'contact_person', 'tenant', 'created_at']
    list_filter = ['tenant', 'created_at']
    search_fields = ['code', 'buyer_name', 'retailer', 'contact_person', 'buyer_address']
    ordering = ['-created_at']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Code Information', {
            'fields': ('id', 'code')
        }),
        ('Buyer Information', {
            'fields': ('buyer_name', 'buyer_address', 'contact_person', 'retailer')
        }),
        ('Relationships', {
            'fields': ('tenant', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VendorCode)
class VendorCodeAdmin(ModelAdmin):
    """Admin interface for VendorCode model"""
    
    list_display = ['code', 'vendor_name', 'gst', 'contact_person', 'email', 'tenant', 'created_at']
    list_filter = ['tenant', 'job_work_category', 'created_at']
    search_fields = ['code', 'vendor_name', 'gst', 'contact_person', 'email', 'address']
    ordering = ['-created_at']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Code Information', {
            'fields': ('id', 'code')
        }),
        ('Vendor Information', {
            'fields': ('vendor_name', 'address', 'gst', 'contact_person', 'email', 'whatsapp_number', 'alt_whatsapp_number')
        }),
        ('Banking Details', {
            'fields': ('bank_name', 'account_number', 'ifsc_code')
        }),
        ('Job Work', {
            'fields': ('job_work_category', 'job_work_sub_category', 'payment_terms')
        }),
        ('Relationships', {
            'fields': ('tenant', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# =============================================================================
# FACTORY CODE INLINES (All Steps in One View)
# =============================================================================

class ComponentInline(TabularInline):
    """Components inline for Product"""
    model = Component
    extra = 0
    fields = ['name', 'sequence', 'length', 'width', 'height', 'size_unit']
    classes = ['collapse']


class WorkOrderInline(TabularInline):
    """Work Orders inline for Raw Material"""
    model = WorkOrder
    extra = 0
    fields = ['work_order', 'wastage', 'for_field', 'for_section', 'machine_type', 'approval_against', 'remarks']
    classes = ['collapse']


class ProductInline(StackedInline):
    """Step 1: Products inline for Factory Code"""
    model = Product
    extra = 0
    fields = ['name', 'sequence', 'description']
    classes = ['collapse']
    verbose_name = "Product"
    verbose_name_plural = "📦 Step 1: Products (Cut & Sew)"
    show_change_link = True


class RawMaterialInline(StackedInline):
    """Step 2: Raw Materials inline for Factory Code"""
    model = RawMaterial
    extra = 0
    fields = [
        ('product_name', 'component_name'),
        'material_description',
        ('net_consumption', 'unit'),
    ]
    classes = ['collapse']
    verbose_name = "Raw Material"
    verbose_name_plural = "🧵 Step 2: Raw Materials"
    show_change_link = True


class ConsumptionMaterialInline(StackedInline):
    """Step 3: Trims & Accessories inline for Factory Code"""
    model = ConsumptionMaterial
    extra = 0
    fields = [
        ('trim_accessory', 'work_order'),
        ('product_name', 'component_name'),
        'material_description',
        ('net_consumption', 'unit', 'unit_additional'),
        ('size_width', 'size_length', 'size_height', 'size_unit'),
        ('length_quantity', 'surplus', 'surplus_for_section'),
        ('testing_requirement', 'approval'),
        'remarks',
    ]
    classes = ['collapse']
    verbose_name = "Trim/Accessory"
    verbose_name_plural = "✂️ Step 3: Trims & Accessories (30 Categories)"
    show_change_link = True


class ArtworkMaterialInline(StackedInline):
    """Step 4: Artwork & Labeling inline for Factory Code"""
    model = ArtworkMaterial
    extra = 0
    fields = [
        ('artwork_category', 'work_order'),
        ('components', 'placement'),
        'material_description',
        ('net_consumption', 'unit'),
        ('size_width', 'size_length', 'size_height', 'size_unit'),
        ('specific_type', 'material', 'colours'),
        ('finishing', 'permanence'),
        ('surplus', 'surplus_for_section'),
        ('approval', 'remarks'),
    ]
    classes = ['collapse']
    verbose_name = "Artwork/Label"
    verbose_name_plural = "🏷️ Step 4: Artwork & Labeling (18 Categories)"
    show_change_link = True


class PackagingMaterialInline(StackedInline):
    """Packaging Materials inline for Packaging"""
    model = PackagingMaterial
    extra = 0
    fields = [
        ('packaging_material_type', 'work_order'),
        ('components', 'product', 'placement'),
        ('net_consumption_per_pc', 'unit'),
        ('size_width', 'size_length', 'size_height', 'size_unit'),
        ('no_of_plys', 'joint_type', 'bursting_strength'),
        ('guage', 'guage_gsm', 'gumming_quality'),
        ('surplus', 'approval_against'),
        'remarks',
    ]
    classes = ['collapse']
    verbose_name = "Packaging Material"
    verbose_name_plural = "Packaging Materials (8 Types)"


class PackagingInline(StackedInline):
    """Step 5: Packaging inline for Factory Code"""
    model = Packaging
    extra = 0
    max_num = 1
    can_delete = False
    fields = [
        ('product_selection', 'packaging_type'),
        ('casepack_qty', 'assorted_sku_link'),
    ]
    classes = ['collapse']
    verbose_name = "Packaging"
    verbose_name_plural = "📦 Step 5: Packaging Configuration"


# =============================================================================
# FACTORY CODE ADMIN - Main Admin with All Steps
# =============================================================================

@admin.register(FactoryCode)
class FactoryCodeAdmin(ModelAdmin):
    """
    Main Factory Code admin - All 6 steps displayed as inlines
    Click on any Factory Code to see complete specification
    """
    
    list_display = [
        'code', 
        'product_name', 
        'sku',
        'buyer_code', 
        'status', 
        'products_count',
        'raw_materials_count',
        'trims_count',
        'artwork_count',
        'has_packaging',
        'tenant', 
        'created_at'
    ]
    list_filter = ['status', 'is_active', 'tenant', 'created_at']
    search_fields = ['code', 'sku', 'product_name', 'notes', 'buyer_code__code', 'buyer_code__buyer_name']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'created_by']
    date_hierarchy = 'created_at'
    list_per_page = 25
    ordering = ['-created_at']
    
    fieldsets = (
        ('🏭 Factory Code Identification (Step 0)', {
            'fields': (
                ('id', 'code'),
                ('sku', 'product_name'),
                'buyer_code',
            ),
            'description': 'Basic product identification information'
        }),
        ('Status & Notes', {
            'fields': (
                ('status', 'is_active'),
                'notes',
            ),
        }),
        ('Metadata', {
            'fields': ('tenant', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        ProductInline,              # Step 1: Cut & Sew
        RawMaterialInline,          # Step 2: Raw Materials
        ConsumptionMaterialInline,  # Step 3: Trims & Accessories
        ArtworkMaterialInline,      # Step 4: Artwork & Labeling
        PackagingInline,            # Step 5: Packaging
    ]
    
    actions = ['mark_as_approved', 'mark_as_in_production']
    
    # --- Count methods for list display ---
    
    def products_count(self, obj):
        count = obj.products.count()
        color = 'green' if count > 0 else 'gray'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, count)
    products_count.short_description = 'Products'
    
    def raw_materials_count(self, obj):
        count = obj.raw_materials.count()
        color = 'green' if count > 0 else 'gray'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, count)
    raw_materials_count.short_description = 'Raw Mat.'
    
    def trims_count(self, obj):
        count = obj.consumption_materials.count()
        color = 'green' if count > 0 else 'gray'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, count)
    trims_count.short_description = 'Trims'
    
    def artwork_count(self, obj):
        count = obj.artwork_materials.count()
        color = 'green' if count > 0 else 'gray'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, count)
    artwork_count.short_description = 'Artwork'
    
    def has_packaging(self, obj):
        try:
            has_pkg = obj.packaging is not None
        except Packaging.DoesNotExist:
            has_pkg = False
        color = 'green' if has_pkg else 'red'
        return format_html('<span style="color: {};">●</span>', color)
    has_packaging.short_description = 'Pkg'
    
    # --- Actions ---
    
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} factory code(s) marked as approved.')
    mark_as_approved.short_description = "✅ Mark selected as Approved"
    
    def mark_as_in_production(self, request, queryset):
        updated = queryset.update(status='in_production')
        self.message_user(request, f'{updated} factory code(s) marked as In Production.')
    mark_as_in_production.short_description = "🏭 Mark selected as In Production"
    
    # --- Save handling ---
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            if hasattr(request.user, 'tenant'):
                obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)
    
    # --- Optimize queries ---
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('buyer_code', 'tenant', 'created_by')
        qs = qs.prefetch_related('products', 'raw_materials', 'consumption_materials', 'artwork_materials')
        return qs


# =============================================================================
# DETAILED ADMIN VIEWS FOR INDIVIDUAL MODELS
# =============================================================================

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """Detailed view for Products with Components inline"""
    list_display = ['name', 'factory_code', 'sequence', 'component_count', 'created_at']
    list_filter = ['factory_code__tenant', 'factory_code__status']
    search_fields = ['name', 'factory_code__code', 'description']
    ordering = ['factory_code', 'sequence']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    inlines = [ComponentInline]
    
    fieldsets = (
        ('Product Information', {
            'fields': ('id', 'factory_code', 'name', 'sequence', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def component_count(self, obj):
        return obj.components.count()
    component_count.short_description = 'Components'


@admin.register(Component)
class ComponentAdmin(ModelAdmin):
    """Detailed view for Components"""
    list_display = ['name', 'product', 'sequence', 'size_display', 'created_at']
    list_filter = ['product__factory_code__tenant', 'size_unit']
    search_fields = ['name', 'product__name', 'product__factory_code__code']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Component Information', {
            'fields': ('id', 'product', 'name', 'sequence')
        }),
        ('Size Specifications', {
            'fields': (('length', 'width', 'height', 'size_unit'),)
        }),
        ('Additional Specifications', {
            'fields': ('specifications',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def size_display(self, obj):
        parts = []
        if obj.length:
            parts.append(f'L:{obj.length}')
        if obj.width:
            parts.append(f'W:{obj.width}')
        if obj.height:
            parts.append(f'H:{obj.height}')
        if parts:
            return f"{' × '.join(parts)} {obj.size_unit or ''}"
        return '-'
    size_display.short_description = 'Size'


@admin.register(RawMaterial)
class RawMaterialAdmin(ModelAdmin):
    """Detailed view for Raw Materials with Work Orders inline"""
    list_display = ['material_description', 'factory_code', 'product_name', 'component_name', 
                   'net_consumption', 'unit', 'work_orders_count']
    list_filter = ['factory_code__tenant', 'unit']
    search_fields = ['material_description', 'factory_code__code', 'product_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    inlines = [WorkOrderInline]
    
    fieldsets = (
        ('Raw Material Information', {
            'fields': ('id', 'factory_code', ('product', 'component'), ('product_name', 'component_name'))
        }),
        ('Material Details', {
            'fields': ('material_description', ('net_consumption', 'unit'))
        }),
        ('Specifications', {
            'fields': ('specifications',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def work_orders_count(self, obj):
        return obj.work_orders.count()
    work_orders_count.short_description = 'Work Orders'


@admin.register(WorkOrder)
class WorkOrderAdmin(ModelAdmin):
    """Detailed view for Work Orders"""
    list_display = ['raw_material', 'work_order', 'wastage', 'machine_type', 'approval_against']
    list_filter = ['work_order', 'approval_against']
    search_fields = ['raw_material__material_description', 'raw_material__factory_code__code']
    readonly_fields = ['id', 'process_data_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Work Order Information', {
            'fields': ('id', 'raw_material', 'work_order')
        }),
        ('Process Details', {
            'fields': (('wastage', 'for_field', 'for_section'), 
                      ('machine_type', 'quilting_type', 'printing_type', 'dyeing_type'),
                      ('design', 'image_ref'),
                      ('approval_against', 'remarks'))
        }),
        ('Process Specific Data', {
            'fields': ('process_data_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def process_data_display(self, obj):
        if obj.process_specific_data:
            return format_html('<pre style="background:#f5f5f5;padding:10px;border-radius:4px;">{}</pre>', 
                              json.dumps(obj.process_specific_data, indent=2))
        return '-'
    process_data_display.short_description = 'Process Specific Data (JSON)'


@admin.register(ConsumptionMaterial)
class ConsumptionMaterialAdmin(ModelAdmin):
    """Detailed view for Trims & Accessories (30 Categories)"""
    list_display = ['trim_accessory', 'factory_code', 'material_description', 
                   'net_consumption', 'unit', 'approval', 'created_at']
    list_filter = ['trim_accessory', 'approval', 'factory_code__tenant']
    search_fields = ['trim_accessory', 'material_description', 'factory_code__code']
    readonly_fields = ['id', 'category_data_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Category Selection', {
            'fields': ('id', 'factory_code', 'trim_accessory', 'work_order')
        }),
        ('Product/Component Link', {
            'fields': (('product', 'component'), ('product_name', 'component_name'))
        }),
        ('Material Details', {
            'fields': ('material_description', ('net_consumption', 'unit', 'unit_additional'))
        }),
        ('Size', {
            'fields': (('size_width', 'size_length', 'size_height', 'size_unit'),)
        }),
        ('Quantity & Surplus', {
            'fields': (('length_quantity', 'surplus', 'surplus_for_section'),)
        }),
        ('Testing & Approval', {
            'fields': (('testing_requirement', 'testing_requirement_file'), ('approval', 'remarks'))
        }),
        ('Category-Specific Data', {
            'fields': ('category_data_display',),
            'classes': ('collapse',),
            'description': 'Additional fields specific to the selected trim category'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def category_data_display(self, obj):
        if obj.category_specific_data:
            return format_html('<pre style="background:#f5f5f5;padding:10px;border-radius:4px;">{}</pre>', 
                              json.dumps(obj.category_specific_data, indent=2))
        return '-'
    category_data_display.short_description = 'Category-Specific Fields (JSON)'


@admin.register(ArtworkMaterial)
class ArtworkMaterialAdmin(ModelAdmin):
    """Detailed view for Artwork & Labeling (18 Categories)"""
    list_display = ['artwork_category', 'factory_code', 'material_description',
                   'specific_type', 'approval', 'created_at']
    list_filter = ['artwork_category', 'approval', 'factory_code__tenant']
    search_fields = ['artwork_category', 'material_description', 'factory_code__code']
    readonly_fields = ['id', 'category_data_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Category Selection', {
            'fields': ('id', 'factory_code', 'artwork_category', 'work_order')
        }),
        ('Placement', {
            'fields': ('components', 'placement')
        }),
        ('Material Details', {
            'fields': ('material_description', ('net_consumption', 'unit'))
        }),
        ('Size', {
            'fields': (('size_width', 'size_length', 'size_height', 'size_unit'), 'size_artwork_id')
        }),
        ('Artwork Specifications', {
            'fields': (('specific_type', 'material', 'colours'), ('finishing', 'permanence', 'permanence_file'))
        }),
        ('Quantity & Surplus', {
            'fields': (('length_quantity', 'length_quantity_for_section'), ('surplus', 'surplus_for_section'))
        }),
        ('Testing & Approval', {
            'fields': (('testing_requirement', 'reference_image'), ('approval', 'remarks'))
        }),
        ('Category-Specific Data', {
            'fields': ('category_data_display',),
            'classes': ('collapse',),
            'description': 'Additional fields specific to the selected artwork category'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def category_data_display(self, obj):
        if obj.category_specific_data:
            return format_html('<pre style="background:#f5f5f5;padding:10px;border-radius:4px;">{}</pre>', 
                              json.dumps(obj.category_specific_data, indent=2))
        return '-'
    category_data_display.short_description = 'Category-Specific Fields (JSON)'


@admin.register(Packaging)
class PackagingAdmin(ModelAdmin):
    """Detailed view for Packaging with Materials inline"""
    list_display = ['factory_code', 'packaging_type', 'casepack_qty', 'materials_count', 'created_at']
    list_filter = ['packaging_type', 'factory_code__tenant']
    search_fields = ['factory_code__code', 'product_selection']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    inlines = [PackagingMaterialInline]
    
    fieldsets = (
        ('Packaging Configuration', {
            'fields': ('id', 'factory_code', 'product_selection', 'packaging_type')
        }),
        ('Quantity', {
            'fields': (('casepack_qty', 'assorted_sku_link'),)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def materials_count(self, obj):
        return obj.materials.count()
    materials_count.short_description = 'Materials'


@admin.register(PackagingMaterial)
class PackagingMaterialAdmin(ModelAdmin):
    """Detailed view for Packaging Materials (8 Types)"""
    list_display = ['packaging_material_type', 'packaging', 'product', 
                   'net_consumption_per_pc', 'unit', 'created_at']
    list_filter = ['packaging_material_type', 'packaging__factory_code__tenant']
    search_fields = ['packaging_material_type', 'packaging__factory_code__code', 'product']
    readonly_fields = ['id', 'material_data_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Material Type', {
            'fields': ('id', 'packaging', 'packaging_material_type')
        }),
        ('Details', {
            'fields': (('components', 'product'), ('work_order', 'placement'))
        }),
        ('Consumption', {
            'fields': (('net_consumption_per_pc', 'unit'),)
        }),
        ('Size', {
            'fields': (('size_width', 'size_length', 'size_height', 'size_unit'),)
        }),
        ('Type-Specific Fields', {
            'fields': (
                ('no_of_plys', 'joint_type', 'bursting_strength'),
                ('guage', 'guage_gsm', 'gumming_quality'),
                ('punch_holes', 'flap_size'),
                ('roll_width', 'roll_width_unit'),
                ('tape_width', 'tape_width_unit'),
                'printing_ref',
            )
        }),
        ('Approval', {
            'fields': (('surplus', 'surplus_for_section'), ('approval_against', 'remarks'))
        }),
        ('Material-Specific Data', {
            'fields': ('material_data_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def material_data_display(self, obj):
        if obj.material_specific_data:
            return format_html('<pre style="background:#f5f5f5;padding:10px;border-radius:4px;">{}</pre>', 
                              json.dumps(obj.material_specific_data, indent=2))
        return '-'
    material_data_display.short_description = 'Material-Specific Fields (JSON)'


@admin.register(PackagingWorkOrder)
class PackagingWorkOrderAdmin(ModelAdmin):
    """Work Orders for Packaging Materials"""
    list_display = ['packaging_material', 'work_order', 'created_at']
    list_filter = ['work_order']
    search_fields = ['packaging_material__packaging__factory_code__code']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Work Order', {
            'fields': ('id', 'packaging_material', 'work_order')
        }),
        ('Additional Data', {
            'fields': ('work_order_data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )