from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    # Создает нового пользователя с заданным именем пользователя, адресом электронной почты и паролем.
    # Любые дополнительные поля могут быть переданы в качестве необязательных аргументов.
    def create_user(self, username, email, password=None, **extra_fields):
        # Создаем экземпляр модели пользователя, заполняя обязательные поля (имя пользователя и адрес электронной почты).
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        # Устанавливаем пароль для пользователя.
        user.set_password(password)
        # Сохраняем пользователя в базе данных, используя текущую базу данных (self._db).
        user.save(using=self._db)
        # Возвращаем созданного пользователя.
        return user

    # Создает нового суперпользователя с заданным именем пользователя, адресом электронной почты и паролем.
    # Любые дополнительные поля могут быть переданы в качестве необязательных аргументов.
    def create_superuser(self, username, email, password=None, **extra_fields):
        # Устанавливаем некоторые стандартные значения для дополнительных полей.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Проверяем, что is_staff=True для суперпользователя, в противном случае вызываем ошибку.
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        # Проверяем, что is_superuser=True для суперпользователя, в противном случае вызываем ошибку.
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        # Создаем суперпользователя, используя метод create_user, передавая ему переданные аргументы.
        user = self.create_user(username, email, password, **extra_fields)
        # Устанавливаем атрибут is_staff в True для суперпользователя.
        setattr(user, 'is_staff', True)

        # Возвращаем созданного суперпользователя.
        return user


class MyUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
        unique=True,
    )
    first_name = models.CharField(
        max_length=155,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=155,
        verbose_name='Фамилия'
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def str(self):
        return self.username



class Category(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def str(self):
        return self.name

def upload_to(instance, filename):
    return 'images/' + filename


class UserImage(models.Model):
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(
        max_length=80, blank=False, null=False)
    description = models.TextField()
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    user_image = models.ForeignKey(UserImage, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def str(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    count_of_views = models.PositiveIntegerField(default=0)
    count_of_like = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def str(self):
        return self.title


class Comment(models.Model):
    body = models.TextField(max_length=1000)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def str(self):
        return f"{self.post.title} {self.body[:20]}"