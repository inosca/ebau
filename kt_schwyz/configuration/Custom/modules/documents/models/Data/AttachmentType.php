<?php

class Documents_Model_Data_AttachmentType {

	/**
	 * The id
	 */
	public $attachmentTypeId;

	/**
	 * The type name
	 */
	public $name;

	public function __construct(
		$attachmentTypeId,
		$name
	) {
		$this->attachmentTypeId = $attachmentTypeId;
		$this->name             = $name;
	}
}
