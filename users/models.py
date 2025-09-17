import random
import uuid

from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, send_mail


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self,username,phone_number ,email, password,is_staff,is_superuser , **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The username must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined = now ,**extra_fields)
        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number[-7:])
            while User.objects.filter(username=username).exists():
                username = username + str(random.randint(10,99))

        return self._create_user(username, phone_number, email, password,False, False ,**extra_fields)

    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**({'phone_number': phone_number}))

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=32, unique=True,
                                help_text=_('Required. 32 characters or fewer. Letters, digits and '),
                                validators=[
                                    validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                    _('Enter a valid username.'), 'invalid')
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                }
                                )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(_('phone number'), unique=True, null=True, blank=True,
                                    validators=[
                                        # TODO: use utils.validators
                                        validators.RegexValidator(r'^989[0-3,9]\d{8}$', _('Enter a valid phone number.') , 'invalid'),
                                    ],
                                    error_messages={
                                        'unique': _("A user with that phone number already exists."),
                                    }
                                    )
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        short_name = '%s %s' % (self.first_name, self.last_name)
        return short_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_longgedin_user(self):

        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if not self.email or self.email.strip() == '':
            self.email = None

        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_('nick name'), max_length=30, blank=True)
    avatar = models.ImageField(_('avatar'), null=True, blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.CharField(_('gender'), help_text=_('female is False, male is True, null is unset'))
    province = models.ForeignKey(verbose_name=_('province'), to='Province',null=True, on_delete=models.SET_NULL)
    #email = models.EmailField(_('email address'), null=True, blank=True)
    #phone_number .....

    class Meta:
        db_table = 'user_profile'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    @property
    def get_first_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    def get_nick_name(self):
        return self.user.nick_name if self.user.nick_name else self.user.username

class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )
    user = models.ForeignKey(verbose_name=_('user'), to='User', on_delete=models.CASCADE)

    device_uuid = models.UUIDField(
        _('device uuid'),
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    last_login = models.DateTimeField(_('last login'), null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE_CHOICES, default=WEB)
    device_os = models.CharField(_('device os'), max_length=30, null=True, blank=True)
    devic_model = models.CharField(_('devic model'), max_length=30, null=True, blank=True)
    app_version = models.CharField(_('app version'), max_length=30, null=True, blank=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    class Meta:
        db_table = 'devices'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together = ('user', 'device_uuid')

class Province(models.Model):
    name = models.CharField(_('province'), max_length=30)
    is_valid =models.BooleanField(_('is valid'), default=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def __str__(self):
        return self.name
