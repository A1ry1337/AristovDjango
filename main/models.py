from django.db import models


class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    key_skills = models.TextField()  # Может потребоваться изменить тип поля, в зависимости от ваших требований
    salary = models.FloatField(null=True)  # Используем одно поле для хранения средней зарплаты
    salary_currency = models.CharField(max_length=10)
    area_name = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    time = models.DateTimeField()
