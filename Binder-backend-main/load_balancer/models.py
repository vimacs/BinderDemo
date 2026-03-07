from django.db import models

# Models will be added as we develop each pillar
# """
# Factory Code Admin - Corrected for inventory_management models
# ===============================================================

# Django admin configuration matching the actual model field names.
# """

# from django.contrib import admin
# from django.utils.html import format_html
# import json

# from .models import (
#     FactoryCode, Product, Component, RawMaterial, WorkOrder,
#     ConsumptionMaterial, ArtworkMaterial, Packaging, PackagingMaterial,
#     PackagingWorkOrder, BuyerCode, VendorCode, Department, Segment
# )


# # =============================================================================
# # INLINE ADMINS
# # =============================================================================

# class ComponentInline(admin.TabularInline):
#     model = Component
#     extra = 0
#     fields = ['name', 'sequence', 'length', 'width', 'height', 'size_unit']


# class WorkOrderInline(admin.TabularInline):
#     model = WorkOrder
#     extra = 0
#     fields = ['work_order', 'wastage', 'for_field', 'remarks']


# class RawMaterialInline(admin.TabularInline):
#     model = RawMaterial
#     extra = 0
#     fields = ['product_name', 'component_name', 'material_description', 'net_consumption', 'unit']


# class ProductInline(admin.TabularInline):
#     model = Product
#     extra = 0
#     fields = ['name', 'sequence', 'description']
#     show_change_link = True


# class ConsumptionMaterialInline(admin.TabularInline):
#     model = ConsumptionMaterial
#     extra = 0
#     fields = ['trim_accessory', 'material_description', 'net_consumption', 'unit']
#     show_change_link = True


# class ArtworkMaterialInline(admin.TabularInline):
#     model = ArtworkMaterial
#     extra = 0
#     fields = ['artwork_category', 'material_description', 'net_consumption', 'unit']
#     show_change_link = True


# class PackagingMaterialInline(admin.TabularInline):
#     model = PackagingMaterial
#     extra = 0
#     fields = ['packaging_material_type', 'product', 'net_consumption_per_pc', 'unit']


# class PackagingWorkOrderInline(admin.TabularInline):
#     model = PackagingWorkOrder
#     extra = 0
#     fields = ['work_order']


# # =============================================================================
# # MODEL ADMINS
# # =============================================================================

# @admin.register(FactoryCode)
# class FactoryCodeAdmin(admin.ModelAdmin):
#     list_display = ['code', 'sku', 'product_name', 'buyer_code', 'status', 'tenant', 'created_at']
#     list_filter = ['status', 'tenant', 'created_at']
#     search_fields = ['code', 'sku', 'product_name', 'notes']
#     readonly_fields = ['code', 'created_at', 'updated_at', 'created_by']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ('Identification', {
#             'fields': ('code', 'sku', 'product_name', 'buyer_code')
#         }),
#         ('Status', {
#             'fields': ('status', 'is_active', 'notes')
#         }),
#         ('Metadata', {
#             'fields': ('tenant', 'created_by', 'created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     inlines = [ProductInline, ConsumptionMaterialInline, ArtworkMaterialInline]
    
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#             if hasattr(request.user, 'tenant'):
#                 obj.tenant = request.user.tenant
#         super().save_model(request, obj, form, change)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'factory_code', 'sequence', 'component_count']
#     list_filter = ['factory_code__tenant']
#     search_fields = ['name', 'factory_code__code', 'description']
    
#     inlines = [ComponentInline]
    
#     def component_count(self, obj):
#         return obj.components.count()
#     component_count.short_description = 'Components'


# @admin.register(Component)
# class ComponentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'product', 'sequence', 'size_display']
#     list_filter = ['product__factory_code__tenant', 'size_unit']
#     search_fields = ['name', 'product__name', 'product__factory_code__code']
    
#     inlines = [RawMaterialInline]
    
#     def size_display(self, obj):
#         parts = []
#         if obj.width:
#             parts.append(f'W:{obj.width}')
#         if obj.length:
#             parts.append(f'L:{obj.length}')
#         if obj.height:
#             parts.append(f'H:{obj.height}')
#         if parts and obj.size_unit:
#             return f"{' x '.join(parts)} {obj.size_unit}"
#         return '-'
#     size_display.short_description = 'Size'


# @admin.register(RawMaterial)
# class RawMaterialAdmin(admin.ModelAdmin):
#     list_display = ['material_description', 'factory_code', 'product_name', 'component_name', 'net_consumption', 'unit']
#     list_filter = ['factory_code__tenant', 'unit']
#     search_fields = ['material_description', 'product_name', 'component_name']
    
#     inlines = [WorkOrderInline]


# @admin.register(WorkOrder)
# class WorkOrderAdmin(admin.ModelAdmin):
#     list_display = ['raw_material', 'work_order', 'wastage', 'has_process_data']
#     list_filter = ['work_order']
#     search_fields = ['raw_material__material_description', 'remarks']
#     readonly_fields = ['process_specific_data_display']
    
#     def has_process_data(self, obj):
#         return bool(obj.process_specific_data)
#     has_process_data.boolean = True
#     has_process_data.short_description = 'Has Data'
    
#     def process_specific_data_display(self, obj):
#         if obj.process_specific_data:
#             return format_html('<pre>{}</pre>', json.dumps(obj.process_specific_data, indent=2))
#         return '-'
#     process_specific_data_display.short_description = 'Process Specific Data'


# @admin.register(ConsumptionMaterial)
# class ConsumptionMaterialAdmin(admin.ModelAdmin):
#     list_display = ['trim_accessory', 'factory_code', 'material_description', 'net_consumption', 'unit', 'created_at']
#     list_filter = ['trim_accessory', 'unit', 'factory_code__tenant']
#     search_fields = ['trim_accessory', 'material_description', 'factory_code__code', 'remarks']
#     readonly_fields = ['category_specific_data_display', 'created_at']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ('Category', {
#             'fields': ('factory_code', 'trim_accessory', 'product', 'component')
#         }),
#         ('Material Info', {
#             'fields': ('product_name', 'component_name', 'material_description')
#         }),
#         ('Consumption', {
#             'fields': ('net_consumption', 'unit', 'unit_additional', 'length_quantity', 'surplus', 'surplus_for_section')
#         }),
#         ('Size', {
#             'fields': ('size_width', 'size_length', 'size_height', 'size_unit')
#         }),
#         ('Testing & Approval', {
#             'fields': ('testing_requirement', 'testing_requirement_file', 'approval', 'remarks')
#         }),
#         ('Category-Specific Data', {
#             'fields': ('category_specific_data_display',),
#             'classes': ('collapse',)
#         }),
#         ('Metadata', {
#             'fields': ('created_at',),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def category_specific_data_display(self, obj):
#         if obj.category_specific_data:
#             return format_html('<pre>{}</pre>', json.dumps(obj.category_specific_data, indent=2))
#         return '-'
#     category_specific_data_display.short_description = 'Category-Specific Data'


# @admin.register(ArtworkMaterial)
# class ArtworkMaterialAdmin(admin.ModelAdmin):
#     list_display = ['artwork_category', 'factory_code', 'material_description', 'net_consumption', 'unit', 'created_at']
#     list_filter = ['artwork_category', 'unit', 'factory_code__tenant']
#     search_fields = ['artwork_category', 'material_description', 'factory_code__code', 'remarks']
#     readonly_fields = ['category_specific_data_display', 'created_at']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ('Category', {
#             'fields': ('factory_code', 'artwork_category')
#         }),
#         ('Material Info', {
#             'fields': ('components', 'material_description', 'placement')
#         }),
#         ('Consumption', {
#             'fields': ('net_consumption', 'unit', 'length_quantity', 'length_quantity_for_section', 'surplus', 'surplus_for_section')
#         }),
#         ('Size', {
#             'fields': ('size_width', 'size_length', 'size_height', 'size_unit', 'size_artwork_id')
#         }),
#         ('Details', {
#             'fields': ('specific_type', 'material', 'colours', 'finishing', 'permanence', 'permanence_file')
#         }),
#         ('Testing & Approval', {
#             'fields': ('testing_requirement', 'reference_image', 'approval', 'remarks')
#         }),
#         ('Category-Specific Data', {
#             'fields': ('category_specific_data_display',),
#             'classes': ('collapse',)
#         }),
#         ('Metadata', {
#             'fields': ('created_at',),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def category_specific_data_display(self, obj):
#         if obj.category_specific_data:
#             return format_html('<pre>{}</pre>', json.dumps(obj.category_specific_data, indent=2))
#         return '-'
#     category_specific_data_display.short_description = 'Category-Specific Data'


# @admin.register(Packaging)
# class PackagingAdmin(admin.ModelAdmin):
#     list_display = ['factory_code', 'packaging_type', 'casepack_qty', 'material_count']
#     list_filter = ['packaging_type', 'factory_code__tenant']
#     search_fields = ['factory_code__code', 'product_selection']
    
#     inlines = [PackagingMaterialInline]
    
#     def material_count(self, obj):
#         return obj.materials.count()
#     material_count.short_description = 'Materials'


# @admin.register(PackagingMaterial)
# class PackagingMaterialAdmin(admin.ModelAdmin):
#     list_display = ['packaging_material_type', 'packaging', 'product', 'net_consumption_per_pc', 'unit', 'created_at']
#     list_filter = ['packaging_material_type', 'packaging__factory_code__tenant']
#     search_fields = ['packaging_material_type', 'packaging__factory_code__code', 'product']
#     readonly_fields = ['material_specific_data_display', 'created_at']
    
#     inlines = [PackagingWorkOrderInline]
    
#     fieldsets = (
#         ('Material', {
#             'fields': ('packaging', 'packaging_material_type', 'components', 'product')
#         }),
#         ('Consumption', {
#             'fields': ('net_consumption_per_pc', 'unit', 'work_order', 'placement')
#         }),
#         ('Size', {
#             'fields': ('size_width', 'size_length', 'size_height', 'size_unit')
#         }),
#         ('Type-Specific Fields', {
#             'fields': ('no_of_plys', 'joint_type', 'bursting_strength', 'guage', 'guage_gsm', 
#                       'gumming_quality', 'punch_holes', 'flap_size', 'roll_width', 'roll_width_unit',
#                       'tape_width', 'tape_width_unit', 'printing_ref')
#         }),
#         ('Approval', {
#             'fields': ('surplus', 'surplus_for_section', 'approval_against', 'remarks')
#         }),
#         ('Material-Specific Data', {
#             'fields': ('material_specific_data_display',),
#             'classes': ('collapse',)
#         }),
#         ('Metadata', {
#             'fields': ('created_at',),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def material_specific_data_display(self, obj):
#         if obj.material_specific_data:
#             return format_html('<pre>{}</pre>', json.dumps(obj.material_specific_data, indent=2))
#         return '-'
#     material_specific_data_display.short_description = 'Material-Specific Data'


# @admin.register(PackagingWorkOrder)
# class PackagingWorkOrderAdmin(admin.ModelAdmin):
#     list_display = ['packaging_material', 'work_order', 'created_at']
#     list_filter = ['work_order']
#     search_fields = ['packaging_material__packaging__factory_code__code', 'work_order']
