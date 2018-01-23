<?php

class Documents_Model_Mapper_AttachmentExtension {
	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Documents_Model_DbTable_AttachmentExtension();
	}

	public function save(Documents_Model_Data_AttachmentExtension $attachmentExtension) {
		$data = array(
			'NAME' => $attachmentExtension->name
		);
		
		return $this->model->insert($data);
	}

	public function update(Documents_Model_Data_AttachmentExtension $attachmentExtension) {
		$data = array(
			'NAME' => $attachmentExtension->name
		);

		$this->model->update(
			$data,
			array('ATTACHMENT_EXTENSION_ID = ?' => $attachmentExtension->attachmentExtensionID)
		);
	}

	public function getEntry($id) {
		$result = NULL;

		$row = $this->model->find($id)->current();

		if ($row) {
			$result = new Documents_Model_Data_AttachmentExtension(
				$row->ATTACHMENT_EXTENSION_ID,
				$row->NAME
			);
		}

		return $result;
	}

	public function getEntries() {
		$select = $this->model->select();

		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Documents_Model_Data_AttachmentExtension(
				$row->ATTACHMENT_EXTENSION_ID,
				$row->NAME
			);
		}

		return $results;
	}

	public function delete($attachmentExtensionID) {
		$this->model->delete(array('ATTACHMENT_EXTENSION_ID = ?' => $attachmentExtensionID));
	}
}
