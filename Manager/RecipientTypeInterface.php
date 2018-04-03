<?php

interface Notification_Manager_RecipientTypeInterface {

	/**
	 * Return a list of recipients.
	 *
	 * This must be in the form of a list of arrays with at least the following
	 * keys each: 'NAME', 'EMAIL'.
	 *
	 * The list may be empty, in which case the email will not be sent.
	 *
	 * Additional notification processor types may require additional fields to
	 * be present.
	 *
	 * @param int $instanceId
	 * @return array
	 *
	 */
	public function getRecipients($instanceId);

	/**
	 * Return the translated name of this recipient type.
	 *
	 * This will be used for display purposes in the admin.
	 *
	 * @return string
	 */
	public function getTranslatedName();
}
