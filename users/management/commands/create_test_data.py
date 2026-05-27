from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import Skill, User


class Command(BaseCommand):
    help = 'Создаёт тестовые данные для проверки проекта'

    def handle(self, *args, **kwargs):
        # навыки
        skill_names = ['Python', 'Django', 'JavaScript', 'React', 'PostgreSQL', 'Docker', 'Git', 'REST API']
        skills = {}
        for name in skill_names:
            s, _ = Skill.objects.get_or_create(name=name)
            skills[name] = s

        # суперпользователь
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                name='Администратор',
                surname='Сайта',
            )
            self.stdout.write('Создан admin@example.com / admin123')

        # тестовые пользователи
        users_data = [
            {
                'email': 'ivanov@example.com',
                'password': 'test123',
                'name': 'Иван',
                'surname': 'Иванов',
                'about': 'Backend-разработчик, люблю Python и всё что с ним связано. Ищу команду для пет-проектов.',
                'phone': '+7 (999) 123-45-67',
                'github_url': 'https://github.com/ivanov-dev',
                'skills': ['Python', 'Django', 'PostgreSQL', 'Git'],
            },
            {
                'email': 'petrova@example.com',
                'password': 'test123',
                'name': 'Мария',
                'surname': 'Петрова',
                'about': 'Занимаюсь фронтендом уже 2 года. Хочу попробовать себя в fullstack-разработке.',
                'github_url': 'https://github.com/mpetrova',
                'skills': ['JavaScript', 'React'],
            },
            {
                'email': 'sidorov@example.com',
                'password': 'test123',
                'name': 'Алексей',
                'surname': 'Сидоров',
                'about': 'DevOps, увлекаюсь автоматизацией и настройкой CI/CD. Иногда пишу на Python.',
                'phone': '+7 (900) 000-11-22',
                'skills': ['Docker', 'Git', 'Python'],
            },
            {
                'email': 'kozlova@example.com',
                'password': 'test123',
                'name': 'Анна',
                'surname': 'Козлова',
                'about': 'Студентка, изучаю Django. Ищу проект где можно получить первый опыт.',
                'github_url': 'https://github.com/anna-k',
                'skills': ['Python', 'Django', 'REST API'],
            },
        ]

        created_users = {}
        for data in users_data:
            email = data['email']
            if not User.objects.filter(email=email).exists():
                user_skills = data.pop('skills')
                pw = data.pop('password')
                user = User.objects.create_user(password=pw, **data)
                for sk in user_skills:
                    user.skills.add(skills[sk])
                self.stdout.write(f'Создан {email}')
            else:
                user = User.objects.get(email=email)
                self.stdout.write(f'Уже существует {email}')
            created_users[email] = user

        ivan = created_users['ivanov@example.com']
        maria = created_users['petrova@example.com']
        alex = created_users['sidorov@example.com']
        anna = created_users['kozlova@example.com']

        # проекты
        projects_data = [
            {
                'owner': ivan,
                'name': 'Трекер задач для учёбы',
                'description': 'Простой таск-менеджер для студентов на Django + PostgreSQL. '
                               'Нужен кто-то на фронтенд, у меня с JS не очень.',
                'status': 'open',
                'github_url': 'https://github.com/ivanov-dev/task-tracker',
            },
            {
                'owner': ivan,
                'name': 'Парсер вакансий с HH.ru',
                'description': 'Скрипт для сбора вакансий и вывода статистики по зарплатам. '
                               'Сделал для себя, хочу развить в полноценный сервис.',
                'status': 'open',
            },
            {
                'owner': maria,
                'name': 'Портфолио-конструктор',
                'description': 'Генератор красивых страниц-портфолио без навыков программирования. '
                               'Ищу бекендера для хранения данных.',
                'status': 'open',
            },
            {
                'owner': alex,
                'name': 'Мониторинг серверов',
                'description': 'Небольшая система для слежения за состоянием нескольких серверов. '
                               'Хочу добавить веб-интерфейс, нужна помощь с Django.',
                'status': 'open',
            },
            {
                'owner': alex,
                'name': 'Telegram-бот напоминалка',
                'description': 'Бот для постановки задач себе и команде через Telegram. Закрыли, '
                               'так как нашли похожее готовое решение.',
                'status': 'closed',
            },
            {
                'owner': anna,
                'name': 'Каталог рецептов',
                'description': 'Учебный проект — сайт с рецептами на Django. '
                               'Буду рада любой помощи и code-review.',
                'status': 'open',
            },
        ]

        for data in projects_data:
            if not Project.objects.filter(name=data['name'], owner=data['owner']).exists():
                Project.objects.create(**data)
                self.stdout.write(f"Создан проект «{data['name']}»")

        # добавляем участников
        tracker = Project.objects.filter(name='Трекер задач для учёбы').first()
        if tracker:
            for u in [maria, anna]:
                if u not in tracker.participants.all():
                    tracker.participants.add(u)

        portfolio = Project.objects.filter(name='Портфолио-конструктор').first()
        if portfolio and ivan not in portfolio.participants.all():
            portfolio.participants.add(ivan)

        self.stdout.write(self.style.SUCCESS('\nВсё создано! Можно заходить:'))
        self.stdout.write('  admin@example.com / admin123  (админ)')
        self.stdout.write('  ivanov@example.com / test123')
        self.stdout.write('  petrova@example.com / test123')
        self.stdout.write('  sidorov@example.com / test123')
        self.stdout.write('  kozlova@example.com / test123')
