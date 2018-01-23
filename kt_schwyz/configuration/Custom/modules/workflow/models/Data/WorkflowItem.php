<?php
class Workflow_Model_Data_WorkflowItem {

	public $position;

	public $workflowItemID;

	public $name;

	public $automatical;

	public $differentColor;

	public $isWorkflow;

	public $isBuildingAuthority;

	public $workflowSectionID;

	public function __construct(
		$workflowItemID,
		$name,
		$automatical,
		$differentColor,
		$position,
		$workflowSectionID,
		$isWorkflow = false,
		$isBuildingAuthority = false
	) {
		$this->workflowItemID      = $workflowItemID;
		$this->name                = $name;
		$this->automatical         = $automatical;
		$this->differentColor      = $differentColor;
		$this->position            = $position;
		$this->workflowSectionID   = $workflowSectionID;
		$this->isWorkflow          = (bool)$isWorkflow;
		$this->isBuildingAuthority = (bool)$isBuildingAuthority;
	}

	public function getEntries($instanceID) {
		$workflowEntryMapper = new Workflow_Model_Mapper_WorkflowEntry;
		return $workflowEntryMapper->getEntries($instanceID, $this->workflowItemID);
	}

	public function getAllowedRoles() {
		$roleMapper = new Workflow_Model_Mapper_WorkflowRole;
		$allowedRoles = $roleMapper->getWorkflowItemRoles($this->workflowItemID);

		return $allowedRoles;
	}

	// DEPRECATED
	public function getName() {
		return $this->name;
	}

	// DEPRECATED
	public function setName($name) {
		$this->name = $name;
	}

	// DEPRECATED
	public function getID() {
		return $this->workflowItemID;
	}

	// DEPRECATED
	public function getAutomatical() {
		return (bool)$this->automatical;
	}

	// DEPRECATED
	public function setAutomatical($automatical) {
		$this->automatical = $automatical;
	}

	// DEPRECATED
	public function getDifferentColor() {
		return (bool)$this->differentColor;
	}

	// DEPRECATED
	public function setDifferentColor($diffcol) {
		$this->differentColor = $diffcol;
	}

	// DEPRECATED
	public function getPosition() {
		return $this->position;
	}

	// DEPRECATED
	public function isWorkflow() {
		return (bool)$this->isWorkflow;
	}

	// DEPRECATED
	public function isBuildingAuthority() {
		return (bool)$this->isBuildingAuthority;
	}
}
