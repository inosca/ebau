<?php

class Buildingauthority_Model_Mapper_BuildingAuthoritySection {

	protected $model;

	public function __construct() {
		$this->model = new Buildingauthority_Model_DbTable_BuildingAuthoritySection();
	}

	public function save(Buildingauthority_Model_Data_BuildingAuthoritySection $baSection) {
		$data = array(
			'NAME' => $baSection->name
		);

		return $this->model->insert($data);
	}

	public function update(Buildingauthority_Model_Data_BuildingauthoritySection $baSection) {
		$data = array('NAME' => $baSection->name);
		$this->model->update($data, array('BUILDING_AUTHORITY_SECTION_ID = ?' => $baSection->baSectionId));
	}

	public function getSection($baSectionId) {
		$result = null;
		$row    = $this->model->find($baSectionId)->current();

		if ($row) {
			$result = new Buildingauthority_Model_Data_BuildingAuthoritySection(
				$baSectionId,
				$row->NAME
			);
		}

		return $result;
	}

	public function getSections($order = null) {
		if (!$order) {
			$order = array('NAME ASC');
		}

		$select = $this->model->select()->order($order);
		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Buildingauthority_Model_Data_BuildingAuthoritySection(
				$row->BUILDING_AUTHORITY_SECTION_ID,
				$row->NAME
			);
		}

		return $results;
	}

	public function enableAll($instanceId) {
		$model = new Buildingauthority_Model_DbTable_BuildingAuthoritySectionDis();
		$model->delete(array(
			'INSTANCE_ID = ?' => $instanceId
		));
	}

	public function disable($baSectionId, $instanceId) {
		$model = new Buildingauthority_Model_DbTable_BuildingAuthoritySectionDis();
		$data = array(
			'BA_SECTION_ID' => $baSectionId,
			'INSTANCE_ID'   => $instanceId
		);
		$model->insert($data);
	}

	public function delete($baSectionId) {
		$this->model->delete(array(
			'BUILDING_AUTHORITY_SECTION_ID = ?' => $baSectionId
		));
	}
}
