<?php

class Notification_Data_Template_Form extends Camac_Form_Admin {

	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$languages = Zend_Registry::get('config')->frontend->languages->toArray();

		$api = Notification_Manager_API::getInstance();

		$languagesOptions = array_combine($languages, $languages);

		$this->addElement('select', 'translation', array(
			'label' => 'Language',
			'class' => 'select searchable',
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'multiOptions' => $languagesOptions,
			'value' => strtoupper((new Zend_Session_Namespace('camac'))->translation)
		));

		parent::init();
		$tr = $this->getTranslator();

		$this->addElement('text', 'PURPOSE', array(
			'label' => $tr->translate('Nutzung (Zweck)'),
			'required' => true,
		));
		$this->addElement('text', 'SUBJECT', array(
			'label' => $tr->translate('Betreff'),
			'required' => true,
			'description' => $api->getTemplateHelpText(),
			// The parser must support the Zend_Validate API.
			'validators' => [$api->getParser()]
		));

		$this->addElement('textarea', 'BODY', array(
			'label' => $tr->translate('Mail-Inhalt'),
			'required' => true,
			'description' => $api->getTemplateHelpText(),
			// The parser must support the Zend_Validate API.
			'validators' => [$api->getParser()]
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->{'PURPOSE'}->getDecorator('Label')->setOption('tagClass', 'translatable-field');
		$this->{'PURPOSE'}->getDecorator('HtmlTag')->setOption('class', 'translatable-field');
		$this->{'SUBJECT'}->getDecorator('Label')->setOption('tagClass', 'translatable-field');
		$this->{'SUBJECT'}->getDecorator('HtmlTag')->setOption('class', 'translatable-field');
		$this->{'BODY'}->getDecorator('Label')->setOption('tagClass', 'translatable-field');
		$this->{'BODY'}->getDecorator('HtmlTag')->setOption('class', 'translatable-field');

		$this->initDisplayGroup();
	}

	/**
	 * Populates the form.
	 *
	 * @param stdClass $proposalAction
	 * @return Zend_Form
	 */
	public function populate($obj) {

		$values = array();

		$values['PURPOSE']     = $obj->PURPOSE;
		$values['BODY']        = $obj->BODY;
		$values['SUBJECT']     = $obj->SUBJECT;
		$values['translation'] = $obj->translation;

		return parent::populate($values, $obj);

	}
}
