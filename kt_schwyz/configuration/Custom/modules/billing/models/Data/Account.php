<?php

class Billing_Model_Data_Account {


	public $billingAccountID;

	public $department;

	public $name;

	public $accountNumber;

	public $serviceGroupID;

	public $predefined;

	/**
	 * @SuppressWarnings(short)
	 */
	public function __construct($ID, $department, $name, $account, $serviceGroupID, $predefined) {
		$this->billingAccountID = $ID;
		$this->department       = $department;
		$this->name             = $name;
		$this->accountNumber    = $account;
		$this->serviceGroupID   = $serviceGroupID;
		$this->predefined       = (bool)$predefined;
	}
}
