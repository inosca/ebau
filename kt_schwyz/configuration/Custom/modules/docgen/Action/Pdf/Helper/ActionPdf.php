<?php

class Docgen_Action_Pdf_Helper_ActionPdf extends Zend_Controller_Action_Helper_Abstract implements Camac_Action_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Docgen_Action_Pdf_Mapper();
	}

	public function add($actionId, $form) {
		$pdfAction = new Docgen_Action_Pdf_Data(
			$actionId,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			$form->getValue('pdf_template_class_id'),
			$form->getValue('pdf_template_id')
		);

		$this->mapper->save($pdfAction);
	}

	public function update($actionId, $form) {
		$pdfAction = new Docgen_Action_Pdf_Data(
			$actionId,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			$form->getValue('pdf_template_class_id'),
			$form->getValue('pdf_template_id')
		);

		$this->mapper->update($pdfAction);
	}

	public function getAction($actionId, $interpreted = false) {
		return $this->mapper->getAction($actionId);
	}

	public function getForm() {
		return new Docgen_Action_Pdf_Form();
	}

	public function injectVariables($actionId, $view) {
	}

	public function getTabs() {
	}

	public function getContextMenu() {
	}

	public function getHandlerAction($actionId) {
		$resourceAction = $this->getAction($actionId, true);
		return new Docgen_Action_Pdf_Action($resourceAction);
	}

	public function delete($actionId) {
		$pdfAction = new Docgen_Action_Pdf_Data(
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

		$this->mapper->delete($pdfAction);
	}

}
