from django.urls import path

from .views import (
    CourseDetailAPIView,
    CourseListAPIView,
    GlossaryTermListAPIView,
    MyTestResultsAPIView,
    ReferenceListAPIView,
    SubmitTestAPIView,
    TopicDetailAPIView,
    TopicListAPIView,
    TopicMaterialsAPIView,
    TopicQuestionsAPIView,
)

urlpatterns = [
    path("courses/", CourseListAPIView.as_view(), name="course-list"),
    path("courses/<slug:slug>/", CourseDetailAPIView.as_view(), name="course-detail"),

    path("topics/", TopicListAPIView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", TopicDetailAPIView.as_view(), name="topic-detail"),
    path("topics/<int:topic_id>/materials/", TopicMaterialsAPIView.as_view(), name="topic-materials"),
    path("topics/<int:topic_id>/questions/", TopicQuestionsAPIView.as_view(), name="topic-questions"),
    path("topics/<int:topic_id>/submit-test/", SubmitTestAPIView.as_view(), name="submit-test"),

    path("my-results/", MyTestResultsAPIView.as_view(), name="my-results"),

    path("references/", ReferenceListAPIView.as_view(), name="reference-list"),
    path("glossary/", GlossaryTermListAPIView.as_view(), name="glossary-list"),
]