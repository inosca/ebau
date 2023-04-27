import pytest

from django.urls import reverse

@pytest.mark.parametrize(
    "role",
    [
        ("applicant",),
        ("municipality",),
        ("service",),
    ],
)
def test_document_visibility(db, role):
    url = reverse("document-list")

def test_file_visibility(db, role):
    url = reverse("file-list")

def test_category_visibility(db, role):
    url = reverse("category-list")

@pytest.mark.parametrize(
    "role",
    [
        ("applicant",),
        ("municipality",),
        ("service",),
        ("support",),
    ],
)
def test_tag_visibility(db, role):
    url = reverse("tag-list")

    

