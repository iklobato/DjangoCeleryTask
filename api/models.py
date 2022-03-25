from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class CeleryTask(models.Model):
    task_name = models.CharField(max_length=100)
    task_status = models.BooleanField(default=False)
    payload = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ('-date_created',)

