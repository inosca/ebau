<?php


class Workflow_Model_Data_WorkflowEntry {

	public $workflowEntryID;

	public $instanceID;

	public $workflowDate;

	public $workflowItemID;

	public $group;

	public function __construct(
		$workflowEntryID,
		$instanceID,
		$workflowDate,
		$workflowItemID,
		$group
	) {
		$this->workflowEntryID = $workflowEntryID;
		$this->instanceID      = $instanceID;
		$this->workflowDate    = $workflowDate;
		$this->workflowItemID  = $workflowItemID;
		$this->group           = $group;
	}

}
