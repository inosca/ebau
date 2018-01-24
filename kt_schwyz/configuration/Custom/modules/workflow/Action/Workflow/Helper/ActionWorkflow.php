<?php

class Workflow_Action_Workflow_Helper_ActionWorkflow extends Zend_Controller_Action_Helper_Abstract implements Camac_Action_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Workflow_Action_Workflow_Mapper();
	}


	public function add($actionId, $form) {
		$workflowAction = new Workflow_Action_Workflow_Data(
			$actionId,
			null, null, null, null, null, null, null, null,
			$form->getValue('workflow_id'),
			$form->getValue('multi_value')
		);

		$this->mapper->save($workflowAction);
   	}

	public function update($actionId, $form) {
		$workflowAction = new Workflow_Action_Workflow_Data(
			$actionId,
			null, null, null, null, null, null, null, null,
			$form->getValue('workflow_id'),
			$form->getValue('multi_value')
		);

		$this->mapper->update($workflowAction);
	}


	public function getAction($actionId, $language = null) {
		return $this->mapper->getWorkflowAction($actionId);
	}

	public function getForm() {
		return new Workflow_Action_Workflow_Form();
	}

 	/**
	 * Injects variables to the view.
	 * These variables are used to display data in the additional tabs added by te resource.
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
	 * @return string
	 */
	public function getTabs() {

		return NULL;

	}

	/**
	 *  Retrieves the url of the file with the context menu fo the additioanl tabs.
	 *
	 * @return string
	 */
	public function getContextMenu() {

		return NULL;

	}

	/**
	 * Retrieves the instance of the concrete handler action.
	 *
	 * @param int $actionId
	 * @return Wsgeocode_Action_Wsgeocode_Action
	 */
	public function getHandlerAction($actionId) {

		$resourceAction = $this->getAction($actionId, true);
		return new Workflow_Action_Workflow_Action($resourceAction);

	}

	/**
	 * Deletes the action.
	 *
	 * @param int $actionId
	 * @return void
	 */
	public function delete($actionId) {
		$this->mapper->delete($actionId);
	}


}
