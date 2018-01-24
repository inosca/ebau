<?php

class Buildingauthority_Model_Data_BuildingAuthorityComment {

	public $baCommentId;

	public $baSectionId;

	public $instanceId;

	public $text;

	public $group;

	public function __construct(
		$baCommentId,
		$baSectionId,
		$instanceId,
		$text,
		$group
	) {
		$this->baCommentId = $baCommentId;
		$this->baSectionId = $baSectionId;
		$this->instanceId  = $instanceId;
		$this->text        = $text;
		$this->group       = $group;
	}
}
