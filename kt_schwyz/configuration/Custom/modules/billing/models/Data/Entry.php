<?php


class Billing_Model_Data_Entry {

	public $billingEntryID;

	public $amount;

	public $billingAccountID;

	public $userID;

	public $instanceID;

	public $serviceID;

	public $created;

	public $type;

	public $amountType;

	public $reason;

	public $invoiced;

	/**
	 * This is like a "computed property": not saved in
	 * the database, but calculated from "amount" and the
	 * hourly rate.
	 */
	public $actualAmount;

	/**
	 * @SuppressWarnings(short)
	 */
	public function __construct(
		$ID,
		$amount,
		$billingAccount,
		$user,
		$instanceID,
		$serviceID,
		$created,
		$type,
		$amountType,
		$reason,
		$invoiced,
		$actualAmount = 0
	) {
		$this->billingEntryID   = $ID;
		$this->amount           = $amount;
		$this->billingAccountID = $billingAccount;
		$this->userID           = $user;
		$this->instanceID       = $instanceID;
		$this->serviceID        = $serviceID;
		$this->created          = $created;
		$this->type             = $type;
		$this->amountType       = $amountType;
		$this->reason           = $reason;
		$this->invoiced         = $invoiced;
		$this->actualAmount     = $actualAmount;
	}

	public function getAccount() {
		$accountMapper = new Billing_Model_Mapper_Account();
		return $accountMapper->getAccount($this->billingAccountID);
	}

	public function getService() {
		$serviceMapper = new Application_Model_Mapper_Account_Service();
		return $serviceMapper->getService($this->serviceID);
	}

	public function getUserName() {
		$userMapper = new Camac_Model_DbTable_Account_User();

		$user = $userMapper->find($this->userID);

		return $user[0]->USERNAME;
	}
}
