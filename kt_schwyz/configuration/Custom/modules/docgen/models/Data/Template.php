<?php


class Docgen_Model_Data_Template {

	public $docgenTemplateId;

	public $name;

	public $path;

	public $type;

	public function __construct(
		$docgenTemplateId,
		$name,
		$path,
		$type
	) {
		$this->docgenTemplateId = $docgenTemplateId;
		$this->name             = $name;
		$this->path             = $path;
		$this->type             = $type;
	}
}
