<?php

/**
 * Buildingauthority form. This form is not used for rendering, but just for validation.
 *
 * @author Adrian Wittwer <adrian.wittwer@adfinis-sygroup.ch>
 */
class Buildingauthority_Data_Form extends Camac_Form_Application {

	/**
	 * Constructor.
	 *
	 * @return void
	 */
	public function __construct() {
		$this->addPrefixPath('Camac_Form_Element', 'Camac/Form/Element', 'element');
		$this->addButtons();
		$this->addFormElements();

		parent::__construct();
	}

	private function addFormElements() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());
		$this->setMethod('post');

		$workflowItems = new Camac_Form_Element_CamacHidden('workflowItem', array(
			'isArray' => true
		));
		$workflowItems->addValidator(new Buildingauthority_Data_DateValidator());
		$this->addElement($workflowItems);
	}
}
