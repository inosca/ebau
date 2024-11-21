import subprocess

from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "camac.document"

    def ready(self):
        import camac.document.signals  # noqa

        _monkeypatch_sorl()


def _monkeypatch_sorl():
    # Can be removed if/when this PR is merged and released:
    # https://github.com/jazzband/sorl-thumbnail/pull/778
    from sorl.thumbnail.conf import settings
    from sorl.thumbnail.engines.convert_engine import Engine

    def _get_exif_orientation(self, image):
        # This is a straight-up copy of the original function, but it appends '[0]'
        # to the file name. This will tell `identify` to only look at the first
        # page. The other convert calls already do this, but for some reason,
        # it was not done in the _get_exif_orientation() method. Speeds up
        # multi-page calls significantly
        args = settings.THUMBNAIL_IDENTIFY.split()
        args.extend(["-format", "%[exif:orientation]", f'{image["source"]}[0]'])
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        result = p.stdout.read().strip()
        try:
            return int(result)
        except ValueError:
            return None

    Engine._get_exif_orientation = _get_exif_orientation
