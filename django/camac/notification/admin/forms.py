from django.forms import ModelForm

from camac.notification.models import NotificationTemplate, NotificationTemplateT


class NotificationTemplateTForm(ModelForm):
    class Meta:
        model = NotificationTemplateT
        fields = ["purpose", "subject", "body"]
        help_texts = {
            "subject": "Der Vorlagen-Inhalt wird bei einer Notifikation mit den folgenden Platzhaltern verarbeitet: {{INSTANCE_ID}}, {{DOSSIER_NR}}, {{INTERNAL_DOSSIER_LINK}}, {{PUBLIC_DOSSIER_LINK}}, {{CURRENT_SERVICE_DESCRIPTION}}, {{GESUCHSTELLER}}, {{VORHABEN}}, {{PARZELLE}}, {{STREET}}, {{INSTANCE_LOCATION}}, {{CURRENT_SERVICE}}",
            "body": "Der Vorlagen-Inhalt wird bei einer Notifikation mit den folgenden Platzhaltern verarbeitet: {{INSTANCE_ID}}, {{DOSSIER_NR}}, {{INTERNAL_DOSSIER_LINK}}, {{PUBLIC_DOSSIER_LINK}}, {{CURRENT_SERVICE_DESCRIPTION}}, {{GESUCHSTELLER}}, {{VORHABEN}}, {{PARZELLE}}, {{STREET}}, {{INSTANCE_LOCATION}}, {{CURRENT_SERVICE}}",
        }


class NotificationTemplateForm(ModelForm):
    class Meta:
        model = NotificationTemplate
        fields = ["slug"]
