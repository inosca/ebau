<?php
class Workflow_Model_Data_WorkflowSection {

	public $workflowSectionID;

	public $name;

	public $sort;

	public function __construct(
		$workflowSectionID,
		$name,
		$sort
	) {
		$this->workflowSectionID = $workflowSectionID;
		$this->name              = $name;
		$this->sort              = $sort;
	}

	public function getItems() {
		$mapper = new Workflow_Model_Mapper_WorkflowItem;
		return $mapper->getBySection($this->workflowSectionID);
	}
}
