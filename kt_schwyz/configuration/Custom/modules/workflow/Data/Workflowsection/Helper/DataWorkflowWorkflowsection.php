<?php

class Workflow_Data_Workflowsection_Helper_DataWorkflowWorkflowsection extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Workflow_Model_Mapper_WorkflowSection();
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function add($form, $id, $mode) {
		$model = new Workflow_Model_Data_WorkflowSection(
			null,
			$form->getValue('name'),
			$form->getValue('sort')
		);
		return $this->mapper->save($model);
	}

	/**
	 *  @SuppressWarnings(short)
	 */
	public function update($id, $form, $previousLanguage = NULL) {
		$model = new Workflow_Model_Data_WorkflowSection(
			$id,
			$form->getValue('name'),
			$form->getValue('sort')
		);
		$this->mapper->update($model);
	}

	/**
	 *  @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->mapper->delete($id);
	}

	/**
	 *  @SuppressWarnings(short)
	 */
	public function move($id, $targetId, $mode) {
		$currentPosition = $this->mapper->getEntry($id)->sort;
		$targetPosition  = $this->mapper->getEntry($targetId)->sort;
		$models = $this->mapper->getAll();
		$newPosition = $mode == 'after' ? $targetPosition + 1 : $targetPosition;

		$elem = array_splice($models, $currentPosition - 1, 1);
		$result = array_merge(
			array_slice($models, 0, $newPosition - 1),
			$elem,
			array_slice($models, $newPosition -1)
		);

		foreach ($result as $key => $model) {
			$this->mapper->updateSort($model->workflowSectionID, $key + 1);
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
		return new Workflow_Data_Workflowsection_Form();
	}
}
