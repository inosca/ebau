<?php

class Notification_Action_Notification_Helper_ActionNotification extends Zend_Controller_Action_Helper_Abstract implements Camac_Action_Helper_Interface {

	private $table;
	private $dbAdapter;

	public function __construct() {

		$this->table   = new Notification_Model_DbTable_NotificationAction();

		$this->dbAdapter = $this->table->getAdapter();
	}

	/**
	 * Adds a new action.
	 *
	 * @param int $actionId
	 * @param Notification_Action_ActionConfig_Form $form
	 * @return void
	 */
	public function add($actionId, $form) {

		$action = Notification_Action_Notification_Data::fromArray([
			'actionId'      => $actionId,
			'processor'     => $form->getElement('processor')->getValue(),
			'recipientType' => $form->getElement('recipientType')->getValue(),
			'templateId'    => $form->getElement('template')->getValue(),
		], true);

		$this->table->insert([
			'ACTION_ID'           => $actionId,
			'TEMPLATE_ID'         => $action->templateId,
			'PROCESSOR'           => $action->processor,
			'RECIPIENT_TYPE'      => $action->recipientType,
		]);
	}

	/**
	 * Updates the action.
	 *
	 * @param int $actionId
	 * @param Notification_Action_ActionConfig_Form $form
	 * @return void
	 */
	public function update($actionId, $form) {

		$this->table->update(
			[
			'PROCESSOR'      => $form->getElement('processor')->getValue(),
			'RECIPIENT_TYPE' => $form->getElement('recipientType')->getValue(),
			'TEMPLATE_ID'    => $form->getElement('template')->getValue(),
			],
			$this->dbAdapter->quoteInto('ACTION_ID = ?', $actionId)
		);
	}

	/**
	 * Retrieves the instance of the action.
	 *
	 * @param int $actionId
	 * @param string $language = null
	 * @return Notification_Action_Notification_Data
	 */
	public function getAction($actionId, $language = null) {
		$language = Camac_Utility::getLanguageIfNull($language);

		$select = $this->table->select()
				->from('ACTION_NOTIFICATION', '*')
				->where('ACTION_NOTIFICATION.ACTION_ID = ?', $actionId)
				->setIntegrityCheck(false);

		$select->joinLeft(
			'ACTION',
			'"ACTION".ACTION_ID = ACTION_NOTIFICATION.ACTION_ID',
			array('ACTION_ID', 'AVAILABLE_ACTION_ID', 'BUTTON_ID', 'EXECUTE_ALWAYS', 'SORT')
		)->joinLeft(
			'ACTION_T',
			$this->dbAdapter->quoteInto('ACTION_T.ACTION_ID = "ACTION".ACTION_ID AND ACTION_T.LANGUAGE = ?', $language),
			array('NAME', 'DESCRIPTION', 'SUCCESS_MESSAGE', 'ERROR_MESSAGE')
		);
		$row = $this->table->fetchAll($select)->current();
		$res = Notification_Action_Notification_Data::fromDBArray($row->toArray(), true);
		return $res;
	}

	/**
	 * Retrieves the form.
	 *
	 * @return Notification_Action_ActionConfig_Form
	 */
	public function getForm() {

		return new Notification_Action_ActionConfig_Form();

	}

	/**
	 * Injects variables to the view.
	 *
	 * Not used in this module
	 *
	 * @param int $actionId
	 * @param Zend_View $view
	 * @return void
	 */
	public function injectVariables($actionId, $view) {

	}

	/**
	 * Retrieves the url of the file with the additional tabs to display.
	 *
	 * Not used in this module
	 *
	 * @return string
	 */
	public function getTabs() {
		return NULL;

	}

	/**
	 *  Retrieves the url of the file with the context menu fo the additioanl tabs.
	 *
	 * Not used in this module
	 *
	 * @return string
	 */
	public function getContextMenu() {
		return NULL;
	}

	/**
	 * Retrieves the instance of the concrete handler action
	 *
	 * @param int $actionId
	 * @return Notification_Action_Notification_Action
	 */
	public function getHandlerAction($actionId) {
		return new Notification_Action_Notification_Action($this->getAction($actionId));
	}

	/**
	 * Deletes the action.
	 *
	 * @param int $actionId
	 * @return void
	 */
	public function delete($actionId) {
		$this->table->delete($this->dbAdapter->quoteInto('ACTION_ID = ?', $actionId));
	}

}

