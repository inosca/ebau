<?php

class Documents_Data_AttachmentextensionRole_Form extends Camac_Form_Admin {
	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('select', 'roleID', array(
			'label' => $this->getTranslator()->translate('Role'),
			'class' => $select,
			'multiOptions' => $this->getRoles()
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

	public function populate(Documents_Model_Data_AttachmentExtensionRole $attachmentExtensionRole) {
		$values = array();
		$values['roleID']              = $attachmentExtensionRole->roleID;
		$values['attachmentExtensionID'] = $attachmentExtensionRole->attachmentExtensionID;

		return parent::populate($values);
	}

	private function getRoles() {
		$rolesDB = new Camac_Model_DbTable_Account_Role();
		$rows =  $rolesDB->fetchAll($rolesDB->select()->order('NAME'));

		$roles = array();
		foreach ($rows as $row) {
			$roles[$row->ROLE_ID] = $row->NAME;
		}

		return $roles;
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
