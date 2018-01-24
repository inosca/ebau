<?php

class Billing_Model_Mapper_Entry {

	protected $dbTable;
	protected $hourlyRate;

	const AMOUNT_TYPE_PAUSCHAL = 0;
	const AMOUNT_TYPE_PER_HOUR = 1;
	const AMOUNT_TYPE_BASIC    = 2;

	const TYPE_BAUBEWILLIGUNG = 0;
	const TYPE_BAUBEGLEITUNG  = 1;

	public function __construct() {
		$this->dbTable = new Billing_Model_DbTable_Entry();
		$this->hourlyRate = Billing_Model_Mapper_Config::getConfigByName('hourly_rate');
	}

	public function insert(Billing_Model_Data_Entry $entry) {
		$data = array(
			'AMOUNT'             => $entry->amount,
			'BILLING_ACCOUNT_ID' => $entry->billingAccountID,
			'USER_ID'            => $entry->userID,
			'INSTANCE_ID'        => $entry->instanceID,
			'SERVICE_ID'         => $entry->serviceID,
			'CREATED'            => Camac_Date::getDbStringFromDateTime($entry->created),
			'TYPE'               => $entry->type,
			'AMOUNT_TYPE'        => $entry->amountType,
			'REASON'             => $entry->reason,
			'INVOICED'           => $entry->invoiced
		);

		$this->dbTable->insert($data);
	}

	public function update(Billing_Model_Data_Entry $entry) {
		$data = array(
			'AMOUNT'             => $entry->amount,
			'BILLING_ACCOUNT_ID' => $entry->billingAccountID,
			'USER_ID'            => $entry->userID,
			'INSTANCE_ID'        => $entry->instanceID,
			'SERVICE_ID'         => $entry->serviceID,
			'CREATED'            => Camac_Date::getDbStringFromDateTime($entry->created),
			'TYPE'               => $entry->type,
			'AMOUNT_TYPE'        => $entry->amountType,
			'REASON'             => $entry->reason,
			'INVOICED'           => $entry->invoiced
		);

		$this->dbTable->update($data, array('BILLING_ENTRY_ID = ?' => $entry->billingEntryID));
	}

	public function getEntries($instanceID = null, $serviceID = null, $uninvoicedOnly = false, $type = null) {
		$select = $this->dbTable->select();

		if ($serviceID) {
			$select = $select
				->where('"SERVICE_ID" = ? OR "INVOICED" = 1', $serviceID);
		}

		if ($instanceID) {
			$select = $select->where('"INSTANCE_ID" = ?', $instanceID);
		}

		if ($uninvoicedOnly) {
			$select = $select->where('"INVOICED" = 0');
		}

		if ($type !== null) {
			$select = $select->where('"TYPE" = ?', $type);
		}

		$rows = $this->dbTable->fetchAll($select);

		$results = array();
		foreach ($rows as $row) {
			switch ($row['AMOUNT_TYPE']) {
				case self::AMOUNT_TYPE_PER_HOUR:
					$actualAmount = $row['AMOUNT'] * $this->hourlyRate;
					break;
				case self::AMOUNT_TYPE_BASIC:
					$actualAmount = $row['AMOUNT'] * $this->hourlyRate / 2;
					break;
				case self::AMOUNT_TYPE_PAUSCHAL:
					$actualAmount = $row['AMOUNT'];
					break;
			}

			$results[] = new Billing_Model_Data_Entry(
				$row['BILLING_ENTRY_ID'],
				$row['AMOUNT'],
				$row['BILLING_ACCOUNT_ID'],
				$row['USER_ID'],
				$row['INSTANCE_ID'],
				$row['SERVICE_ID'],
				Camac_Date::getDateTimeFromDbString($row['CREATED']),
				$row['TYPE'],
				$row['AMOUNT_TYPE'],
				$row['REASON'],
				$row['INVOICED'],
				$actualAmount
			);
		}

		return $results;
	}

	public function getUninvoicedEntries($instanceID = null, $type = null) {
		return $this->getEntries($instanceID, null, true, $type);
	}

	public function getEntry($entryID) {
		$row = $this->dbTable->find($entryID)->current();

		return new Billing_Model_Data_Entry(
			$row['BILLING_ENTRY_ID'],
			$row['AMOUNT'],
			$row['BILLING_ACCOUNT_ID'],
			$row['USER_ID'],
			$row['INSTANCE_ID'],
			$row['SERVICE_ID'],
			Camac_Date::getDateTimeFromDbString($row['CREATED']),
			$row['TYPE'],
			$row['AMOUNT_TYPE'],
			$row['REASON'],
			$row['INVOICED']
		);
	}

	public function delete($deleteID) {
		$this->dbTable->delete(array('BILLING_ENTRY_ID = ? ' => $deleteID));
	}

}

