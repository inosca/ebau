<?php

class Documents_Data_AttachmentsectionRole_Form extends Camac_Form_Admin {
	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('select', 'roleID', array(
			'label' => $this->getTranslator()->translate('Role'),
			'class' => $select,
			'multiOptions' => $this->getRoles()
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

	public function populate(Documents_Model_Data_AttachmentSectionRole $attachmentSectionRole) {
		$values = array();
		$values['roleID']              = $attachmentSectionRole->roleID;
		$values['attachmentSectionID'] = $attachmentSectionRole->attachmentSectionID;
		$values['mode']                = $attachmentSectionRole->mode;

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
