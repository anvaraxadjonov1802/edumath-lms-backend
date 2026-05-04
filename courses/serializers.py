from rest_framework import serializers

from .models import (
    Answer,
    Course,
    GlossaryTerm,
    Material,
    Module,
    Question,
    Reference,
    Topic,
)


class MaterialSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    material_type_display = serializers.CharField(
        source="get_material_type_display",
        read_only=True,
    )

    class Meta:
        model = Material
        fields = (
            "id",
            "title",
            "description",
            "material_type",
            "material_type_display",
            "file",
            "file_url",
            "order",
            "uploaded_at",
        )

    def get_file_url(self, obj):
        request = self.context.get("request")

        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)

        if obj.file:
            return obj.file.url

        return None


class PublicAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "text",
        )


class QuestionSerializer(serializers.ModelSerializer):
    answers = PublicAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "text",
            "order",
            "answers",
        )


class TopicListSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source="module.title", read_only=True)
    course_title = serializers.CharField(source="module.course.title", read_only=True)

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "order",
            "module",
            "module_title",
            "course_title",
        )


class TopicDetailSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source="module.title", read_only=True)
    course_title = serializers.CharField(source="module.course.title", read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "order",
            "module",
            "module_title",
            "course_title",
            "materials",
            "questions_count",
        )

    def get_questions_count(self, obj):
        return obj.questions.filter(is_active=True).count()


class ModuleSerializer(serializers.ModelSerializer):
    topics = TopicListSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "order",
            "topics",
        )


class CourseListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    modules_count = serializers.SerializerMethodField()
    topics_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "image",
            "image_url",
            "modules_count",
            "topics_count",
            "created_at",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")

        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)

        if obj.image:
            return obj.image.url

        return None

    def get_modules_count(self, obj):
        return obj.modules.filter(is_active=True).count()

    def get_topics_count(self, obj):
        return Topic.objects.filter(
            module__course=obj,
            is_active=True,
            module__is_active=True,
        ).count()


class CourseDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "image",
            "image_url",
            "modules",
            "created_at",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")

        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)

        if obj.image:
            return obj.image.url

        return None


class ReferenceSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Reference
        fields = (
            "id",
            "title",
            "author",
            "year",
            "link",
            "file",
            "file_url",
            "description",
        )

    def get_file_url(self, obj):
        request = self.context.get("request")

        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)

        if obj.file:
            return obj.file.url

        return None


class GlossaryTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryTerm
        fields = (
            "id",
            "term_uz",
            "term_en",
            "term_ru",
            "definition",
        )