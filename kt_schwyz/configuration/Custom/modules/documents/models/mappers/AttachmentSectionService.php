<?php

class Documents_Model_Mapper_AttachmentSectionService {
	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Documents_Model_DbTable_AttachmentSectionService();
	}

	public function save(Documents_Model_Data_AttachmentSectionService $attachmentSectionService) {
		$data = array(
			'ATTACHMENT_SECTION_ID' => $attachmentSectionService->attachmentSectionID,
			'SERVICE_ID'            => $attachmentSectionService->serviceID,
			'MODE'                  => $attachmentSectionService->mode
		);

		return $this->model->insert($data);
	}

	public function update(Documents_Model_Data_AttachmentSectionService $attachmentSectionService) {
		$data = array(
			'ATTACHMENT_SECTION_ID' => $attachmentSectionService->attachmentSectionID,
			'SERVICE_ID'            => $attachmentSectionService->serviceID,
			'MODE'                  => $attachmentSectionService->mode
		);

		$this->model->update(
			$data,
			array('ID = ?' => $attachmentSectionService->id)
		);
	}

	public function getEntry($id) {
		$result = NULL;

		$row = $this->model->find($id)->current();

		if ($row) {
			$result = new Documents_Model_Data_AttachmentSectionService(
				$row->ID,
				$row->SERVICE_ID,
				$row->ATTACHMENT_SECTION_ID,
				$row->MODE
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
			$results[] = new Documents_Model_Data_AttachmentSectionService(
				$row->ID,
				$row->SERVICE_ID,
				$row->ATTACHMENT_SECTION_ID,
				$row->MODE
			);
		}

		return $results;
	}

	public function delete($attachmentSectionServiceID) {
		$this->model->delete(array('ID = ?' => $attachmentSectionServiceID));
	}
}
