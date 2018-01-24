<?php

class Documents_Data_Attachmentsectionrole_Helper_DataDocumentsAttachmentsectionrole extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface { 

	public function __construct() {
		$this->mapper = new Documents_Model_Mapper_AttachmentSectionRole();
	}

	public function add($form, $id, $mode) {
		$attachmentSectionRole = new Documents_Model_Data_AttachmentSectionRole(
			null,
			$form->getValue('roleID'),
			$form->getValue('attachmentSectionID'),
			$form->getValue('mode')
		);
		$this->mapper->save($attachmentSectionRole);
	}

	public function update($id, $form, $previousLanguage = null) {
		$attachmentSectionRole  = $this->mapper->getEntry($id);
		$attachmentSectionRole->roleID              = $form->getValue('roleID');
		$attachmentSectionRole->attachmentSectionID = $form->getValue('attachmentSectionID');
		$attachmentSectionRole->mode                = $form->getValue('mode');

		$this->mapper->update($attachmentSectionRole);
	}

	public function delete($id) {
		$this->mapper->delete($id);
	}

	public function move($id, $targetId, $mode) {
	}

	public function getRows() {
		return $this->mapper->getEntries();
	}

	public function getData($id, $language = null) {
		return $this->mapper->getEntry($id);
	}

	public function getForm() {
		return new Documents_Data_Attachmentsectionrole_Form();
	}
}
