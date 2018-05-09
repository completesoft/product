# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-09 07:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CvState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('comment', models.TextField(default='', max_length=200, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name_plural': 'Статусы анкет',
                'verbose_name': 'Статусы анкет',
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='CvStatusName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Новое'), (1, 'Просмотренное'), (2, 'Собеседование'), (3, 'Принят'), (4, 'НЕ принят'), (5, 'Архив')], unique=True, verbose_name='Статус резюме')),
            ],
            options={
                'verbose_name_plural': 'Справочник: Статусы анкеты',
                'verbose_name': 'Справочник: Статусы анкеты',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Начало обучения')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Окончание обучения')),
                ('name_institute', models.TextField(blank=True, default='', verbose_name='Название учебного заведения, факультет, форма обучения')),
                ('qualification', models.CharField(blank=True, default='', max_length=50, verbose_name='Специальность')),
            ],
            options={
                'verbose_name_plural': 'Образование и специальность',
                'verbose_name': 'Образование и специальность',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_start_date', models.DateField(blank=True, null=True, verbose_name='Период работы с')),
                ('exp_end_date', models.DateField(blank=True, null=True, verbose_name='Период работы по')),
                ('workplace', models.CharField(blank=True, default='', max_length=100, verbose_name='Место работы')),
                ('exp_position', models.CharField(blank=True, default='', max_length=100, verbose_name='Должность')),
                ('responsibility', models.TextField(blank=True, default='', max_length=100, verbose_name='Обязанности')),
                ('exp_salary', models.CharField(blank=True, default='', max_length=10, verbose_name='Зарплата')),
                ('reason_leaving', models.TextField(blank=True, default='', max_length=100, verbose_name='Причина увольнения')),
            ],
            options={
                'verbose_name_plural': 'Опыт работы',
                'verbose_name': 'Опыт работы',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_id', models.CharField(max_length=20, verbose_name='Идентификатор')),
                ('describe', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name_plural': 'Справочник: АРМ анкетирования',
                'verbose_name': 'Справочник: АРМ анкетирования',
            },
        ),
        migrations.CreateModel(
            name='MailBackSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_host', models.CharField(default='smtp.product.in.ua', max_length=50, verbose_name='EMAIL_HOST (сервер)')),
                ('email_host_user', models.EmailField(default='product@product.in.ua', max_length=50, verbose_name='EMAIL_HOST_USER')),
                ('email_host_password', models.CharField(default='A126YzSd6Kjm9At', max_length=50, verbose_name='EMAIL_HOST_PASSWORD')),
                ('email_port', models.IntegerField(default=587, verbose_name='EMAIL_PORT')),
                ('email_use_tls', models.BooleanField(default=False, verbose_name='Использовать TLS')),
                ('description', models.CharField(blank=True, default='', max_length=100, verbose_name='Описание настроек отправки почты')),
                ('default', models.BooleanField(default=False, verbose_name='Использовать по умоланию')),
            ],
            options={
                'verbose_name_plural': 'Настройки: отправки эл. почты',
                'verbose_name': 'Настройки: отправки эл. почты',
            },
        ),
        migrations.CreateModel(
            name='MailToAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Фамилия, имя, отчество')),
                ('email_address', models.EmailField(max_length=254, verbose_name='Адрес электронной почты')),
            ],
            options={
                'verbose_name_plural': 'Адресаты - получатели эл. анкет',
                'verbose_name': 'Адресаты - получатели эл. анкет',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fill_date', models.DateField(auto_now_add=True, verbose_name='Дата заполнения')),
                ('position', models.CharField(max_length=50, verbose_name='Должность')),
                ('full_name', models.CharField(max_length=100, verbose_name='Фамилия, имя, отчество')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(blank=True, choices=[('0', 'Мужской'), ('1', 'Женский')], default='', max_length=1, verbose_name='Пол')),
                ('registration', models.TextField(blank=True, default='', verbose_name='Адрес прописки')),
                ('residenceBool', models.BooleanField(default=True, verbose_name='Адрес проживания совпадает с адресом прописки')),
                ('phone', models.CharField(blank=True, default='', max_length=15, verbose_name='Мобильный телефон')),
                ('civil_status', models.CharField(blank=True, choices=[('Женат/Замужем', 'Женат/Замужем'), ('Не женат/Не замужем', 'Не женат/Не замужем')], default='', max_length=20, verbose_name='Семейное положение')),
                ('quant_children', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], default=0, verbose_name='Количество детей')),
                ('passp_number', models.CharField(blank=True, default='', max_length=20, verbose_name='Серия, номер паспорта')),
                ('passp_issue', models.CharField(blank=True, default='', max_length=255, verbose_name='Кем выдан')),
                ('passp_date', models.DateField(blank=True, null=True, verbose_name='Дата выдачи')),
                ('army', models.BooleanField(default=False, verbose_name='Служба в армии')),
                ('army_id', models.BooleanField(default=False, verbose_name='Военный билет')),
                ('driver_lic', models.BooleanField(default=False, verbose_name='Водительское удостоверение')),
                ('car', models.BooleanField(default=False, verbose_name='Личный автомобиль')),
                ('advantage', models.TextField(blank=True, default='', verbose_name='Ваши сильные стороны')),
                ('disadvantage', models.TextField(blank=True, default='', verbose_name='Ваши слабые стороны')),
                ('convicted', models.BooleanField(default=False, verbose_name='Привлекались ли Вы к ответственности (административной, уголовной и т.д.)')),
                ('illness', models.BooleanField(default=False, verbose_name='Страдаете ли Вы хроническими заболеваниями?')),
                ('salary', models.CharField(blank=True, default='', max_length=10, verbose_name='Какую заработную плату Вы хотите получать?')),
                ('ref1_full_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Фамилия, имя, отчество')),
                ('ref1_position', models.CharField(blank=True, default='', max_length=50, verbose_name='Должность')),
                ('ref1_workplace', models.CharField(blank=True, default='', max_length=100, verbose_name='Место работы')),
                ('ref1_phone', models.CharField(blank=True, default='', max_length=15, verbose_name='Мобильный телефон')),
                ('ref2_full_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Фамилия, имя, отчество')),
                ('ref2_position', models.CharField(blank=True, default='', max_length=50, verbose_name='Должность')),
                ('ref2_workplace', models.CharField(blank=True, default='', max_length=100, verbose_name='Место работы')),
                ('ref2_phone', models.CharField(blank=True, default='', max_length=15, verbose_name='Мобильный телефон')),
                ('source_about_as', models.CharField(blank=True, default='', max_length=50, verbose_name='Из какого источника узнали о вакансии')),
                ('add_details', models.TextField(blank=True, default='', verbose_name='Дополнительные сведения, которые Вы желаете сообщить о себе')),
                ('start', models.DateField(blank=True, null=True, verbose_name='Когда Вы можете начать работать')),
                ('email_send', models.BooleanField(default=False, editable=False, verbose_name='Анкета отправлена почтой')),
                ('fill_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.Location', verbose_name='Место заполнения')),
            ],
            options={
                'verbose_name_plural': 'Анкеты соискателей',
                'verbose_name': 'Анкеты соискателей',
            },
        ),
        migrations.CreateModel(
            name='Residence_address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('residence', models.TextField(blank=True, default='', verbose_name='Адрес проживания')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Person')),
            ],
            options={
                'verbose_name_plural': 'Адрес проживания',
                'verbose_name': 'Адрес проживания',
            },
        ),
        migrations.AddField(
            model_name='location',
            name='mail_to',
            field=models.ManyToManyField(blank=True, related_name='locations', to='job.MailToAddress', verbose_name='Получатели почты'),
        ),
        migrations.AddField(
            model_name='experience',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Person'),
        ),
        migrations.AddField(
            model_name='education',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Person'),
        ),
        migrations.AddField(
            model_name='cvstate',
            name='cv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Person', verbose_name='ID Person'),
        ),
        migrations.AddField(
            model_name='cvstate',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.CvStatusName', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='cvstate',
            name='user_responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='getter', to=settings.AUTH_USER_MODEL, verbose_name='Кому назначено'),
        ),
        migrations.AddField(
            model_name='cvstate',
            name='user_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='setter', to=settings.AUTH_USER_MODEL, verbose_name='Установил статус'),
        ),
    ]
