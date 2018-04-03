<?php

interface Notification_Manager_ProcessorInterface {

	/**
	 * Process the given notification.
	 *
	 * The $recipient parameter is an array containing the attributes of the
	 * recipient.  Note this may be called multiple times if there are multiple
	 * recipients. The following fields are guaranteed to be present: 'NAME', 'EMAIL'.
	 * Other fields may be present depending on the recipient type that generated
	 * the data.
	 *
	 * The $data parameter is an array containing the attributes to be processed.
	 * The fields given here are at the minimum: 'LANGUAGE', 'BODY', and 'SUBJECT'.
	 *
	 * To parse the contents, you can use the `Notification_Manager_Parser` class.
	 *
	 * Return TRUE if processing went sucessfully, FALSE otherwise.
	 *
	 * TODO: store error somewhere?
	 *
	 * @param int $instanceId
	 * @param array $recipient
	 * @param array $template
	 * @return bool
	 *
	 */
	public function process($instanceId, $recipient, $data);

	/**
	 * Return the translated name of this notification processor.
	 *
	 * This will be used for display purposes in the admin.
	 *
	 * @return string
	 */
	public function getTranslatedName();
}
