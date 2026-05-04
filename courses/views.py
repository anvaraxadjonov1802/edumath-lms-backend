from django.db.models import Q

from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Course,
    GlossaryTerm,
    Material,
    Question,
    Reference,
    TestResult,
    Topic,
)
from .serializers import (
    CourseDetailSerializer,
    CourseListSerializer,
    GlossaryTermSerializer,
    MaterialSerializer,
    QuestionSerializer,
    ReferenceSerializer,
    SubmitTestSerializer,
    TestResultSerializer,
    TopicDetailSerializer,
    TopicListSerializer,
)


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True).order_by("id")

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset


class CourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Course.objects.filter(is_active=True).prefetch_related(
            "modules",
            "modules__topics",
        )


class TopicListAPIView(generics.ListAPIView):
    serializer_class = TopicListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Topic.objects.filter(
            is_active=True,
            module__is_active=True,
            module__course__is_active=True,
        ).select_related("module", "module__course").order_by("module__order", "order")

        module_id = self.request.query_params.get("module")
        course_id = self.request.query_params.get("course")
        search = self.request.query_params.get("search")

        if module_id:
            queryset = queryset.filter(module_id=module_id)

        if course_id:
            queryset = queryset.filter(module__course_id=course_id)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset


class TopicDetailAPIView(generics.RetrieveAPIView):
    serializer_class = TopicDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Topic.objects.filter(
            is_active=True,
            module__is_active=True,
            module__course__is_active=True,
        ).select_related(
            "module",
            "module__course",
        ).prefetch_related(
            "materials",
            "questions",
        )


class TopicMaterialsAPIView(generics.ListAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        topic_id = self.kwargs.get("topic_id")

        topic_exists = Topic.objects.filter(
            id=topic_id,
            is_active=True,
            module__is_active=True,
            module__course__is_active=True,
        ).exists()

        if not topic_exists:
            raise NotFound("Mavzu topilmadi")

        queryset = Material.objects.filter(topic_id=topic_id).order_by("order", "id")

        material_type = self.request.query_params.get("type")
        if material_type:
            queryset = queryset.filter(material_type=material_type)

        return queryset


class TopicQuestionsAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        topic_id = self.kwargs.get("topic_id")

        topic_exists = Topic.objects.filter(
            id=topic_id,
            is_active=True,
            module__is_active=True,
            module__course__is_active=True,
        ).exists()

        if not topic_exists:
            raise NotFound("Mavzu topilmadi")

        return Question.objects.filter(
            topic_id=topic_id,
            is_active=True,
        ).prefetch_related("answers").order_by("order")


class ReferenceListAPIView(generics.ListAPIView):
    serializer_class = ReferenceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Reference.objects.all().order_by("id")

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset


class GlossaryTermListAPIView(generics.ListAPIView):
    serializer_class = GlossaryTermSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = GlossaryTerm.objects.all().order_by("term_uz")

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(term_uz__icontains=search) |
                Q(term_en__icontains=search) |
                Q(term_ru__icontains=search) |
                Q(definition__icontains=search)
            )

        return queryset
    

class SubmitTestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, topic_id):
        try:
            topic = Topic.objects.get(
                id=topic_id,
                is_active=True,
                module__is_active=True,
                module__course__is_active=True,
            )
        except Topic.DoesNotExist:
            raise NotFound("Mavzu topilmadi")

        serializer = SubmitTestSerializer(
            data=request.data,
            context={"topic": topic},
        )
        serializer.is_valid(raise_exception=True)

        test_data = serializer.save(user=request.user)
        result = test_data["result"]

        return Response(
            {
                "message": "Test muvaffaqiyatli yakunlandi",
                "result": TestResultSerializer(result).data,
                "summary": {
                    "score": test_data["score"],
                    "total_questions": test_data["total_questions"],
                    "answered_questions": test_data["answered_questions"],
                    "percentage": test_data["percentage"],
                },
            },
            status=status.HTTP_201_CREATED,
        )


class MyTestResultsAPIView(generics.ListAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestResult.objects.filter(
            user=self.request.user,
        ).select_related(
            "topic",
            "topic__module",
            "topic__module__course",
        ).order_by("-created_at")