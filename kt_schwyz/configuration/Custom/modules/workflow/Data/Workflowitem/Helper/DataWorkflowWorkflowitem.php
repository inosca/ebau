<?php

class Workflow_Data_WorkflowItem_Helper_DataWorkflowWorkflowitem extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {


	protected $mapper;

	public function __construct() {
		$this->mapper = new Workflow_Model_Mapper_WorkflowItem();
		$this->roleMapper = new Workflow_Model_Mapper_WorkflowRole();
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function add($form, $id, $mode) {
		$workflow = new Workflow_Model_Data_WorkflowItem(
			null,
			$form->getValue('name'),
			$form->getValue('automatical'),
			$form->getValue('differentColor'),
			$this->mapper->countWorkflows() + 1,
			$form->getValue('workflowSectionID'),
			true // set is_workflow to true for items created in admin
		);
		$workflowItemID = $this->mapper->save($workflow);

		$this->saveRoles($workflowItemID, $form);
	}

	protected function saveRoles($workflowItemID, $form) {
		$this->roleMapper->deleteFromWorkflowItem($workflowItemID);

		foreach ($form->getValue('roles') as $role) {
			$workflowRole = new Workflow_Model_Data_WorkflowRole(
				$workflowItemID,
				$role
			);

			$this->roleMapper->save($workflowRole);
		}
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function update($id, $form, $previousLanguage = NULL) {
		$workflow = $this->mapper->getEntry($id);
		$workflow->name = $form->getValue('name');
		$workflow->automatical = $form->getValue('automatical');
		$workflow->differentColor = $form->getValue('differentColor');
		$workflow->workflowSectionID = $form->getValue('workflowSectionID');

		$this->mapper->update($workflow);

		$this->saveRoles($id, $form);
	}


	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->roleMapper->deleteFromWorkflowItem($id);
		$this->mapper->delete($id);
	}

	/**
	 *  @SuppressWarnings(short)
	 */
	public function move($id, $targetId, $mode) {
		$currentPosition = $this->mapper->getEntry($id)->position;
		$targetPosition  = $this->mapper->getEntry($targetId)->position;
		$workflows = $this->mapper->getAll();
		$newPosition = $mode == 'after' ? $targetPosition + 1 : $targetPosition;

		$elem = array_splice($workflows, $currentPosition - 1, 1);
		$result = array_merge(array_slice($workflows, 0, $newPosition - 1), $elem, array_slice($workflows, $newPosition -1));

		foreach ($result as $key => $workflow) {
			$this->mapper->updatePosition($workflow->workflowItemID, $key + 1);
		}
	}

	public function getRows() {
		return $this->mapper->getAll();
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function getData($id, $language = NULL) {
		return $this->mapper->getEntry($id);
	}

	public function getForm() {
		return new Workflow_Data_Workflowitem_Form();
	}
}
