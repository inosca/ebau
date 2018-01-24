<?php

class Buildingauthority_Model_Mapper_BuildingAuthorityItemDis {

	protected $model;

	public function __construct() {
		$this->model = new Buildingauthority_Model_DbTable_BuildingAuthorityItemDis();
	}

	public function isDisabled($workflowItemId, $instanceId, $group) {
		$select = $this->model->select()
			->where('WORKFLOW_ITEM_ID = ?', $workflowItemId)
			->where('INSTANCE_ID = ?', $instanceId)
			->where('"GROUP" = ?', $group);

		return (bool)$this->model->fetchRow($select);
	}

	public function enableAll($instanceId) {
		$this->model->delete(array(
			'INSTANCE_ID = ?' => $instanceId
		));
	}

	public function disable($workflowItemId, $instanceId, $group) {
		$data = array(
			'WORKFLOW_ITEM_ID' => $workflowItemId,
			'INSTANCE_ID'      => $instanceId,
			'GROUP'            => $group
		);
		$this->model->insert($data);
	}
}
