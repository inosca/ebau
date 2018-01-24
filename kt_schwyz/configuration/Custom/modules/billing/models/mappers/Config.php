<?php

class Billing_Model_Mapper_Config {

	protected $dbTable;

	public function __construct() {
		$this->dbTable = new Billing_Model_DbTable_Config();
	}

	public function insert(Billing_Model_Data_Config $config) {
		$data = array(
			'NAME'  => $config->name,
			'VALUE' => $config->value
		);

		return $this->dbTable->insert($data);
	}

	public function update(Billing_Model_Data_Config $config) {
		$data = array(
			'NAME'    => $config->name,
			'VALUE'   => $config->value
		);

		$this->dbTable->update($data, array('BILLING_CONFIG_ID = ?' => $config->billingConfigID));
	}

	public function getConfigs() {
		$select = $this->dbTable->select();
		$rows = $this->dbTable->fetchAll($select);

		$result = array();
		foreach ($rows as $row) {
			$result[] = new Billing_Model_Data_Config(
				$row['BILLING_CONFIG_ID'],
				$row['NAME'],
				$row['VALUE']
			);
		}

		return $result;
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function getConfig($id) {
		$row = $this->dbTable->find($id);

		if ($row) {
			return new Billing_Model_Data_Config(
				$id,
				$row[0]['NAME'],
				$row[0]['VALUE']
			);
		}
	}

	/**
	 * Returns a config value by its name. This is static to
	 * allow convenient calling.
	 *
	 * @param {String} $name
	 * @return {String}
	 */
	public static function getConfigByName($name) {
		$dbTable = new Billing_Model_DbTable_Config();
		$select = $dbTable->select();
		$select->where('"NAME" = ?', $name);
		$row = $dbTable->fetchRow($select);

		if ($row) {
			return $row['VALUE'];
		}
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->dbTable->delete(array('BILLING_CONFIG_ID = ?' => $id));
	}

}
