<?php

class Documents_Model_Data_AttachmentExtensionRole {
	/**
	 * Attachment section ID
	 *
	 * @var int $id
	 */
	public $id;

	/**
	 * Role relation
	 *
	 * @var int $roleID
	 */
	public $roleID;

	/**
	 * Attachment extension relation
	 *
	 * @var int 
	 */
	public $attachmentExtensionID;

	/**
	 * The permission mode
	 */
	public $mode;


	public function __construct(
		$id,
		$roleID,
		$attachmentExtensionID
	) {
		$this->id                  = $id;
		$this->roleID              = $roleID;
		$this->attachmentExtensionID = $attachmentExtensionID;
	}
}
