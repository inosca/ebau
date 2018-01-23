<?php

/**
 * Action docx data model.
 *
 * @package Docgen\Action\Docx
 */
class Docgen_Action_Docx_Data extends Camac_Model_Data_Resource_Action {
	protected $docxTemplateclassId;
	protected $docxTemplateId;

	/**
	 * Constructor.
	 *
	 * @param int $actionId
	 * @param string $availableActionId
	 * @param int $buttonId
	 * @param string $name
	 * @param string $description
	 * @param string $confirmMessage
	 * @param string $errorMessage
	 * @param bool $executeAlways
	 * @param int $sort
	 * @return void
	 */
	public function __construct($actionId, $availableActionId, $buttonId, $name, $description, $confirmMessage, $errorMessage, $executeAlways, $sort, $docxTemplateclassId, $docxTemplateId) {

		parent::__construct($actionId, $availableActionId, $buttonId, $name, $description, $confirmMessage, $errorMessage, $executeAlways, $sort);

		$this->docxTemplateclassId = $docxTemplateclassId;
		$this->docxTemplateId = $docxTemplateId;
	}

	public function getTemplateclassId() {
		return $this->docxTemplateclassId;
	}
	
	public function getTemplateId() {
		return $this->docxTemplateId;
	}
}
