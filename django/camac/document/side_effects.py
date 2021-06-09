from django.conf import settings


def on_attachment_download(attachment, request):
    if settings.APPLICATION_NAME != "kt_uri":
        return
    __import__("remote_pdb").RemotePdb("0.0.0.0", 5555).set_trace()
    # check if file is downloaded by gesuchsteller
    # check if buttons are pressed
    # write workflow entry for pressed buttons if it doesnt exist yet
