<?php

class Documents_Data_Attachmenttype_Form extends Camac_Form_Admin {

	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('text', 'name', array(
			'label'    => $this->getTranslator()->translate('Name') .' *',
			'class'    => 'text',
			'required' => true,
			'filters'  => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags'  => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 250)
			)
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Documents_Model_Data_AttachmentType $attachmentType) {
		$values = array();
		$values['name'] = $attachmentType->name;

		return parent::populate($values);
	}
}
