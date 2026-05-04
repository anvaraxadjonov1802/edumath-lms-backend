from django.core.management.base import BaseCommand

from courses.models import (
    Answer,
    Course,
    GlossaryTerm,
    Module,
    Question,
    Reference,
    Topic,
)


class Command(BaseCommand):
    help = "Create initial demo data for EduMath LMS"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding initial data..."))

        course, _ = Course.objects.update_or_create(
            slug="iqtisodchilar-uchun-matematika",
            defaults={
                "title": "Iqtisodchilar uchun matematika",
                "description": (
                    "Ushbu kurs iqtisodiyot yo‘nalishida tahsil oluvchi talabalar "
                    "uchun matematika fanini nazariy, amaliy va test shaklida "
                    "o‘rganishga mo‘ljallangan elektron ta’lim kursidir."
                ),
                "is_active": True,
            },
        )

        module_1, _ = Module.objects.update_or_create(
            course=course,
            slug="1-qism",
            defaults={
                "title": "1-qism",
                "description": "Iqtisodchilar uchun matematika fanining birinchi qismi.",
                "order": 1,
                "is_active": True,
            },
        )

        module_2, _ = Module.objects.update_or_create(
            course=course,
            slug="2-qism",
            defaults={
                "title": "2-qism",
                "description": "Iqtisodchilar uchun matematika fanining ikkinchi qismi.",
                "order": 2,
                "is_active": True,
            },
        )

        topics_1 = [
            {
                "title": "1-mavzu: Matritsalar va ular ustida amallar",
                "slug": "1-mavzu-matritsalar-va-ular-ustida-amallar",
                "description": (
                    "Matritsa tushunchasi, matritsalar turlari, matritsalarni qo‘shish, "
                    "ayirish va songa ko‘paytirish amallari o‘rganiladi."
                ),
                "order": 1,
            },
            {
                "title": "2-mavzu: Determinantlar",
                "slug": "2-mavzu-determinantlar",
                "description": (
                    "Determinant tushunchasi, determinantni hisoblash usullari va "
                    "uning asosiy xossalari o‘rganiladi."
                ),
                "order": 2,
            },
            {
                "title": "3-mavzu: Chiziqli tenglamalar sistemasi",
                "slug": "3-mavzu-chiziqli-tenglamalar-sistemasi",
                "description": (
                    "Chiziqli tenglamalar sistemasi, Kramer usuli, Gauss usuli va "
                    "iqtisodiy masalalarda qo‘llanilishi ko‘rib chiqiladi."
                ),
                "order": 3,
            },
            {
                "title": "4-mavzu: Vektorlar va ular ustida amallar",
                "slug": "4-mavzu-vektorlar-va-ular-ustida-amallar",
                "description": (
                    "Vektor tushunchasi, vektorlar ustida amallar va ularning "
                    "geometrik hamda iqtisodiy talqinlari o‘rganiladi."
                ),
                "order": 4,
            },
            {
                "title": "5-mavzu: Analitik geometriya elementlari",
                "slug": "5-mavzu-analitik-geometriya-elementlari",
                "description": (
                    "Tekislikdagi to‘g‘ri chiziq, nuqta va chiziqlarning o‘zaro "
                    "joylashuvi, masofa va burchak tushunchalari o‘rganiladi."
                ),
                "order": 5,
            },
        ]

        topics_2 = [
            {
                "title": "16-mavzu: Sonli ketma-ketliklar",
                "slug": "16-mavzu-sonli-ketma-ketliklar",
                "description": (
                    "Sonli ketma-ketlik, uning limiti, yaqinlashuvchi va uzoqlashuvchi "
                    "ketma-ketliklar tushunchasi o‘rganiladi."
                ),
                "order": 1,
            },
            {
                "title": "17-mavzu: Bir va ko‘p o‘zgaruvchili funksiyalar",
                "slug": "17-mavzu-bir-va-kop-ozgaruvchili-funksiyalar",
                "description": (
                    "Funksiya tushunchasi, ko‘p o‘zgaruvchili funksiyalar va "
                    "Kobb-Duglas funksiyasining iqtisodiy talqini o‘rganiladi."
                ),
                "order": 2,
            },
            {
                "title": "18-mavzu: Funksiya limiti",
                "slug": "18-mavzu-funksiya-limiti",
                "description": (
                    "Funksiya limiti, limitning asosiy xossalari va limitlarni "
                    "hisoblash usullari ko‘rib chiqiladi."
                ),
                "order": 3,
            },
            {
                "title": "19-mavzu: Hosila va differensial",
                "slug": "19-mavzu-hosila-va-differensial",
                "description": (
                    "Bir o‘zgaruvchili funksiya hosilasi, differensiali va iqtisodiy "
                    "jarayonlardagi marginal tahlil bilan bog‘liqligi o‘rganiladi."
                ),
                "order": 4,
            },
        ]

        created_topics = []

        for topic_data in topics_1:
            topic, _ = Topic.objects.update_or_create(
                module=module_1,
                slug=topic_data["slug"],
                defaults={
                    "title": topic_data["title"],
                    "description": topic_data["description"],
                    "order": topic_data["order"],
                    "is_active": True,
                },
            )
            created_topics.append(topic)

        for topic_data in topics_2:
            topic, _ = Topic.objects.update_or_create(
                module=module_2,
                slug=topic_data["slug"],
                defaults={
                    "title": topic_data["title"],
                    "description": topic_data["description"],
                    "order": topic_data["order"],
                    "is_active": True,
                },
            )
            created_topics.append(topic)

        first_topic = Topic.objects.get(
            module=module_1,
            slug="1-mavzu-matritsalar-va-ular-ustida-amallar",
        )

        question_1, _ = Question.objects.update_or_create(
            topic=first_topic,
            order=1,
            defaults={
                "text": "Matritsa nima?",
                "is_active": True,
            },
        )

        self.create_answers(
            question_1,
            [
                {
                    "text": "Sonlar yoki matematik ifodalardan tashkil topgan to‘g‘ri to‘rtburchak shaklidagi jadval.",
                    "is_correct": True,
                },
                {
                    "text": "Faqat bitta sondan iborat matematik ifoda.",
                    "is_correct": False,
                },
                {
                    "text": "Faqat geometrik shakllarni ifodalovchi chizma.",
                    "is_correct": False,
                },
                {
                    "text": "Faqat bitta noma’lumli tenglama.",
                    "is_correct": False,
                },
            ],
        )

        question_2, _ = Question.objects.update_or_create(
            topic=first_topic,
            order=2,
            defaults={
                "text": "Matritsalarni qo‘shish uchun qanday shart bajarilishi kerak?",
                "is_active": True,
            },
        )

        self.create_answers(
            question_2,
            [
                {
                    "text": "Matritsalarning satr va ustunlari soni bir xil bo‘lishi kerak.",
                    "is_correct": True,
                },
                {
                    "text": "Matritsalarning determinantlari teng bo‘lishi kerak.",
                    "is_correct": False,
                },
                {
                    "text": "Matritsalardan biri kvadrat matritsa bo‘lishi kerak.",
                    "is_correct": False,
                },
                {
                    "text": "Matritsalarning barcha elementlari musbat bo‘lishi kerak.",
                    "is_correct": False,
                },
            ],
        )

        question_3, _ = Question.objects.update_or_create(
            topic=first_topic,
            order=3,
            defaults={
                "text": "Kvadrat matritsa deb nimaga aytiladi?",
                "is_active": True,
            },
        )

        self.create_answers(
            question_3,
            [
                {
                    "text": "Satrlar soni ustunlar soniga teng bo‘lgan matritsaga.",
                    "is_correct": True,
                },
                {
                    "text": "Faqat nollardan iborat matritsaga.",
                    "is_correct": False,
                },
                {
                    "text": "Faqat bitta satrdan iborat matritsaga.",
                    "is_correct": False,
                },
                {
                    "text": "Faqat bitta ustundan iborat matritsaga.",
                    "is_correct": False,
                },
            ],
        )

        glossary_items = [
            {
                "term_uz": "Matritsa",
                "term_en": "Matrix",
                "term_ru": "Матрица",
                "definition": (
                    "Matritsa — m ta satr va n ta ustundan iborat sonlar yoki "
                    "matematik ifodalar jadvalidir."
                ),
            },
            {
                "term_uz": "Determinant",
                "term_en": "Determinant",
                "term_ru": "Определитель",
                "definition": (
                    "Determinant — kvadrat matritsaga mos keluvchi va uning "
                    "asosiy xossalarini ifodalovchi sonli qiymatdir."
                ),
            },
            {
                "term_uz": "Funksiya",
                "term_en": "Function",
                "term_ru": "Функция",
                "definition": (
                    "Funksiya — bir to‘plamdagi har bir elementga ikkinchi "
                    "to‘plamdan yagona elementni mos qo‘yuvchi qoidadir."
                ),
            },
            {
                "term_uz": "Hosila",
                "term_en": "Derivative",
                "term_ru": "Производная",
                "definition": (
                    "Hosila — funksiya qiymatining argument o‘zgarishiga nisbatan "
                    "o‘zgarish tezligini ifodalaydi."
                ),
            },
            {
                "term_uz": "Limit",
                "term_en": "Limit",
                "term_ru": "Предел",
                "definition": (
                    "Limit — argument ma’lum qiymatga yaqinlashganda funksiya "
                    "qiymatining qanday qiymatga yaqinlashishini ifodalaydi."
                ),
            },
        ]

        for item in glossary_items:
            GlossaryTerm.objects.update_or_create(
                term_uz=item["term_uz"],
                defaults={
                    "term_en": item["term_en"],
                    "term_ru": item["term_ru"],
                    "definition": item["definition"],
                },
            )

        references = [
            {
                "title": "Iqtisodchilar uchun matematika",
                "author": "O‘quv-uslubiy qo‘llanma",
                "year": "2024",
                "description": (
                    "Iqtisodiyot yo‘nalishi talabalari uchun matematika faniga oid "
                    "nazariy va amaliy materiallar."
                ),
            },
            {
                "title": "Oliy matematika asoslari",
                "author": "O‘quv adabiyoti",
                "year": "2022",
                "description": (
                    "Matritsalar, determinantlar, funksiyalar, limit va hosila "
                    "mavzulari bo‘yicha asosiy nazariy manba."
                ),
            },
            {
                "title": "Matematika iqtisodchilar uchun",
                "author": "Elektron o‘quv materiali",
                "year": "2023",
                "description": (
                    "Iqtisodiy masalalarni matematik metodlar orqali yechishga "
                    "qaratilgan o‘quv materiali."
                ),
            },
        ]

        for item in references:
            Reference.objects.update_or_create(
                title=item["title"],
                defaults={
                    "author": item["author"],
                    "year": item["year"],
                    "description": item["description"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Initial data created successfully!"))
        self.stdout.write(self.style.SUCCESS(f"Course: {course.title}"))
        self.stdout.write(self.style.SUCCESS(f"Modules: {course.modules.count()}"))
        self.stdout.write(self.style.SUCCESS(f"Topics: {len(created_topics)}"))
        self.stdout.write(self.style.SUCCESS("Demo questions, answers, glossary and references created."))

    def create_answers(self, question, answers):
        Answer.objects.filter(question=question).delete()

        for answer_data in answers:
            Answer.objects.create(
                question=question,
                text=answer_data["text"],
                is_correct=answer_data["is_correct"],
            )