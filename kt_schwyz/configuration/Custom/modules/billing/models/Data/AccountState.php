<?php

class Billing_Model_Data_AccountState {

	public $id;

	public $billingAccountId;

	public $instanceStateId;

	public function __construct($id, $billingAccountId, $instanceStateId) {
		$this->id = $id;
		$this->billingAccountId = $billingAccountId;
		$this->instanceStateId   = $instanceStateId;
	}
}
