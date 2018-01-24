<?php

class Docgen_Action_Docx_Helper_ActionDocx extends Zend_Controller_Action_Helper_Abstract implements Camac_Action_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Docgen_Action_Docx_Mapper();
	}

	public function add($actionId, $form) {
		$docxAction = new Docgen_Action_Docx_Data(
			$actionId,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			$form->getValue('docx_template_class_id'),
			$form->getValue('docx_template_id')
		);

		$this->mapper->save($docxAction);
	}

	public function update($actionId, $form) {
		$docxAction = new Docgen_Action_Docx_Data(
			$actionId,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			$form->getValue('docx_template_class_id'),
			$form->getValue('docx_template_id')
		);

		$this->mapper->update($docxAction);
	}

	public function getAction($actionId, $interpreted = false) {
		return $this->mapper->getAction($actionId);
	}

	public function getForm() {
		return new Docgen_Action_Docx_Form();
	}

	public function injectVariables($actionId, $view) {}

	public function getTabs() {}

	public function getContextMenu() {}

	public function getHandlerAction($actionId) {
		$resourceAction = $this->getAction($actionId, true);
		return new Docgen_Action_Docx_Action($resourceAction);
	}

	public function delete($actionId) {
		$docxAction = new Docgen_Action_Docx_Data(
			$actionId,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			null
		);

		$this->mapper->delete($docxAction);
	}
}
