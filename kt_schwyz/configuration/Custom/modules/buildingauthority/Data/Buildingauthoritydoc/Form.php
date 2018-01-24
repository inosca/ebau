<?php

class Buildingauthority_Data_Buildingauthoritydoc_Form extends Camac_Form_Admin {

	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('select', 'buttonId', array(
			'label'        => $this->getTranslator()->translate('Button') . ' *',
			'required'     => 'true',
			'multiOptions' => $this->getButtons()
		));

		$this->addElement('select', 'templateClassId', array(
			'label'        => $this->getTranslator()->translate('Template class') . ' *',
			'required'     => 'true',
			'multiOptions' => $this->getTemplateClasses()
		));

		$this->addElement('select', 'templateId', array(
			'label'        => $this->getTranslator()->translate('Template') . ' *',
			'required'     => 'true',
			'multiOptions' => $this->getTemplates()
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Buildingauthority_Model_Data_BuildingAuthorityDoc $baDoc) {
		return parent::populate(array(
			'buttonId'        => $baDoc->baButtonId,
			'templateClassId' => $baDoc->templateClassId,
			'templateId'      => $baDoc->templateId
		));
	}

	private function getButtons() {
		$buttonDB = new Buildingauthority_Model_DbTable_BuildingAuthorityButton();
		$rows     = $buttonDB->fetchAll($buttonDB->select()->order('LABEL'));

		$buttons = array();
		foreach ($rows as $row) {
			$buttons[$row->BUILDING_AUTHORITY_BUTTON_ID] = $row->LABEL;
		}

		return $buttons;
	}

	private function getTemplateClasses() {
		$templateClassDB = new Docgen_Model_DbTable_Templateclass();
		$rows            = $templateClassDB->fetchAll(
			$templateClassDB->select()->order('NAME')
		);

		$templateClasses = array();
		foreach ($rows as $row) {
			$templateClasses[$row->DOCGEN_TEMPLATE_CLASS_ID] = $row->NAME;
		}

		return $templateClasses;
	}

	private function getTemplates() {
		$templateDB = new Docgen_Model_DbTable_Template();
		$rows       = $templateDB->fetchAll($templateDB->select()->order('NAME'));

		$templates = array();
		foreach ($rows as $row) {
			$templates[$row->DOCGEN_TEMPLATE_ID] = $row->NAME;
		}

		return $templates;
	}
}
