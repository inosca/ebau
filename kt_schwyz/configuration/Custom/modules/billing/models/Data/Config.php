<?php

class Billing_Model_Data_Config {


	public $billingConfigID;

	public $name;

	public $value;

	/**
	 * @SuppressWarnings(short)
	 */
	public function __construct($ID, $name, $value) {
		$this->billingConfigID = $ID;
		$this->name  = $name;
		$this->value = $value;
	}
}
