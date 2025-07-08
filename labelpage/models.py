from django.db import models
from django.contrib.auth.models import User
from homepage.models import CsvData

class Label(models.Model):
    LABEL_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal'),
    ]

    ABNORMAL_SUB_CHOICES = [
        ('Super voider', 'Super voider'),
        ('Compressive', 'Compressive'),
        ('Constrictive', 'Constrictive'),
        ('Interrupted', 'Interrupted'),
        ('Staccato', 'Staccato'),
    ]


    csv_data = models.ForeignKey(CsvData, on_delete=models.CASCADE, related_name='labels')
    label_type = models.CharField(max_length=10, choices=LABEL_TYPE_CHOICES)
    abnormal_subtype = models.CharField(max_length=20, choices=ABNORMAL_SUB_CHOICES, null=True, blank=True)
    labeled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='labeled_entries')
    label_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('csv_data', 'labeled_by'),)
        constraints = [
            models.UniqueConstraint(fields=['csv_data', 'labeled_by'], name='unique_csv_labeled_by')
        ]


    def __str__(self):
        return f"{self.label_type} by {self.labeled_by.username} on {self.label_time}"
    