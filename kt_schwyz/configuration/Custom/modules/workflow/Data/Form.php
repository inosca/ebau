<?php

/**
 * Workflow form. This form is not used for rendering, but just for validation.
 *
 * @author Christian Zosel <christian.zosel@adfinis-sygroup.ch>
 */
class Workflow_Data_Form extends Camac_Form_Application {

	/**
	 * Constructor.
	 *
	 * @return void
	 */
	public function __construct() {
		$this->addPrefixPath('Camac_Form_Element', 'Camac/Form/Element', 'element');

		$this->addButtons();

		// Add the elements to the form
		$this->addFormElements();

		parent::__construct();

	}

	/**
	 * Inizializes the form elements.
	 *
	 * @return void
	 */
	private function addFormElements() {

		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());
		$this->setAttrib('enctype', 'multipart/form-data');
		$this->setMethod('post');

		$workflowEntries = new Camac_Form_Element_CamacHidden('workflowEntries', array(
			'isArray' => true
		));
		$workflowEntries->addValidator(new Workflow_Data_DateValidator());
		$this->addElement($workflowEntries);
	}
}
