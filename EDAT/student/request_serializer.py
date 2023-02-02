from rest_framework import serializers


class AddStudentCourseTaskSerializer(serializers.Serializer):
    start_date = serializers.CharField(required=False)
    base_status = serializers.CharField(required=False)
    is_inprogress = serializers.BooleanField(required=False)
    # approver_id = serializers.UUIDField(required=False)
    course_task_id = serializers.UUIDField(required=True)
    formulated_question = serializers.CharField(required=False)
    procedure = serializers.JSONField(required=False)
    flow_diagram = serializers.JSONField(required=False)
    program = serializers.CharField(required=False)





