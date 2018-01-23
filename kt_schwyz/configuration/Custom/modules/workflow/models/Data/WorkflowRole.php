<?php

class Workflow_Model_Data_WorkflowRole {

	public $workflowItemID;

	public $roleID;


	public function __construct($workflowItemID, $roleID) {

		$this->workflowItemID = $workflowItemID;
		$this->roleID         = $roleID;
	}
}
