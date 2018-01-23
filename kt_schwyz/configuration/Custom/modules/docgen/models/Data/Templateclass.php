<?php

class Docgen_Model_Data_Templateclass {

	public $docgenTemplateclassId;

	public $name;

	public $path;

	public $type;

	public function __construct(
		$docgenTemplateId,
		$name,
		$path,
		$type
	) {
		$this->docgenTemplateclassId = $docgenTemplateId;
		$this->name                  = $name;
		$this->path                  = $path;
		$this->type                  = $type;
	}
}
