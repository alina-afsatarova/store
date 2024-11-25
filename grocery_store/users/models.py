from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    """Пользователь."""
    pass


class CustomGroup(Group):

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'Группы'
        proxy = True
