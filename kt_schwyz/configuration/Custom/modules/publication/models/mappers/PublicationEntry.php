<?php

class Publication_Model_Mapper_PublicationEntry {

	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Publication_Model_DbTable_PublicationEntry();
	}

	public function save(Publication_Model_Data_PublicationEntry $publicationEntry) {
		if ($publicationEntry->publicationEntryID !== null) {
			return $this->update($publicationEntry);
		}

		$data = array(
			'INSTANCE_ID'      => $publicationEntry->instanceID,
			'NOTE'             => $publicationEntry->note,
			'PUBLICATION_DATE' => Camac_Date::getDbStringFromDateTime($publicationEntry->publicationDate),
			'TEXT'             => $publicationEntry->text,
			'IS_PUBLISHED'     => $publicationEntry->isPublished
		);

		return $this->model->insert($data);
	}

	public function update(Publication_Model_Data_PublicationEntry $publicationEntry) {
		$data = array(
			'NOTE'             => $publicationEntry->note,
			'PUBLICATION_DATE' => Camac_Date::getDbStringFromDateTime($publicationEntry->publicationDate),
			'TEXT'             => $publicationEntry->text,
			'IS_PUBLISHED'     => $publicationEntry->isPublished
		);

		return $this->model->update($data, array('PUBLICATION_ENTRY_ID = ?' => $publicationEntry->publicationEntryID));
	}

	public function getEntry($publicationEntryID) {
		$result = NULL;
		$row = $this->model->find($publicationEntryID)->current();
		if ($row) {
			$result = new Publication_Model_Data_PublicationEntry(
				$row->PUBLICATION_ENTRY_ID,
				$row->INSTANCE_ID,
				$row->NOTE,
				Camac_Date::getDateTimeFromDbString($row->PUBLICATION_DATE),
				$row->TEXT,
				$row->IS_PUBLISHED
			);
		}

		return $result;
	}

	public function getEntriesByInstance($instanceID) {
		$select = $this->model->select()
			->where('INSTANCE_ID = ?', $instanceID)
			->order(array('PUBLICATION_DATE ASC'));

		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Publication_Model_Data_PublicationEntry(
				$row->PUBLICATION_ENTRY_ID,
				$row->INSTANCE_ID,
				$row->NOTE,
				Camac_Date::getDateTimeFromDbString($row->PUBLICATION_DATE),
				$row->TEXT,
				$row->IS_PUBLISHED
			);
		}

		return $results;
	}

	public function delete($publicationEntryID) {
		$this->model->delete(array('PUBLICATION_ENTRY_ID = ?' => $publicationEntryID));
	}
}