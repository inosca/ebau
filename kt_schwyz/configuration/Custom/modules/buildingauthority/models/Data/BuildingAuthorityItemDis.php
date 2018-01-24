<?php

class Buildingauthority_Model_Data_BuildingAuthorityItemDis {

	public $baItemDisId;

	public $workflowItemId;

	public $instanceId;

	public $group;

	public function __construct(
		$baItemDisId,
		$workflowItemId,
		$instanceId,
		$group
	) {
		$this->baItemDisId    = $baItemDisId;
		$this->workflowItemId = $workflowItemId;
		$this->instanceId     = $instanceId;
		$this->group          = $group;
	}
}
