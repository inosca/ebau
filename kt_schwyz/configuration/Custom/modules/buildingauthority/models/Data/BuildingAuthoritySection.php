<?php

class Buildingauthority_Model_Data_BuildingAuthoritySection {

	public $baSectionId;

	public $name;

	protected $isDisabled;

	public function __construct(
		$baSectionId,
		$name
	) {
		$this->baSectionId = $baSectionId;
		$this->name        = $name;
	}

	public function isDisabled($instanceId) {
		if ($this->isDisabled !== null) {
			return $this->isDisabled;
		}

		$model = new Buildingauthority_Model_DbTable_BuildingAuthoritySectionDis();
		$select = $model->select()
			->where('BA_SECTION_ID = ?', $this->baSectionId)
			->where('INSTANCE_ID = ?', $instanceId);
		$result = $model->fetchRow($select);

		$this->isDisabled = (bool)$result;
		return $this->isDisabled;
	}
}
