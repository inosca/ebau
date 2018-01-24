<?php

class Documents_Data_AttachmentsectionService_Form extends Camac_Form_Admin {
	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('select', 'serviceID', array(
			'label' => $this->getTranslator()->translate('Service'),
			'class' => $select,
			'multiOptions' => $this->getServices()
		));

		$this->addElement('select', 'attachmentSectionID', array(
			'label' => $this->getTranslator()->translate('Attachment Section'),
			'class' => $select,
			'multiOptions' => $this->getAttachmentSections()
		));

		$this->addElement('radio', 'mode', array(
			'label'    => $this->getTranslator()->translate('Mode'),
			'class'    => 'radio',
			'required' => true,
			'multiOptions' => array(
				'read'  => $this->getTranslator()->translate('read'),
				'write' => $this->getTranslator()->translate('write'),
				'admin' => $this->getTranslator()->translate('admin'),
			)
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Documents_Model_Data_AttachmentSectionService $attachmentSectionService) {
		$values = array();
		$values['serviceID']           = $attachmentSectionService->serviceID;
		$values['attachmentSectionID'] = $attachmentSectionService->attachmentSectionID;
		$values['mode']                = $attachmentSectionService->mode;

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

	private function getAttachmentSections() {
		$attachmentDB = new Documents_Model_DbTable_AttachmentSection();
		$rows = $attachmentDB->fetchAll($attachmentDB->select()->order('SORT'));

		$sections = array();
		foreach ($rows as $row) {
			$sections[$row->ATTACHMENT_SECTION_ID] = $row->NAME;
		}

		return $sections;
	}
}
