<?php


class Documents_Model_Data_AttachmentExtension  {
	/**
	 * The ID
	 */
	public $attachmentExtensionID;

	/**
	 * The extension
	 */
	public $name;

	public function __construct(
		$attachmentExtensionID,
		$name
	) {
		$this->attachmentExtensionID = $attachmentExtensionID;
		$this->name = $name;
	}
}
