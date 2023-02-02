from rest_framework import serializers

class GetPredefinedCategoriesSerializer(serializers.Serializer):
    service_type_id = serializers.UUIDField(required=True)

class AddBrandCategorySerializer(serializers.Serializer):
    service_type_id = serializers.UUIDField(required=True)
    id = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    is_parent = serializers.BooleanField(required=True)
    parent_id = serializers.UUIDField(required=False)
    is_independent_slot = serializers.BooleanField(required=True)
    service_time = serializers.IntegerField(required=False)
    service_price = serializers.IntegerField(required=False)

class AddBrandServiceSerializer(serializers.Serializer):
    service_type_id = serializers.UUIDField(required=True)
    branch_meta_id = serializers.UUIDField(required=True)
    id = serializers.UUIDField(required=False)
    display_name = serializers.CharField(required=True)
    service_time = serializers.CharField(required=False)
    service_price = serializers.CharField(required=False)

class UpdateBrandBranchServiceSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)

class UpdateBrandServiceSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)

class GetPredefinedFormFieldsSerializer(serializers.Serializer):
    service_type_id = serializers.UUIDField(required=True)


class GetPredefinedServicesSerializer(serializers.Serializer):
    service_ids = serializers.ListField(child=serializers.UUIDField(required=True))


class SubmitBrandMasterUomSerializer(serializers.Serializer):
    brand_id =  serializers.UUIDField(required=True) 
    # serializers.ListField(child=serializers.UUIDField(required=True))

class SubmitBrandServicesSerializer(serializers.Serializer):
    brand_id =  serializers.UUIDField(required=True) 


class AddBranchSerializer(serializers.Serializer):
    communication_address = serializers.CharField(required=True)
    billing_address = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    city = serializers.CharField(required=True)
    district = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    pincode = serializers.CharField(required=True)
    parent = serializers.CharField(required=True)
    
class AddBranchLocationSerializer(serializers.Serializer):
    location_latitude = serializers.CharField(required=True)
    location_longitude = serializers.CharField(required=True)
    fencing_radius = serializers.IntegerField(required=False)

class AddFenceAdminSerializer(serializers.Serializer):
    branch_id = serializers.UUIDField(required=True)
    employee_id = serializers.UUIDField(required=True)


class UpdateBranchLocationSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    location_latitude = serializers.CharField(required=False)
    location_longitude = serializers.CharField(required=False)
    fencing_radius = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        instance.location_latitude = validated_data.get('location_latitude', instance.location_latitude)
        instance.location_longitude = validated_data.get('location_longitude', instance.location_longitude)
        instance.fencing_radius = validated_data.get('fencing_radius', instance.fencing_radius)
        instance.save()
        return instance


class AddDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)


class EnableBranchFenceSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)


class GetBrandBranchCategoriesSerializer(serializers.Serializer):
    branch_id = serializers.UUIDField(required=True)

class GetBrandBranchServicesSerializer(serializers.Serializer):
    brand_meta_ids = serializers.ListField(child=serializers.UUIDField(required=True))

class SubmitBrandBranchCalendarWeekSerializer(serializers.Serializer):
    week_calendar = serializers.ListField(child=serializers.JSONField(required=True))
    brand_id = serializers.UUIDField(required=True)
    branch_id = serializers.UUIDField(required=False)

