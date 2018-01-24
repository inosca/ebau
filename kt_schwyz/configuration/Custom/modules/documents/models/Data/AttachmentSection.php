<?php

class Documents_Model_Data_AttachmentSection {
	/**
	 * Attachment section ID
	 *
	 * @var int $attachmentSectionID
	 */
	public $attachmentSectionID;

	/**
	 * Section Name
	 *
	 * @var string $name
	 */
	public $name;


	/** 
	 * Section ordering
	 *
	 * @var int $sort
	 */
	public $sort;

	public function __construct(
		$attachmentSectionID,
		$name,
		$sort = 1
	) {
		$this->attachmentSectionID = $attachmentSectionID;
		$this->name                = $name;
		$this->sort                = $sort;
	}
}
