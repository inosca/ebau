<?php

class Buildingauthority_Data_Buildingauthorityemail_Form extends Camac_Form_Admin {

	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('select', 'buttonId', array(
			'label'        => $this->getTranslator()->translate('Button') . ' *',
			'required'     => 'true',
			'multiOptions' => $this->getButtons()
		));

		$this->addElement('text', 'emailSubject', array(
			'label'    => $this->getTranslator()->translate('Email subject') . ' *',
			'class'    => 'text',
			'required' => 'true'
		));

		$this->addElement('textarea', 'emailText', array(
			'label'    => $this->getTranslator()->translate('Email text') . ' *',
			'class'    => 'text',
			'required' => 'true'
		));

		$this->addElement('text', 'fromEmail', array(
			'label'    => $this->getTranslator()->translate('From email') . ' *',
			'class'    => 'text',
			'required' => 'true'
		));

		$this->addElement('text', 'fromName', array(
			'label'    => $this->getTranslator()->translate('From name') . ' *',
			'class'    => 'text',
			'required' => 'true'
		));

		$this->addElement('textarea', 'receiverQuery', array(
			'label'    => $this->getTranslator()->translate('ReceiverQuery') . ' *',
			'class'    => 'text',
			'required' => 'true'
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Buildingauthority_Model_Data_BuildingAuthorityEmail $baEmail) {
		return parent::populate(array(
			'buttonId'      => $baEmail->baButtonId,
			'emailSubject'  => $baEmail->emailSubject,
			'emailText'     => $baEmail->emailText,
			'fromEmail'     => $baEmail->fromEmail,
			'fromName'      => $baEmail->fromName,
			'receiverQuery' => $baEmail->receiverQuery
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
}
