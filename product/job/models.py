from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver



class MailToAddress(models.Model):
    full_name = models.CharField('Фамилия, имя, отчество', max_length=100, null=False, blank=False)
    email_address = models.EmailField('Адрес электронной почты', null=False, blank=False)

    class Meta():
        verbose_name = 'Адресаты - получатели эл. анкет'
        verbose_name_plural = 'Адресаты - получатели эл. анкет'

    def __str__(self):
        return '{} {}'.format(self.full_name, self.email_address)


class Location(models.Model):
    loc_id = models.CharField('Идентификатор', max_length=20, null=False, blank=False)
    describe = models.CharField('Наименование', max_length=100, null=True, blank=True, default='')
    mail_to = models.ManyToManyField(MailToAddress, verbose_name='Получатели почты', related_name='locations', blank=True)

    class Meta():
        verbose_name = 'Справочник: АРМ анкетирования'
        verbose_name_plural = 'Справочник: АРМ анкетирования'

    def __str__(self):
        return '{} {}'.format(self.loc_id, self.describe)


class Person(models.Model):
    fill_location = models.ForeignKey(Location, verbose_name='Место заполнения', null=True, blank=True, on_delete=models.SET_NULL)

    fill_date = models.DateField('Дата заполнения',auto_now_add=True)

    position = models.CharField('Должность',max_length=50)
    full_name = models.CharField('Фамилия, имя, отчество',max_length=100)
    birthday = models.DateField('Дата рождения', null=True, blank=True)

    gender_set = (
        ('0', 'Мужской'),
        ('1', 'Женский'),
    )
    gender = models.CharField('Пол', max_length=1, choices=gender_set, default='', blank=True)

    registration = models.TextField('Адрес прописки', default='', blank=True)
    residenceBool = models.BooleanField('Адрес проживания совпадает с адресом прописки', default=True, blank=True)

    phone = models.CharField('Мобильный телефон',max_length=15, default='', blank=True)

    civil_status_set = (
        ('Женат/Замужем', 'Женат/Замужем'),
        ('Не женат/Не замужем', 'Не женат/Не замужем'),
    )
    civil_status = models.CharField('Семейное положение', max_length=20, choices=civil_status_set, default='', blank=True)
    # children = models.BooleanField('Дети', default=False)

    quant_children_set = (
        (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
    )
    quant_children = models.IntegerField('Количество детей', choices=quant_children_set, default=0)

    passp_number = models.CharField('Серия, номер паспорта',max_length=20, default='', blank=True)
    passp_issue = models.CharField('Кем выдан',max_length=255, default='', blank=True)
    passp_date = models.DateField('Дата выдачи', null=True, blank=True)

    army = models.BooleanField('Служба в армии', default=False)
    army_id = models.BooleanField('Военный билет', default=False)
    driver_lic = models.BooleanField('Водительское удостоверение', default=False)
    car = models.BooleanField('Личный автомобиль', default=False)

    advantage = models.TextField('Ваши сильные стороны', default='', blank=True)
    disadvantage = models.TextField('Ваши слабые стороны', default='', blank=True)
    convicted = models.BooleanField('Привлекались ли Вы к ответственности (административной, уголовной и т.д.)', default=False, blank=True)
    illness = models.BooleanField('Страдаете ли Вы хроническими заболеваниями?', default=False, blank=True)
    salary = models.CharField('Какую заработную плату Вы хотите получать?', max_length=10, default="", blank=True)

    # Section: Other
        # referrer first
    ref1_full_name = models.CharField('Фамилия, имя, отчество',max_length=100, default='', blank=True)
    ref1_position = models.CharField('Должность',max_length=50, default='', blank=True)
    ref1_workplace = models.CharField('Место работы', max_length=100, default='', blank=True)
    ref1_phone = models.CharField('Мобильный телефон',max_length=15, default='', blank=True)
        # referrer second
    ref2_full_name = models.CharField('Фамилия, имя, отчество', max_length=100, default='', blank=True)
    ref2_position = models.CharField('Должность', max_length=50, default='', blank=True)
    ref2_workplace = models.CharField('Место работы', max_length=100, default='', blank=True)
    ref2_phone = models.CharField('Мобильный телефон', max_length=15, default='', blank=True)

    source_about_as = models.CharField('Из какого источника узнали о вакансии',max_length=50, default='', blank=True)
    add_details = models.TextField('Дополнительные сведения, которые Вы желаете сообщить о себе', default='', blank=True)

    start = models.DateField('Когда Вы можете начать работать', null=True, blank=True)

    email_send = models.BooleanField('Анкета отправлена почтой', default=False, editable=False)


    class Meta():
        verbose_name = 'Анкеты соискателей'
        verbose_name_plural = 'Анкеты соискателей'

    def __str__(self):
        return '{} : {}'.format(self.full_name, self.position)

    def last_state(self):
        state = self.cvstate_set.all().latest()
        return state.status.get_status_display()
    last_state.short_description = 'Статус анкеты'

    def cv_state(self):
        state = self.cvstate_set.all().latest()
        return state

class Residence_address(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    residence = models.TextField('Адрес проживания', default='', blank=True)

    class Meta():
        verbose_name = 'Адрес проживания'
        verbose_name_plural = 'Адрес проживания'

    def __str__(self):
        return '{} {}'.format('адрес', self.person.full_name)

class Education(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    start_date = models.DateField('Начало обучения', null=True, blank=True)
    end_date = models.DateField('Окончание обучения', null=True, blank=True)
    name_institute = models.TextField('Название учебного заведения, факультет, форма обучения', default='', blank=True)
    qualification = models.CharField('Специальность', max_length=50, default='', blank=True)

    class Meta():
        verbose_name = 'Образование и специальность'
        verbose_name_plural = 'Образование и специальность'

    def __str__(self):
        return '{} {}'.format('Образование', self.person.full_name)


class Experience(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    exp_start_date = models.DateField('Период работы с', null=True, blank=True)
    exp_end_date = models.DateField('Период работы по', null=True, blank=True)
    workplace = models.CharField('Место работы', max_length=100, default='', blank=True)
    exp_position = models.CharField('Должность', max_length=100, default='', blank=True)
    responsibility = models.TextField('Обязанности', max_length=100,default='', blank=True)
    exp_salary = models.CharField('Зарплата', max_length=10, default="", blank=True)
    reason_leaving = models.TextField('Причина увольнения',max_length=100, default='', blank=True)

    class Meta():
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'

    def __str__(self):
        return '{} {}'.format('Опыт работы', self.person.full_name)



class MailBackSettings(models.Model):

    email_host = models.CharField('EMAIL_HOST (сервер)', max_length=50, default='smtp.product.in.ua', blank=False)
    email_host_user = models.EmailField('EMAIL_HOST_USER', max_length=50, default='product@product.in.ua', blank=False)
    email_host_password = models.CharField('EMAIL_HOST_PASSWORD', max_length=50, default='A126YzSd6Kjm9At', blank=False)
    email_port = models.IntegerField('EMAIL_PORT', default=587, blank=False)
    email_use_tls = models.BooleanField('Использовать TLS', default=False, blank=False)
    description = models.CharField('Описание настроек отправки почты', max_length=100, default='', blank=True)
    default = models.BooleanField('Использовать по умоланию', default=False)

    class Meta():
        verbose_name = 'Настройки: отправки эл. почты'
        verbose_name_plural = 'Настройки: отправки эл. почты'

    def __str__(self):
        return 'EMAIL_HOST (сервер):{}, EMAIL_HOST_USER:{}'.format(self.email_host, self.email_host_user)



class CvStatusName(models.Model):
    status_name_set = (
        (0, 'Новое'),
        (1, 'Просмотренное'),
        (2, 'Собеседование'),
        (3, 'Принят'),
        (4, 'НЕ принят'),
        (5, 'Архив')
    )

    status = models.PositiveSmallIntegerField('Статус резюме', choices=status_name_set, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Справочник: Статусы анкеты"
        verbose_name_plural = "Справочник: Статусы анкеты"

    def __str__(self):
        return '{}'.format(self.get_status_display())



class CvState(models.Model):
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    cv = models.ForeignKey(Person, verbose_name='ID Person', on_delete=models.CASCADE)
    status = models.ForeignKey(CvStatusName, verbose_name='Статус', on_delete=models.SET_NULL, null=True)
    user_set = models.ForeignKey(User, related_name='setter', verbose_name='Установил статус', on_delete=models.SET_NULL, blank=True, null=True)
    user_responsible = models.ForeignKey(User, related_name='getter', verbose_name='Кому назначено', on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField('Комментарий', max_length=200, default='', blank=False, null=True)

    class Meta:
        verbose_name = "Статусы анкет"
        verbose_name_plural = "Статусы анкет"
        get_latest_by = "date"

    def __str__(self):
        return "{} - {}".format(self.cv.full_name, self.cv.position)

    def full_name(self):
        return self.cv.full_name
    full_name.short_description = 'ФИО'

    def position(self):
        return self.cv.position
    full_name.short_description = 'Должность'

