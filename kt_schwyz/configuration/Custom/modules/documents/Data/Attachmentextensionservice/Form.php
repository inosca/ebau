<?php

class Documents_Data_AttachmentextensionService_Form extends Camac_Form_Admin {
	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('select', 'serviceID', array(
			'label' => $this->getTranslator()->translate('Service'),
			'class' => $select,
			'multiOptions' => $this->getServices()
		));

		$this->addElement('select', 'attachmentExtensionID', array(
			'label' => $this->getTranslator()->translate('Attachment Extension'),
			'class' => $select,
			'multiOptions' => $this->getAttachmentExtensions()
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Documents_Model_Data_AttachmentExtensionService $attachmentExtensionService) {
		$values = array();
		$values['serviceID']              = $attachmentExtensionService->serviceID;
		$values['attachmentExtensionID'] = $attachmentExtensionService->attachmentExtensionID;

		return parent::populate($values);
	}

	private function getServices() {
		$servicesDB = new Camac_Model_DbTable_Account_Service();
		$rows =  $servicesDB->fetchAll($servicesDB->select()->order('NAME'));

		$services = array();
		foreach ($rows as $row) {
			$services[$row->SERVICE_ID] = $row->NAME;
		}

		return $services;
	}

	private function getAttachmentExtensions() {
		$attachmentDB = new Documents_Model_DbTable_AttachmentExtension();
		$rows = $attachmentDB->fetchAll($attachmentDB->select());

		$extensions = array();
		foreach ($rows as $row) {
			$extensions[$row->ATTACHMENT_EXTENSION_ID] = $row->NAME;
		}

		return $extensions;
	}
}
