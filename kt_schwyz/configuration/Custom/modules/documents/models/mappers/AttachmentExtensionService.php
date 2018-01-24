<?php

class Documents_Model_Mapper_AttachmentExtensionService {
	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Documents_Model_DbTable_AttachmentExtensionService();
	}

	public function save(Documents_Model_Data_AttachmentExtensionService $attachmentExtensionService) {
		$data = array(
			'ATTACHMENT_EXTENSION_ID' => $attachmentExtensionService->attachmentExtensionID,
			'SERVICE_ID'              => $attachmentExtensionService->serviceID
		);

		return $this->model->insert($data);
	}

	public function update(Documents_Model_Data_AttachmentExtensionService $attachmentExtensionService) {
		$data = array(
			'ATTACHMENT_EXTENSION_ID' => $attachmentExtensionService->attachmentExtensionID,
			'SERVICE_ID'              => $attachmentExtensionService->serviceID
		);

		$this->model->update(
			$data,
			array('ID = ?' => $attachmentExtensionService->id)
		);
	}

	public function getEntry($id) {
		$result = NULL;

		$row = $this->model->find($id)->current();

		if ($row) {
			$result = new Documents_Model_Data_AttachmentExtensionService(
				$row->ID,
				$row->SERVICE_ID,
				$row->ATTACHMENT_EXTENSION_ID
			);
		}

		return $result;
	}

	public function getEntries($serviceID=null) {
		$select = $this->model->select();

		if ($serviceID != null) {
			$select->where('"SERVICE_ID" = ?', $serviceID);
		}

		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Documents_Model_Data_AttachmentExtensionService(
				$row->ID,
				$row->SERVICE_ID,
				$row->ATTACHMENT_EXTENSION_ID
			);
		}

		return $results;
	}

	public function delete($attachmentExtensionServiceID) {
		$this->model->delete(array('ID = ?' => $attachmentExtensionServiceID));
	}
}
