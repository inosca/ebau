<?php

class Documents_Model_Mapper_AttachmentSection {
	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Documents_Model_DbTable_AttachmentSection();
	}

	public function save(Documents_Model_Data_AttachmentSection $attachmentSection) {
		$data = array(
			'NAME' => $attachmentSection->name
		);

		return $this->model->insert($data);
	}

	public function update(Documents_Model_Data_AttachmentSection $attachmentSection) {
		$data = array(
			'NAME' => $attachmentSection->name
		);

		$this->model->update(
			$data,
			array('ATTACHMENT_SECTION_ID = ?' => $attachmentSection->attachmentSectionID)
		);
	}

	public function getEntry($id) {
		$result = NULL;

		$row = $this->model->find($id)->current();

		if ($row) {
			$result = new Documents_Model_Data_AttachmentSection(
				$row->ATTACHMENT_SECTION_ID,
				$row->NAME,
				$row->SORT
			);
		}

		return $result;
	}

	public function getEntries() {
		$select = $this->model->select()->order(array('SORT ASC'));

		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Documents_Model_Data_AttachmentSection(
				$row->ATTACHMENT_SECTION_ID,
				$row->NAME,
				$row->SORT
			);
		}

		return $results;
	}

	public function delete($attachmentSectionID) {
		$this->model->delete(array('ATTACHMENT_SECTION_ID = ?' => $attachmentSectionID));
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function updatePosition($id, $position) {
		$data = array(
			'SORT' => $position
		);
		$this->model->update($data, array('ATTACHMENT_SECTION_ID = ?' => $id));
	}
}
