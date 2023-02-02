from rest_framework import serializers


class AddTimeSheetSerializer(serializers.Serializer):
    details = serializers.CharField(required=True)

class AttendanceSettingsSerializer(serializers.Serializer):
    start_time = serializers.CharField(required=True)
    end_time = serializers.CharField(required=True)
    is_excempt_allowed = serializers.BooleanField(required=True)


class AddDesignationSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    is_admin = serializers.BooleanField(required=True)

class UpdateEmployeeCheckinAssociationsSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)

class GetEmployeeDetailsSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)

class ValidateUserByFaceSerializer(serializers.Serializer):
    pass

class UpdateEmployeeProfilePhotoSerializer(serializers.Serializer):
    pass
    # attachments = serializers.CharField(required=True)
    
    # user_id = serializers.UUIDField(required=True)

class EnableFaceReRegisterSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)


class UpdateEmployeeStatusSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    is_active = serializers.BooleanField(required=True)

class AddEmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    pan = serializers.CharField(required=True)
    aadhar_number = serializers.CharField(required=True)
    attendance_settings = AttendanceSettingsSerializer(required=True)
    designation_id = serializers.UUIDField(required=True)
    department_id = serializers.UUIDField(required=True)
    branch_id = serializers.UUIDField(required=True)
    id = serializers.UUIDField(required=False)


class AddEmployeeSerializerV1(serializers.Serializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    pan = serializers.CharField(required=False)
    aadhar_number = serializers.CharField(required=False)
    attendance_settings = AttendanceSettingsSerializer(required=True)
    designation_id = serializers.UUIDField(required=True)
    department_id = serializers.UUIDField(required=True)
    branch_id = serializers.UUIDField(required=True)
    id = serializers.UUIDField(required=False)
    date_of_joining = serializers.CharField(required=False)
    dob = serializers.CharField(required=False)
    employment_type = serializers.CharField(required=False)
    blood_group = serializers.CharField(required=False)