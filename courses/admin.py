from django.contrib import admin

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


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ("title", "order", "is_active")


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1
    fields = ("title", "order", "is_active")


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ("text", "is_correct")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "order", "is_active")
    list_filter = ("course", "is_active")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "module", "order", "is_active")
    list_filter = ("module", "is_active")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "topic", "material_type", "order", "uploaded_at")
    list_filter = ("material_type", "topic")
    search_fields = ("title", "description", "topic__title")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "topic", "order", "is_active")
    list_filter = ("topic", "is_active")
    search_fields = ("text", "topic__title")
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "question", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("text", "question__text")


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "topic",
        "score",
        "total_questions",
        "percentage",
        "created_at",
    )
    list_filter = ("topic", "created_at")
    search_fields = ("user__username", "topic__title")
    readonly_fields = ("created_at",)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "year")
    search_fields = ("title", "author", "description")


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ("id", "term_uz", "term_en", "term_ru")
    search_fields = ("term_uz", "term_en", "term_ru", "definition")