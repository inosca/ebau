<?php

class Publication_Model_Data_PublicationSetting {

	public $publicationSettingID;

	public $key;

	public $value;

	public function __construct(
		$publicationSettingID,
		$key,
		$value
	) {
		$this->publicationSettingID = $publicationSettingID;
		$this->key                  = $key;
		$this->value                = $value;
	}

}