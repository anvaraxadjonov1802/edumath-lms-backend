from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Kurs nomi")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(verbose_name="Kurs haqida")
    image = models.ImageField(
        upload_to="courses/images/",
        blank=True,
        null=True,
        verbose_name="Kurs rasmi"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name="Kurs"
    )
    title = models.CharField(max_length=255, verbose_name="Qism nomi")
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(blank=True, verbose_name="Qism haqida")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = "Qism"
        verbose_name_plural = "Qismlar"
        ordering = ["order"]
        unique_together = ("course", "slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Topic(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="topics",
        verbose_name="Qism"
    )
    title = models.CharField(max_length=255, verbose_name="Mavzu nomi")
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(blank=True, verbose_name="Mavzu haqida")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"
        ordering = ["order"]
        unique_together = ("module", "slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Material(models.Model):
    class MaterialType(models.TextChoices):
        THEORY = "theory", "Nazariy qism"
        PRACTICE = "practice", "Amaliy qism"
        PRESENTATION = "presentation", "Prezentatsiya"
        ASSIGNMENT = "assignment", "Mustaqil ish"
        LITERATURE = "literature", "Adabiyot"
        OTHER = "other", "Boshqa"

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="Mavzu"
    )
    title = models.CharField(max_length=255, verbose_name="Material nomi")
    description = models.TextField(blank=True, verbose_name="Material haqida")
    material_type = models.CharField(
        max_length=30,
        choices=MaterialType.choices,
        default=MaterialType.THEORY,
        verbose_name="Material turi"
    )
    file = models.FileField(
        upload_to="materials/",
        verbose_name="Fayl"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class Question(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Mavzu"
    )
    text = models.TextField(verbose_name="Savol matni")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = "Test savoli"
        verbose_name_plural = "Test savollari"
        ordering = ["order"]

    def __str__(self):
        return self.text[:80]


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Savol"
    )
    text = models.CharField(max_length=500, verbose_name="Javob matni")
    is_correct = models.BooleanField(default=False, verbose_name="To‘g‘ri javobmi?")

    class Meta:
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"

    def __str__(self):
        return self.text[:80]


class TestResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="test_results",
        verbose_name="Foydalanuvchi"
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="test_results",
        verbose_name="Mavzu"
    )
    score = models.PositiveIntegerField(verbose_name="To‘g‘ri javoblar soni")
    total_questions = models.PositiveIntegerField(verbose_name="Jami savollar soni")
    percentage = models.FloatField(verbose_name="Foiz")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.topic.title} - {self.percentage}%"


class Reference(models.Model):
    title = models.CharField(max_length=255, verbose_name="Adabiyot nomi")
    author = models.CharField(max_length=255, blank=True, verbose_name="Muallif")
    year = models.CharField(max_length=20, blank=True, verbose_name="Yil")
    link = models.URLField(blank=True, verbose_name="Havola")
    file = models.FileField(
        upload_to="references/",
        blank=True,
        null=True,
        verbose_name="Fayl"
    )
    description = models.TextField(blank=True, verbose_name="Izoh")

    class Meta:
        verbose_name = "Adabiyot"
        verbose_name_plural = "Adabiyotlar"
        ordering = ["id"]

    def __str__(self):
        return self.title


class GlossaryTerm(models.Model):
    term_uz = models.CharField(max_length=255, verbose_name="O‘zbekcha atama")
    term_en = models.CharField(max_length=255, blank=True, verbose_name="Inglizcha atama")
    term_ru = models.CharField(max_length=255, blank=True, verbose_name="Ruscha atama")
    definition = models.TextField(verbose_name="Ta’rif")

    class Meta:
        verbose_name = "Glossariy atamasi"
        verbose_name_plural = "Glossariy atamalari"
        ordering = ["term_uz"]

    def __str__(self):
        return self.term_uz