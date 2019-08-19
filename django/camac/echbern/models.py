# from django.db import models
#
#
# class Message(models.Model):
#     STATUS_OPEN = "open"
#     STATUS_SUCCESS = "success"
#     STATUS_ERROR = "error"
#
#     STATUS_CHOICES = (
#         STATUS_OPEN,
#         STATUS_SUCCESS,
#         STATUS_ERROR,
#     )
#     STATUS_CHOICES_TUPLE = ((type_choice, type_choice) for type_choice in STATUS_CHOICES)
#
#     body = models.TextField(help_text="XML body")
#     status = models.CharField(choices=STATUS_CHOICES_TUPLE, max_length=7)
#     created_at = models.DateTimeField(auto_now_add=True)
#     sent_at = models.DateTimeField(null=True, blank=True)
#     receiver = models.ForeignKey('user.service', on_delete=models.PROTECT)
#
#     class Meta:
#         managed = True
