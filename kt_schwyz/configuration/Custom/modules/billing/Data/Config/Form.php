<?php


class Billing_Data_Config_Form extends Camac_Form_Admin {
	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());


		$this->addElement('text', 'name', array(
			'label' => $this->getTranslator()->translate('Name'),
			'class' => 'text',
			'required' => true,
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 100)
			)
		));

		$this->addElement('text', 'value', array(
			'label' => $this->getTranslator()->translate('Value'),
			'class' => 'text',
			'required' => true,
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 300)
			)
		));


		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));


		$this->initDisplayGroup();
	}

	/**
	 * @SuppressWarnings(unused)
	 */
	public function populate(Billing_Model_Data_Config $config) {
		$values = array();
		$values['name']     = $config->name;
		$values['value']  = $config->value;
		return parent::populate($values);
	}
}


