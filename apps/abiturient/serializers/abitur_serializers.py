from apps.abiturient.models import Request, Exam, Department, CertificateImage
from rest_framework.serializers import ModelSerializer


class CertificateImageSerializer(ModelSerializer):
    class Meta:
        model = CertificateImage
        fields = "__all__"
        ref_name = 'CertificateImage'

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        ref_name = 'Department'


class RequestReadSerializer(ModelSerializer):
    certs = CertificateImageSerializer(many=True, read_only=True)

    class Meta:
        model = Request
        fields = '__all__'
        ref_name = 'RequestRead'


class RequestSerializer(ModelSerializer):
    certs = CertificateImageSerializer(many=True, read_only=True)

    class Meta:
        model = Request
        fields = '__all__'
        ref_name = 'Request'

    def save_images(self, instance, is_update=False):
        request = self.context.get("request")
        images_data = request.FILES.getlist("certs", [])

        if is_update:
            instance.images.all().delete()

        for image_data in images_data:
            CertificateImage.objects.create(request=instance, image=image_data)

    def create(self, validated_data):
        certificate = Request.objects.create(**validated_data)
        self.save_images(certificate)
        return certificate

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self.save_images(instance, is_update=True)
        return instance
