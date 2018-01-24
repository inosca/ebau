<?php

class Workflow_Model_Mapper_WorkflowRole {

	protected $model;

	public function __construct() {
		$this->model = new Workflow_Model_DbTable_WorkflowRole();
	}


	public function save(Workflow_Model_Data_WorkflowRole $role) {
	
		$data = array(
			'WORKFLOW_ITEM_ID' => $role->workflowItemID,
			'ROLE_ID'          => $role->roleID
		);

		$this->model->insert($data);
	}


	public function deleteFromWorkflowItem($workflowItemID) {
		$this->model->delete(array('WORKFLOW_ITEM_ID = ?' => $workflowItemID));
	}

	public function getWorkflowItemRoles($workflowItemID) {
		$select = $this->model->select()->where('WORKFLOW_ITEM_ID = ?', $workflowItemID);

		$rows =  $this->model->fetchAll($select);
		$results = array();

		foreach ($rows as $row) {
			$results[] = new Workflow_Model_Data_WorkflowRole(
				$row->WORKFLOW_ITEM_ID,
				$row->ROLE_ID
			);
		}

		return $results;
	}
}
