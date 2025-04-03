from django.conf import settings

from camac.eeba_integration import utils

EEBA_HIDDEN_QUESTIONS_SLUGS = settings.APPLICATION.get(
    "EEBA_HIDDEN_QUESTIONS_SLUGS", {}
)


class EebaIntegrationState:
    """
    Manage EEBA integration state.

    Retrieve and store answers of a document for predefined hidden question slugs.
    """

    def __init__(self, document):
        """
        Initialize a new instance of EebaIntegrationState.

        This constructor sets up the slugs used to store and retrieve
        various EEBA integration fields for the provided document.

        Args:
            document: The document object related to the EEBA answers.
        """
        self.document = document
        self.integration_id_slug = EEBA_HIDDEN_QUESTIONS_SLUGS.get(
            "integration_id", "eeba-integration-id"
        )
        self.state_slug = EEBA_HIDDEN_QUESTIONS_SLUGS.get("state", "eeba-state")
        self.required_slug = EEBA_HIDDEN_QUESTIONS_SLUGS.get(
            "required", "eeba-required"
        )
        self.web_url_slug = EEBA_HIDDEN_QUESTIONS_SLUGS.get("web_url", "eeba-web-url")

    def get_integration_id(self):
        """
        Retrieve the integration ID for the document.

        Returns:
            The integration ID stored for the document, or None if not found.
        """
        return utils.get_answer(self.integration_id_slug, self.document)

    def set_integration_id(self, integration_id):
        """
        Save the integration ID for the document.

        Args:
            integration_id: The integration ID value to save.

        Returns:
            The result of the save operation, as provided by utils.save_answer.
        """
        return utils.save_answer(
            self.document, self.integration_id_slug, integration_id
        )

    def get_state(self):
        """
        Retrieve the state value for the document.

        Returns:
            The state value stored for the document, or None if not set.
        """
        return utils.get_answer(self.state_slug, self.document)

    def set_state(self, state_value):
        """
        Save the state value for the document.

        Args:
            state_value: The state value to save.

        Returns:
            The result of the save operation, as provided by utils.save_answer.
        """
        return utils.save_answer(self.document, self.state_slug, state_value)

    def get_required(self):
        """
        Retrieve the eeba-required value for the document.

        Returns:
            The value of the eeba-required field stored for the document, or None if not set.
        """
        return utils.get_answer(self.required_slug, self.document)

    def set_required(self, required_value):
        """
        Save the eeba-required value for the document.

        Args:
            required_value: The value to be saved as the required flag.

        Returns:
            The result of the save operation, as provided by utils.save_answer.
        """
        return utils.save_answer(self.document, self.required_slug, required_value)

    def get_web_url(self):
        """
        Retrieve the web URL for the document.

        Returns:
            The web URL stored for the document, or None if not set.
        """
        return utils.get_answer(self.web_url_slug, self.document)

    def set_web_url(self, web_url):
        """
        Save the web URL for the document.

        Args:
            web_url: The web URL to be saved.

        Returns:
            The result of the save operation, as provided by utils.save_answer.
        """
        return utils.save_answer(self.document, self.web_url_slug, web_url)
