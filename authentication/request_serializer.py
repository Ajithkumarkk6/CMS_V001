from rest_framework import serializers

class RegisterUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)

class RegisterCustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=True)
    email = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)

class AttachUserAccountsSerializer(serializers.Serializer):
    pass
    # first_name = serializers.CharField(required=True)
    # last_name = serializers.CharField(required=False)
    # mobile_number = serializers.CharField(required=False)
    # email = serializers.CharField(required=False)
    # gender = serializers.CharField(required=False)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class SubmitRegistationOtpSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=False)
    otp = serializers.CharField(required=True)

class OtpLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=False)
    otp = serializers.CharField(required=True)

class OtpRegisterSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)

class GetBusinessPlacesSerializer(serializers.Serializer):
    q = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    location_latitude = serializers.CharField(required=False)
    location_longitude = serializers.CharField(required=False)

class GetBusinessPlaceDetailsSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)

class ValidateUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True)

class ValidateUserEmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

class ValidateUserMobileSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True)
    app_user_type = serializers.CharField(required=True)
    ln = serializers.CharField(required=True)

class ValidateResendOtpSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

class RegisterCompanySerializer(serializers.Serializer):
    registered_name = serializers.CharField(required=True)
    brand_name = serializers.CharField(required=True)
    brand_service_type_id = serializers.UUIDField(required=True)
    brand_sector_id = serializers.UUIDField(required=True)
    # pan = serializers.CharField(required=True)
    # gst = serializers.CharField(required=True)
    communication_address = serializers.CharField(required=True)
    pincode = serializers.CharField(required=True)
    # city = serializers.CharField(required=True)
    # referral_id = serializers.CharField(required=False)
