<?php

class Buildingauthority_Model_Mapper_BuildingAuthorityButtonState extends Custom_CamacMapper {

	protected $dbTable = "Buildingauthority_Model_DbTable_BuildingAuthorityButtonState";
	protected $pk_prop = "baButtonStateId";
	protected $pk_col  = "BA_BUTTON_STATE_ID";

	public function rowToModel($row) {
		return new Buildingauthority_Model_Data_BuildingAuthorityButtonState(
			$row['BA_BUTTON_STATE_ID'],
			$row['BUILDING_AUTHORITY_BUTTON_ID'],
			$row['INSTANCE_ID'],
			$row['IS_CLICKED'],
			$row['IS_DISABLED']
		);
	}

	public function modelToRow($model) {
		return array(
			'BUILDING_AUTHORITY_BUTTON_ID' => $model->baButtonId,
			'INSTANCE_ID'                  => $model->instanceId,
			'IS_CLICKED'                   => $model->isClicked,
			'IS_DISABLED'                  => $model->isDisabled
		);
	}

	public function isClicked($buttonId, $instanceId) {
		$select = $this->model->select()
			->where('BUILDING_AUTHORITY_BUTTON_ID = ?', $buttonId)
			->where('INSTANCE_ID = ?', $instanceId)
			->where('IS_CLICKED = ?', 1);
		return (bool)$this->model->fetchRow($select);
	}

	public function isDisabled($buttonId, $instanceId) {
		$select = $this->model->select()
			->where('BUILDING_AUTHORITY_BUTTON_ID = ?', $buttonId)
			->where('INSTANCE_ID = ?', $instanceId)
			->where('IS_DISABLED = ?', 1);
		return (bool)$this->model->fetchRow($select);
	}

	public function setIsClicked($buttonId, $instanceId) {
		$data  = array('IS_CLICKED' => 1);
		$where = array(
			'BUILDING_AUTHORITY_BUTTON_ID = ?' => $buttonId,
			'INSTANCE_ID = ?' => $instanceId
		);

		$updatedRows = $this->model->update($data, $where);

		if (!$updatedRows) {
			$data['BUILDING_AUTHORITY_BUTTON_ID'] = $buttonId;
			$data['INSTANCE_ID'] = $instanceId;

			$this->model->insert($data);
		}
	}

	public function setIsDisabled($buttonId, $instanceId) {
		$data  = array('IS_DISABLED' => 1);
		$where = array(
			'BUILDING_AUTHORITY_BUTTON_ID = ?' => $buttonId,
			'INSTANCE_ID = ?' => $instanceId
		);

		$updatedRows = $this->model->update($data, $where);

		if (!$updatedRows) {
			$data['BUILDING_AUTHORITY_BUTTON_ID'] = $buttonId;
			$data['INSTANCE_ID'] = $instanceId;

			$this->model->insert($data);
		}
	}

	public function enableAll($instanceId) {
		$this->model->update(
			array('IS_DISABLED' => 0),
			array('INSTANCE_ID = ?' => $instanceId)
		);
	}
}
