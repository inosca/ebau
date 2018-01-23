<?php

class Billing_Model_Mapper_AccountState {

	protected $dbTable;

	public function __construct() {
		$this->dbTable = new Billing_Model_DbTable_AccountState();
	}

	public function insert(Billing_Model_Data_AccountState $accountState) {
		$data = array(
			'BILLING_ACCOUNT_STATE_ID' => $accountState->id,
			'BILLING_ACCOUNT_ID'       => $accountState->billingAccountId,
			'INSTANCE_STATE_ID'        => $accountState->instanceStateId
		);

		return $this->dbTable->insert($data);
	}

	public function update(Billing_Model_Data_Account $account) {
		$data = array(
			'BILLING_ACCOUNT_STATE_ID' => $accountState->id,
			'BILLING_ACCOUNT_ID'       => $accountState->billingAccountId,
			'INSTANCE_STATE_ID'        => $accountState->instanceStateId
		);

		$this->dbTable->update($data, array('BILLING_ACCOUNT_ID = ?' => $account->billingAccountId));
	}

	public function getStates($billingAccountId) {
		$select = $this->dbTable->select();

		$select->where('"BILLING_ACCOUNT_ID" = ?', $billingAccountId);

		$rows = $this->dbTable->fetchAll($select);

		$result = array();
		foreach ($rows as $row) {
			$result[] = new Billing_Model_Data_AccountState(
				$row['BILLING_ACCOUNT_STATE_ID'],
				$row['BILLING_ACCOUNT_ID'],
				$row['INSTANCE_STATE_ID']
			);
		}

		return $result;
	}

	public function deleteAll($accountId) {
		$this->dbTable->delete(array('BILLING_ACCOUNT_ID = ?' => $accountId));
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->dbTable->delete(array('BILLING_ACCOUNT_STATE_ID = ?' => $id));
	}
}
