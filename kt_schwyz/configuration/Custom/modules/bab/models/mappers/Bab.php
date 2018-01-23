<?php

class Bab_Model_Mapper_Bab {

	function __construct() {
		$this->table = new Bab_Model_DbTable_BabUsage();
	}

	public function get($instanceId) {
		$select = $this->table->select()->where('INSTANCE_ID = ?', $instanceId);
		return $this->table->fetchAll($select);
	}

	/**
	 * Saves a set of entries by deleting all old ones and
	 * recreating them.
	 */
	public function save($instanceId, $entries) {
		if (!is_numeric($instanceId)) {
			return false;
		}
		if (!Custom_UriUtils::validateArray($entries, function($entry) {
			return is_numeric($entry['USAGE_TYPE']) &&
				is_numeric($entry['USAGE']);
		})) {
			return false;
		}

		$where = $this->table->getAdapter()->quoteInto('INSTANCE_ID = ?', $instanceId);
		$this->table->delete($where);

		foreach ($entries as $entry) {
			$entry['INSTANCE_ID'] = $instanceId;
			$this->table->insert($entry);
		}
		return true;
	}

}
