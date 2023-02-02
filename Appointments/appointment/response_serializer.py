from rest_framework import serializers
from providerservice.models import BrandBranchCategory, ServiceMasterUomFormFieldServiceMapping, ServiceType, PredefinedCategory, PredefinedServices

class ServiceTypeSerializer(serializers.ModelSerializer):

    sector_id = serializers.SerializerMethodField()

    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'sector_id']

    def get_sector_id(self, obj):
        if obj.service_sector is not None:
            return obj.service_sector.id
        else:
            return None


class  ServiceMasterUomFormFieldServiceMappingSerializer(serializers.ModelSerializer):

    uom_name = serializers.SerializerMethodField()
    uom_support_data = serializers.SerializerMethodField()
    uom_field_type = serializers.SerializerMethodField()
    display_order = serializers.SerializerMethodField()

    class Meta:
        model = ServiceMasterUomFormFieldServiceMapping
        fields = ['id', 'display_order', 'uom_name', 'uom_support_data', 'uom_field_type']

    def get_uom_name(self, obj):
        return obj.master_uom.name

    def get_uom_field_type(self, obj):
        return obj.master_uom.field_type.tag

    def get_uom_support_data(self, obj):
        return obj.master_uom.support_data

    def get_display_order(self, obj):
        return obj.display_order

class PredefinedCategorySerializer(serializers.ModelSerializer):

    parent = serializers.SerializerMethodField()

    class Meta:
        model = PredefinedCategory
        fields = ['id', 'display_name', 'is_parent', 'parent', 'is_independent_slot']

    def get_parent(self, obj):
        if obj.parent is not None:
            return obj.parent.id
        else:
            return None


class PredefinedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PredefinedServices
        fields = ['id', 'display_name', 'description']


class BrandBranchCategorySerializer(serializers.ModelSerializer):

    brand_meta_parent_id = serializers.SerializerMethodField()
    brand_meta_id = serializers.SerializerMethodField()
    is_parent = serializers.SerializerMethodField()
    is_independent_slot = serializers.SerializerMethodField()

    class Meta:
        model = BrandBranchCategory
        fields = ['id', 'display_name', 'is_parent', 'brand_meta_parent_id', 'brand_meta_id', 'is_independent_slot']

    def get_is_parent(self, obj):
        return obj.brand_category.is_parent

    def get_is_independent_slot(self, obj):
        return obj.brand_category.is_independent_slot


    def get_brand_meta_parent_id(self, obj):
        if obj.brand_category.parent is not None:
            return obj.brand_category.parent.id
        else:
            return None

    def get_brand_meta_id(self, obj):
        return obj.brand_category.id



class BrandBranchServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrandBranchCategory
        fields = ['id', 'display_name', 'description', 'service_time', 'service_price']