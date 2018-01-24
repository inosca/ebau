<?php

class Documents_Model_Mapper_AttachmentSectionRole {
	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Documents_Model_DbTable_AttachmentSectionRole();
	}

	public function save(Documents_Model_Data_AttachmentSectionRole $attachmentSectionRole) {
		$data = array(
			'ATTACHMENT_SECTION_ID' => $attachmentSectionRole->attachmentSectionID,
			'ROLE_ID'               => $attachmentSectionRole->roleID,
			'MODE'                  => $attachmentSectionRole->mode
		);

		return $this->model->insert($data);
	}

	public function update(Documents_Model_Data_AttachmentSectionRole $attachmentSectionRole) {
		$data = array(
			'ATTACHMENT_SECTION_ID' => $attachmentSectionRole->attachmentSectionID,
			'ROLE_ID'               => $attachmentSectionRole->roleID,
			'MODE'                  => $attachmentSectionRole->mode
		);

		$this->model->update(
			$data,
			array('ID = ?' => $attachmentSectionRole->id)
		);
	}

	public function getEntry($id) {
		$result = NULL;

		$row = $this->model->find($id)->current();

		if ($row) {
			$result = new Documents_Model_Data_AttachmentSectionRole(
				$row->ID,
				$row->ROLE_ID,
				$row->ATTACHMENT_SECTION_ID,
				$row->MODE
			);
		}

		return $result;
	}

	public function getEntries($roleID=null) {
		$select = $this->model->select();

		if ($roleID != null) {
			$select->where('"ROLE_ID" = ?', $roleID);
		}

		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Documents_Model_Data_AttachmentSectionRole(
				$row->ID,
				$row->ROLE_ID,
				$row->ATTACHMENT_SECTION_ID,
				$row->MODE
			);
		}

		return $results;
	}

	public function delete($attachmentSectionRoleID) {
		$this->model->delete(array('ID = ?' => $attachmentSectionRoleID));
	}
}
