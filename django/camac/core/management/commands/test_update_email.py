import pytest
from django.core.management import call_command


@pytest.mark.parametrize(
    "user__username,new_mail,new_active_state,disabled",
    [
        ("testuser", "updatedmail@test.ch", "x", False),
        ("testuser", "updatedmail@test.ch", "X", False),
        ("testuser", "updatedmail@test.ch", "otherstring", True),
        ("testuser", "updatedmail@test.ch", "", True),
    ],
)
def test_update_email(db, capsys, user, tmp_path, new_mail, new_active_state, disabled):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(f",,{user.username},,,{new_mail},{new_active_state}")

    call_command("update_email", str(csv_file))

    user.refresh_from_db()
    assert user.email == new_mail
    assert user.disabled == disabled

    captured = capsys.readouterr()
    assert user.username in captured.out


def test_update_email_missing_users(db, capsys, user, tmp_path):
    user.username = "existinguser"
    user.save()

    csv_username = "notexistinguser"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(f",,{csv_username},,,,")

    with pytest.raises(SystemExit) as we:
        call_command("update_email", str(csv_file))
    assert we.value.code == 1

    captured = capsys.readouterr()
    assert user.username in captured.out
