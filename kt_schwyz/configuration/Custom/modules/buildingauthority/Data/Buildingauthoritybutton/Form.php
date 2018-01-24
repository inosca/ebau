<?php

class Buildingauthority_Data_Buildingauthoritybutton_Form extends Camac_Form_Admin {

	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('text', 'label', array(
			'label'      => $this->getTranslator()->translate('Name') . ' *',
			'class'      => 'text',
			'required'   => 'true',
			'filters'    => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags'  => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 128)
			)
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Buildingauthority_Model_Data_BuildingAuthorityButton $baButton) {
		return parent::populate(array('label' => $baButton->label));
	}
}
