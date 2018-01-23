<?php

class Publication_Model_Data_PublicationEntry {

	public $publicationEntryID;

	public $instanceID;

	public $note;

	public $publicationDate;

	public $text;

	public $isPublished;

	public function __construct(
		$publicationEntryID,
		$instanceID,
		$note,
		$publicationDate,
		$text = null,
		$isPublished = 0
	) {
		$this->publicationEntryID = $publicationEntryID;
		$this->instanceID         = $instanceID;
		$this->note               = $note;
		$this->publicationDate    = $publicationDate;
		$this->text               = $text;
		$this->isPublished        = $isPublished;
	}

}