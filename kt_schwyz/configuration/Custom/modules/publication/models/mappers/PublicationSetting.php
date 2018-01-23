<?php

class Publication_Model_Mapper_PublicationSetting {

	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Publication_Model_DbTable_PublicationSetting();
	}

	public function save(Publication_Model_Data_PublicationSetting $publicationSetting) {
		$data = array(
			'KEY'   => $publicationSetting->key,
			'VALUE' => $publicationSetting->value
		);

		return $this->model->insert($data);
	}

	public function update(Publication_Model_Data_PublicationSetting $publicationSetting) {
		$data = array(
			'KEY' => $publicationSetting->key,
			'VALUE' => $publicationSetting->value
		);

		$this->model->update(
			$data,
			array('PUBLICATION_SETTING_ID = ?' => $publicationSetting->publicationSettingID)
		);
	}

	public function getEntry($id) {
		$result = NULL;
		$row = $this->model->find($id)->current();
		if ($row) {
			$result = new Publication_Model_Data_PublicationSetting(
				$row->PUBLICATION_SETTING_ID,
				$row->KEY,
				$row->VALUE
			);
		}

		return $result;
	}

	public function getEntryByKey($key) {
		$result = NULL;
		$select = $this->model->select()->where('KEY = ?', $key);
		$row = $this->model->fetchRow($select);
		if ($row) {
			$result = new Publication_Model_Data_PublicationSetting(
				$row->PUBLICATION_SETTING_ID,
				$row->KEY,
				$row->VALUE
			);
		}

		return $result;
	}

	public function getEntries() {
		$select = $this->model->select()->order(array('KEY ASC'));

		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Publication_Model_Data_PublicationSetting(
				$row->PUBLICATION_SETTING_ID,
				$row->KEY,
				$row->VALUE
			);
		}

		return $results;
	}

	public function delete($publicationSettingID) {
		$this->model->delete(array('PUBLICATION_SETTING_ID = ?' => $publicationSettingID));
	}
}
