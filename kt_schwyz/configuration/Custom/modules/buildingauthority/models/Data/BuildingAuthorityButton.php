<?php

class Buildingauthority_Model_Data_BuildingAuthorityButton {

	public $baButtonId;

	public $label;

	private $isClicked;

	private $isDisabled;

	public function __construct(
		$baButtonId,
		$label
	) {
		$this->baButtonId = $baButtonId;
		$this->label      = $label;
	}

	public function isClicked($instanceId) {
		if ($this->isClicked === null) {
			$baButtonStateMapper = new Buildingauthority_Model_Mapper_BuildingAuthorityButtonState();
			$this->isClicked = $baButtonStateMapper->isClicked($this->baButtonId, $instanceId);
		}

		return $this->isClicked;
	}

	public function isDisabled($instanceId) {
		if ($this->isDisabled === null) {
			$baButtonStateMapper = new Buildingauthority_Model_Mapper_BuildingAuthorityButtonState();
			$this->isDisabled = $baButtonStateMapper->isDisabled($this->baButtonId, $instanceId);
		}

		return $this->isDisabled;
	}

	public function hasPropDisabled($instanceId) {
		return ($this->isClicked($instanceId) || $this->isDisabled($instanceId));
	}
}
