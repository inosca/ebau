<?php

class Buildingauthority_Model_Data_BuildingAuthorityEmail {

	public $baEmailId;

	public $baButtonId;

	public $emailSubject;

	public $emailText;

	public $fromEmail;

	public $fromName;

	public $receiverQuery;

	public function __construct(
		$baEmailId,
		$baButtonId,
		$emailSubject,
		$emailText,
		$fromEmail,
		$fromName,
		$receiverQuery
	) {
		$this->baEmailId     = $baEmailId;
		$this->baButtonId    = $baButtonId;
		$this->emailSubject  = $emailSubject;
		$this->emailText     = $emailText;
		$this->fromEmail     = $fromEmail;
		$this->fromName      = $fromName;
		$this->receiverQuery = $receiverQuery;
	}

	public function getButton() {
		$mapper = new Buildingauthority_Model_Mapper_BuildingAuthorityButton();
		return $mapper->getButton($this->baButtonId);
	}
}
