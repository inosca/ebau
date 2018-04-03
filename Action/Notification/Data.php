<?php

class Notification_Action_Notification_Data extends Camac_Model_Data_Resource_Action {

	/**
	 * Translate between DB fields and model attributes.
	 *
	 * Used by the Camac_Model_Data_Resource_Action::fromArray() method
	 */
	const PROPERTIES_IN_DB = [
		'AVAILABLE_ACTION_ID' => 'availableActionId',
		'BUTTON_ID'           => 'buttonId',
		'EXECUTE_ALWAYS'      => 'executeAlways',
		'SORT'                => 'sort',
		'NAME'                => 'name',
		'DESCRIPTION'         => 'description',
		'SUCCESS_MESSAGE'     => 'successMessage',
		'ERROR_MESSAGE'       => 'errorMessage',
		'ACTION_ID'           => 'actionId',
		'TEMPLATE_ID'         => 'templateId',
		'PROCESSOR'           => 'processor',
		'RECIPIENT_TYPE'      => 'recipientType',
	];

	public $templateId;
	public $processor;
	public $recipientType;

	public function __construct($actionId, $availableActionId, $buttonId, $name, $description, $successMessage, $errorMessage, $executeAlways, $sort, $templateId, $processor, $recipientType, $language = null) {
		parent::__construct($actionId, $availableActionId, $buttonId, $name, $description, $successMessage, $errorMessage, $executeAlways, $sort, $language = null);

		$this->templateId    = $templateId;
		$this->processor     = $processor;
		$this->recipientType = $recipientType;
	}
}
