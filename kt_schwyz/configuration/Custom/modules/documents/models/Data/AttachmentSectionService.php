<?php

class Documents_Model_Data_AttachmentSectionService {
	/**
	 * Attachment section ID
	 *
	 * @var int $attachmentSectionID
	 */
	public $attachmentSectionServiceID;

	/**
	 * Service relation
	 *
	 * @var int $serviceID
	 */
	public $serviceID;

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
		$serviceID,
		$attachmentSectionID,
		$mode
	) {
		$this->id                  = $id;
		$this->serviceID           = $serviceID;
		$this->attachmentSectionID = $attachmentSectionID;
		$this->mode                = $mode;
	}
}
