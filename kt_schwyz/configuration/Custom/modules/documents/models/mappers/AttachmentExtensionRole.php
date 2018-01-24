<?php

class Documents_Model_Mapper_AttachmentExtensionRole {
	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Documents_Model_DbTable_AttachmentExtensionRole();
	}

	public function save(Documents_Model_Data_AttachmentExtensionRole $attachmentExtensionRole) {
		$data = array(
			'ATTACHMENT_EXTENSION_ID' => $attachmentExtensionRole->attachmentExtensionID,
			'ROLE_ID'                 => $attachmentExtensionRole->roleID
		);

		return $this->model->insert($data);
	}

	public function update(Documents_Model_Data_AttachmentExtensionRole $attachmentExtensionRole) {
		$data = array(
			'ATTACHMENT_EXTENSION_ID' => $attachmentExtensionRole->attachmentExtensionID,
			'ROLE_ID'                 => $attachmentExtensionRole->roleID
		);

		$this->model->update(
			$data,
			array('ID = ?' => $attachmentExtensionRole->id)
		);
	}

	public function getEntry($id) {
		$result = NULL;

		$row = $this->model->find($id)->current();

		if ($row) {
			$result = new Documents_Model_Data_AttachmentExtensionRole(
				$row->ID,
				$row->ROLE_ID,
				$row->ATTACHMENT_EXTENSION_ID
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
			$results[] = new Documents_Model_Data_AttachmentExtensionRole(
				$row->ID,
				$row->ROLE_ID,
				$row->ATTACHMENT_EXTENSION_ID
			);
		}

		return $results;
	}

	public function delete($attachmentExtensionRoleID) {
		$this->model->delete(array('ID = ?' => $attachmentExtensionRoleID));
	}
}
