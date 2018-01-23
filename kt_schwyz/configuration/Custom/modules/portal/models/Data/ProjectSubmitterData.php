<?php

class Portal_Model_Data_ProjectSubmitterData {

	public $instanceId;

	public $name;

	public $email;

	public $answer;

	public function __construct(
		$instanceId,
		$name,
		$email,
		$answer
	) {
		$this->instanceId = $instanceId;
		$this->name       = $name;
		$this->email      = $email;
		$this->answer     = $answer;
	}
}
