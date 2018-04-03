<?php


class Notification_Manager_DefaultPlaceholderSource {

	/**
	 * Parse the template, fill in the values.
	 *
	 * This will return an array with the same structure as was used when creating
	 * the parser (see __construct() above). The values in the array will be parsed
	 * and the placeholders filled.
	 *
	 * @param   int  $instanceId  The ID of the instance for which the template
	 *                            should be rendered
	 * @param   array $recipient  Recipient of the notification. MUST contain
	 *                            EMAIL and NAME at least, but MAY contain more
	 */
	public function getPlaceholders($instanceId, $recipient) {

		// Build placeholder data. The following rules apply:
		// 1) recipient data overrules instance data
		// 2) additional data overrules recipient data
		$data = array_merge(
			$this->getInstanceData($instanceId),
			$recipient
		);

		return $data;
	}

	protected function getInstanceData($instanceId) {

		$mapper = new Application_Model_Mapper_Instance();

		$instance = $mapper->getInstance($instanceId);

		$instanceStateMapper = new Application_Model_Mapper_Resource_InstanceState();
		$instanceState = $instanceStateMapper->getInstanceStateWithInstanceId($instanceId);

		$formId = $instance->getFormId();

		$form = (new Application_Model_Mapper_Form_Form)->getForm($formId);

		$config = Zend_Registry::get('config');
		$dateformat = $config->date->application->phpFormat;

		return [
			'INSTANCE_ID'       => $instance->getInstanceId(),
			'MODIFICATION_DATE' => $instance->getModificationDate()->format($dateformat),
			'MODIFICATION_TIME' => $instance->getModificationDate()->format('H:i'),
			'STATUS'            => $instanceState->getName(),
			'FORM_NAME'         => $form->getName()
		];
	}

	public function getAvailablePlaceholders() {
		return [
			'INSTANCE_ID',
			'MODIFICATION_DATE',
			'MODIFICATION_TIME',
			'STATUS',
			'NAME',
			'EMAIL',
			'FORM_NAME',
		];
	}
}
