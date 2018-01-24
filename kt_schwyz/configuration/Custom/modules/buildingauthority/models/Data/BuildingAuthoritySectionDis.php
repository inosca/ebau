<?php

class Buildingauthority_Model_Data_BuildingAuthoritySectionDis {

	public $baSectionDisId;

	public $baSectionId;

	public $instanceId;

	public function __construct(
		$baSectionDisId,
		$baSectionId,
		$instanceId
	) {
		$this->baSectionDisId = $baSectionDisId;
		$this->baSectionId    = $baSectionId;
		$this->instanceId     = $instanceId;
	}
}
