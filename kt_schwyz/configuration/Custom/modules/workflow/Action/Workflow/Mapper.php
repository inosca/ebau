<?php

class Workflow_Action_Workflow_Mapper {

	protected $model;


	public function __construct() {
		$this->model = new Workflow_Action_Workflow_DbTable();
	}

	public function save(Workflow_Action_Workflow_Data $workflowAction) {
		$data = array(
			'WORKFLOW_ITEM_ID' => $workflowAction->getWorkflowItemID(),
			'MULTI_VALUE'      => $workflowAction->getMultiValue(),
			'ACTION_ID'   => $workflowAction->getActionId()
		);

		$this->model->insert($data);
	}

	public function update(Workflow_Action_Workflow_Data $workflowAction) {
		$data = array(
			'WORKFLOW_ITEM_ID' => $workflowAction->getWorkflowItemID(),
			'MULTI_VALUE'      => $workflowAction->getMultiValue(),
		);

		$this->model->update($data, array('ACTION_ID = ?' => $workflowAction->getActionId()));
	}

	public function delete($actionId) {
		$this->model->delete(array('ACTION_ID = ?' => $actionId));
	}

	public function getWorkflowAction($actionId) {

		$sel = $this->model->select()
			->from('WORKFLOW_ACTION', "*")
			->joinLeft('ACTION', 'ACTION.ACTION_ID = WORKFLOW_ACTION.ACTION_ID')
			->where('WORKFLOW_ACTION.ACTION_ID = ?', $actionId)
			->setIntegrityCheck(false);
		$row = $this->model->fetchAll($sel)->current();

		$result = new Workflow_Action_Workflow_Data(
			$row->ACTION_ID,
			$row->AVAILABLE_ACTION_ID,
			$row->BUTTON_ID,
			$row->NAME,
			$row->DESCRIPTION,
			$row->SUCCESS_MESSAGE,
			$row->ERROR_MESSAGE,
			$row->EXECUTE_ALWAYS,
			$row->SORT,
			$row->WORKFLOW_ITEM_ID,
			$row->MULTI_VALUE
		);

		return $result;
	}

} 
