import os
import time

from django.core.management import call_command


def test_cleanup_tempfiles(mocker, tmp_path, settings):
    settings.TEMPFILE_DOWNLOAD_PATH = str(tmp_path)
    threshold = time.time() - settings.TEMPFILE_RETENTION_TIME

    # create some files and directories
    # - file1.zip (old)
    # - file2.zip (old)
    # - file3.zip
    # \ subfolder
    # | - file1.pdf (old)
    #  \ subsub
    #  | - someotherfile.jpg (old)
    # \ another-folder
    # | - file1.zip (old)
    # | - file2.zip

    file1 = tmp_path / "file1.zip"
    file2 = tmp_path / "file2.zip"
    file3 = tmp_path / "file3.zip"
    file1.touch()
    file2.touch()
    file3.touch()

    subdir1 = tmp_path / "subfolder"
    subdir1.mkdir()
    file1_1 = subdir1 / "file1.pdf"
    file1_1.touch()

    subdir2 = tmp_path / "another-folder"
    subdir2.mkdir()
    file2_1 = subdir2 / "file1.zip"
    file2_2 = subdir2 / "file2.zip"
    file2_1.touch()
    file2_2.touch()

    subsubdir = subdir1 / "subsub"
    subsubdir.mkdir()
    file1_1_1 = subsubdir / "someotherfile.jpg"
    file1_1_1.touch()

    # make files 1000 seconds older than threshold
    mtime = (threshold - 1000, threshold - 1000)

    os.utime(file1, mtime)
    os.utime(file2, mtime)
    os.utime(file1_1, mtime)
    os.utime(file2_1, mtime)
    os.utime(file1_1_1, mtime)

    call_command("cleanup_tempfiles")

    assert all(dir.exists() for dir in [subdir1, subdir2, subsubdir])
    assert file3.exists()
    assert file2_2.exists()
    assert not file1.exists()
    assert not file2.exists()
    assert not file1_1.exists()
    assert not file2_1.exists()
    assert not file1_1_1.exists()
