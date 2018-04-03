<?php

class Notification_Action_Notification_Action extends Camac_Action_Action {

	public function __construct($action) {
		parent::__construct($action, false);
	}

	/**
	 * Handles the execution of this action.
	 *
	 * Generate a journal entry and proceed. We assume no failure possible here
	 *
	 * @param boolean $previousSuccess
	 * @return boolean
	 */
	public function handleAction($previousSuccess) {

		$action = $this->getResourceAction();

		if ($action->isAlwaysExecutable() || $previousSuccess) {
			$result = false;

			$pigeon = Camac_Nest_Pigeon::getInstance();

			$this->sendNotification($pigeon->instanceId, $action);
		}

		return parent::handleAction($previousSuccess);
	}

	private function sendNotification($instanceId, $action) {
		$rec  = new $action->recipientType;
		$proc = new $action->processor;

		$templateTable = new Notification_Model_DbTable_TemplateT();

		$template = $templateTable->fetchRow(
			$templateTable
				->select()
				->where($templateTable->getAdapter()->quoteInto('TEMPLATE_ID = ?', $action->templateId))
		)->toArray();

		$recipients = $rec->getRecipients($instanceId);

		foreach($recipients as $recipient) {
			$proc->process($instanceId, $recipient, $template);
		}

	}
}
