import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch


def load_wsgi_dav_module():
    module_path = Path(__file__).parents[1] / "wsgi_dav.py"
    spec = importlib.util.spec_from_file_location("test_wsgi_dav", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@patch("camac.wsgi_common.setup_environment")
@patch("camac.wsgi_common.get_dav_application")
def test_dav_application_is_created_on_first_request(
    get_dav_application, setup_environment
):
    dav_application = Mock(return_value=[])
    get_dav_application.return_value = dav_application

    wsgi_dav = load_wsgi_dav_module()

    setup_environment.assert_called_once_with(is_dav=True)
    get_dav_application.assert_not_called()

    environ = {"SCRIPT_NAME": "/app"}
    start_response = Mock()

    assert wsgi_dav.application(environ, start_response) == []
    assert wsgi_dav.application(environ, start_response) == []

    get_dav_application.assert_called_once_with()
    assert dav_application.call_count == 2
    assert environ == {"SCRIPT_NAME": "/app"}
    assert dav_application.call_args_list[0].args[0]["SCRIPT_NAME"] == "/app/dav"
