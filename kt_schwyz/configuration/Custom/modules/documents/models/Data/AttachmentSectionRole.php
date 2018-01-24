<?php

class Documents_Model_Data_AttachmentSectionRole {
	/**
	 * Attachment section ID
	 *
	 * @var int $attachmentSectionID
	 */
	public $id;

	/**
	 * Role relation
	 *
	 * @var int $roleID
	 */
	public $roleID;

	/**
	 * Attachment section relation
	 *
	 * @var int 
	 */
	public $attachmentSectionID;

	/**
	 * The permission mode
	 */
	public $mode;


	public function __construct(
		$id,
		$roleID,
		$attachmentSectionID,
		$mode
	) {
		$this->id                  = $id;
		$this->roleID              = $roleID;
		$this->attachmentSectionID = $attachmentSectionID;
		$this->mode                = $mode;
	}
}
