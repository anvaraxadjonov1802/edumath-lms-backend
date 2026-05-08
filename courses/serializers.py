from rest_framework import serializers

from .models import (
    Answer,
    Course,
    GlossaryTerm,
    Material,
    Module,
    Question,
    Reference,
    TestResult,
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
            "external_url",
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


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()


class SubmitTestSerializer(serializers.Serializer):
    answers = SubmitAnswerSerializer(many=True)

    def validate_answers(self, value):
        if not value:
            raise serializers.ValidationError("Kamida bitta javob yuborilishi kerak")

        topic = self.context.get("topic")

        active_question_ids = set(
            topic.questions.filter(is_active=True).values_list("id", flat=True)
        )

        if not active_question_ids:
            raise serializers.ValidationError("Bu mavzu uchun faol test savollari mavjud emas")

        submitted_question_ids = []

        for item in value:
            question_id = item.get("question_id")
            answer_id = item.get("answer_id")

            if question_id not in active_question_ids:
                raise serializers.ValidationError(
                    f"{question_id} ID li savol ushbu mavzuga tegishli emas"
                )

            if question_id in submitted_question_ids:
                raise serializers.ValidationError(
                    f"{question_id} ID li savolga takror javob yuborilgan"
                )

            answer_exists = Answer.objects.filter(
                id=answer_id,
                question_id=question_id,
            ).exists()

            if not answer_exists:
                raise serializers.ValidationError(
                    f"{answer_id} ID li javob {question_id} ID li savolga tegishli emas"
                )

            submitted_question_ids.append(question_id)

        return value

    def save(self, **kwargs):
        user = kwargs.get("user")
        topic = self.context.get("topic")
        answers = self.validated_data["answers"]

        total_questions = topic.questions.filter(is_active=True).count()
        answered_questions = len(answers)

        submitted_answer_ids = [item["answer_id"] for item in answers]

        score = Answer.objects.filter(
            id__in=submitted_answer_ids,
            is_correct=True,
        ).count()

        percentage = round((score / total_questions) * 100, 2)

        result = TestResult.objects.create(
            user=user,
            topic=topic,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
        )

        return {
            "result": result,
            "score": score,
            "total_questions": total_questions,
            "answered_questions": answered_questions,
            "percentage": percentage,
        }


class TestResultSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source="topic.title", read_only=True)
    module_title = serializers.CharField(source="topic.module.title", read_only=True)
    course_title = serializers.CharField(source="topic.module.course.title", read_only=True)
    grade = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = (
            "id",
            "topic",
            "topic_title",
            "module_title",
            "course_title",
            "score",
            "total_questions",
            "percentage",
            "grade",
            "created_at",
        )

    def get_grade(self, obj):
        if obj.percentage >= 90:
            return "A'lo"
        if obj.percentage >= 70:
            return "Yaxshi"
        if obj.percentage >= 50:
            return "Qoniqarli"
        return "Qoniqarsiz"