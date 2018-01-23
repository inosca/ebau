<?php

class Billing_Model_Mapper_Account {

	protected $dbTable;

	private $serviceGroupTable;

	public function __construct() {
		$this->dbTable = new Billing_Model_DbTable_Account();
		$this->serviceGroupTable = new Camac_Model_DbTable_Account_ServiceGroup();
	}

	public function insert(Billing_Model_Data_Account $account) {
		$data = array(
			'DEPARTMENT'       => $account->department,
			'NAME'             => $account->name,
			'ACCOUNT_NUMBER'   => $account->accountNumber,
			'SERVICE_GROUP_ID' => $account->serviceGroupID,
			'PREDEFINED'       => intval($account->predefined)
		);

		return $this->dbTable->insert($data);
	}

	public function update(Billing_Model_Data_Account $account) {
		$data = array(
			'DEPARTMENT'       => $account->department,
			'NAME'             => $account->name,
			'ACCOUNT_NUMBER'   => $account->accountNumber,
			'SERVICE_GROUP_ID' => $account->serviceGroupID,
			'PREDEFINED'       => intval($account->predefined)
		);

		$this->dbTable->update($data, array('BILLING_ACCOUNT_ID = ?' => $account->billingAccountID));
	}

	public function getAccounts($predefinedOnly = true, $serviceGroupID = null, $instanceStateId = null) {
		$serviceGroupID = (int) $serviceGroupID;
		$select = $this->dbTable->select()->from('BILLING_ACCOUNT');

		if ($predefinedOnly) {
			$select = $select->where('"PREDEFINED" = 1');
		}

		// filter for serviceGroup, except if it is a KOORD.
		if ($serviceGroupID && $serviceGroupID !== 1) {
			$select->where('"SERVICE_GROUP_ID" = ?', $serviceGroupID);
		}
		$select->order(array('DEPARTMENT ASC'));

		if ($instanceStateId) {
			$select->join('BILLING_ACCOUNT_STATE', '"BILLING_ACCOUNT_STATE"."BILLING_ACCOUNT_ID" = "BILLING_ACCOUNT"."BILLING_ACCOUNT_ID"')
				->where('"BILLING_ACCOUNT_STATE"."INSTANCE_STATE_ID" = ?', $instanceStateId)
				->setIntegrityCheck(false);
		}

		$rows = $this->dbTable->fetchAll($select);

		$result = array();
		foreach ($rows as $row) {
			$result[] = new Billing_Model_Data_Account(
				$row['BILLING_ACCOUNT_ID'],
				$row['DEPARTMENT'],
				$row['NAME'],
				$row['ACCOUNT_NUMBER'],
				$row['SERVICE_GROUP_ID'],
				$row['PREDEFINED']
			);
		}

		return $result;
	}

	/**
	 * Returns nested array of service groups with their respective billing accounts.
	 *
	 * Example:
	 * array("Koordinationsstellen => array(account1, account2, ... ), ... )
	 */
	public function getGroupedAccounts($predefinedOnly, $serviceGroupID = null, $instanceStateId = null) {
		$accounts = $this->getAccounts($predefinedOnly, $serviceGroupID, $instanceStateId);

		$serviceGroupIDs = array_unique(array_map(function($account) {
			return $account->serviceGroupID;
		}, $accounts));

		$serviceGroupIDs = array_filter($serviceGroupIDs, function($serviceGroupID) {
			return $serviceGroupID != null;
		});

		$result = array();
		foreach($serviceGroupIDs as $serviceGroupID) {
			$name = $this->serviceGroupTable->find($serviceGroupID)->current()->NAME;
			$result[$name] = array_filter($accounts, function($account) use ($serviceGroupID) {
				return $account->serviceGroupID === $serviceGroupID;
			});
		}

		return $result;
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function getAccount($id) {
		$row = $this->dbTable->find($id);

		if ($row) {
			return new Billing_Model_Data_Account(
				$row[0]['BILLING_ACCOUNT_ID'],
				$row[0]['DEPARTMENT'],
				$row[0]['NAME'],
				$row[0]['ACCOUNT_NUMBER'],
				$row[0]['SERVICE_GROUP_ID'],
				$row[0]['PREDEFINED']
			);
		}

	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->dbTable->delete(array('BILLING_ACCOUNT_ID = ?' => $id));
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function deleteIfNotPredefined($id) {
		$account = $this->getAccount($id);

		if (!$account->predefined) {
			$this->dbTable->delete(array('BILLING_ACCOUNT_ID = ? ' => $id));
		}
	}
}
