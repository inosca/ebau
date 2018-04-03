<?php

class Notification_Action_ActionConfig_Form extends Admin_Form_Resource_Action {

	public function init() {
		parent::init();
		$tr = $this->getTranslator();

		$this->addElement('select', 'template', array(
			'label' => $tr->translate('Template'),
			'class' => 'select searchable',
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'multiOptions' => $this->getTemplates()
		));

		$this->addElement('select', 'recipientType', array(
			'label' => $tr->translate('Recipients'),
			'class' => 'select searchable',
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'multiOptions' => $this->getRecipientTypes()
		));

		$this->addElement('select', 'processor', array(
			'label' => $tr->translate('Processor'),
			'class' => 'select searchable',
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'multiOptions' => $this->getProcessors()
		));

	}

	private function getProcessors() {
		$api        = Notification_Manager_API::getInstance();
		$processors = $api->getProcessors();

		$res = [];
		foreach ($processors as $obj) {
			$res[get_class($obj)] = $obj->getTranslatedName();
		}

		return $res;
	}
	private function getRecipientTypes() {
		$api = Notification_Manager_API::getInstance();
		$types = $api->getRecipientTypes();

		$res = [];
		foreach ($types as $obj) {
			$res[get_class($obj)] = $obj->getTranslatedName();
		}

		return $res;
	}

	private function getTemplates($language=NULL) {
		$lang = Camac_Utility::getLanguageIfNull($language);
		$table = new Notification_Model_DbTable_TemplateT();
		$query = $table->select()
			->where($table->getAdapter()->quoteInto('LANGUAGE = ?', $lang))
			->order('PURPOSE');

		$res = [];

		foreach ($table->fetchAll($query) as $row) {
			$res[$row['TEMPLATE_ID']] = $row['PURPOSE'];
		}
		return $res;
	}

	/**
	 * Populates the form.
	 *
	 * @param Camac_Model_Data_Resource_Action $proposalAction
	 * @return Zend_Form
	 */
	public function populate(Camac_Model_Data_Resource_Action $obj) {

		$values = array();

		$values['processor']     = $obj->processor;
		$values['recipientType'] = $obj->recipientType;
		$values['template']      = $obj->templateId;

		return parent::populate($values, $obj);
	}
}
