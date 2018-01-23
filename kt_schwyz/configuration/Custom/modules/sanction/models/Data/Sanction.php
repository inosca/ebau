<?php

class Sanction_Model_Data_Sanction {

	public $sanctionID;

	public $instanceID;

	public $serviceID;

	public $userID;

	public $text;

	public $startDate;

	public $deadlineDate;

	public $endDate;

	public $notice;

	public $isFinished;

	public $finishedByUserID;

	public $finishedByUsername;

	public $username;

	public function __construct(
		$sanctionID,
		$instanceID,
		$serviceID,
		$userID,
		$username,
		$text,
		$startDate,
		$deadlineDate = null,
		$endDate = null,
		$notice = null,
		$isFinished = 0,
		$finishedByUserID = null,
		$finishedByUsername = null
	) {
		$this->sanctionID         = $sanctionID;
		$this->instanceID         = $instanceID;
		$this->serviceID          = $serviceID;
		$this->userID             = $userID;
		$this->username           = $username;
		$this->text               = $text;
		$this->startDate          = $startDate;
		$this->deadlineDate       = $deadlineDate;
		$this->endDate            = $endDate;
		$this->notice             = $notice;
		$this->isFinished         = $isFinished;
		$this->finishedByUserID   = $finishedByUserID;
		$this->finishedByUsername = $finishedByUsername;
	}

	public static function getEmpty() {
		return new self(null, null, null, null, null, null, null);
	}

	public function getService() {
		$serviceMapper = new Application_Model_Mapper_Account_Service();

		if ($this->serviceID) {
			return $serviceMapper->getService($this->serviceID)->getName();
		}
	}
}
