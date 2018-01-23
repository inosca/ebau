<?php

class Buildingauthority_Model_Data_BuildingAuthorityButtonState {

	public $baButtonStateId;

	public $instanceId;

	public $isClicked;

	public $isDisabled;

	public function __construct(
		$baButtonStateId,
		$instanceId,
		$isClicked,
		$isDisabled
	) {
		$this->baButtonStateId = $baButtonStateId;
		$this->instanceId      = $instanceId;
		$this->isClicked       = $isClicked;
		$this->isDisabled      = $isDisabled;
	}
}
