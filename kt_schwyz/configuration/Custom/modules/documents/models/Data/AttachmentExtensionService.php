<?php

class Documents_Model_Data_AttachmentExtensionService {
	/**
	 * Attachment section ID
	 *
	 * @var int $id
	 */
	public $id;

	/**
	 * Service relation
	 *
	 * @var int $serviceID
	 */
	public $serviceID;

	/**
	 * Attachment extension relation
	 *
	 * @var int 
	 */
	public $attachmentExtensionID;

	public function __construct(
		$id,
		$serviceID,
		$attachmentExtensionID
	) {
		$this->id                    = $id;
		$this->serviceID             = $serviceID;
		$this->attachmentExtensionID = $attachmentExtensionID;
	}
}
