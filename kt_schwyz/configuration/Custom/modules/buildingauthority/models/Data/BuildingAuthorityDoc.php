<?php

class Buildingauthority_Model_Data_BuildingAuthorityDoc {

	public $baDocId;

	public $baButtonId;

	public $templateClassId;

	public $templateId;

	public function __construct(
		$baDocId,
		$baButtonId,
		$templateClassId,
		$templateId
	) {
		$this->baDocId         = $baDocId;
		$this->baButtonId      = $baButtonId;
		$this->templateClassId = $templateClassId;
		$this->templateId      = $templateId;
	}

	public function getButton() {
		$mapper = new Buildingauthority_Model_Mapper_BuildingAuthorityButton();
		return $mapper->getButton($this->baButtonId);
	}

	public function getTemplateClass() {
		$mapper = new Docgen_Model_Mapper_Templateclass();
		return $mapper->getTemplateClass($this->templateClassId);
	}

	public function getTemplate() {
		$mapper = new Docgen_Model_Mapper_Template();
		return $mapper->getTemplate($this->templateId);
	}
}
