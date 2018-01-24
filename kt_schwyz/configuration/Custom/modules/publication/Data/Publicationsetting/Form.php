<?php

class Publication_Data_Publicationsetting_Form extends Camac_Form_Admin {

	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('text', 'key', array(
			'label' => $this->getTranslator()->translate('Key') . ' *',
			'class' => 'text',
			'required' => 'true',
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 64)
			)
		));

		$this->addElement('textarea', 'value', array(
			'label' => $this->getTranslator()->translate('Value'),
			'class' => 'text'
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Publication_Model_Data_PublicationSetting $publicationSetting) {
		$values = array();
		$values['key'] = $publicationSetting->key;
		$values['value'] = $publicationSetting->value;

		return parent::populate($values);
	}
}