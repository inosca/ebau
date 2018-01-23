<?php

class Documents_Data_Attachmentextensionrole_Helper_DataDocumentsAttachmentextensionrole extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface { 

	public function __construct() {
		$this->mapper = new Documents_Model_Mapper_AttachmentExtensionRole();
	}

	public function add($form, $id, $mode) {
		$attachmentExtensionRole = new Documents_Model_Data_AttachmentExtensionRole(
			null,
			$form->getValue('roleID'),
			$form->getValue('attachmentExtensionID')
		);


		$this->mapper->save($attachmentExtensionRole);
	}

	public function update($id, $form) {
		$attachmentExtensionRole                        = $this->mapper->getEntry($id);
		$attachmentExtensionRole->roleID                = $form->getValue('roleID');
		$attachmentExtensionRole->attachmentExtensionID = $form->getValue('attachmentExtensionID');

		$this->mapper->update($attachmentExtensionRole);
	}

	public function delete($id) {
		$this->mapper->delete($id);
	}

	public function move($id, $targetId, $mode) {
	}

	public function getRows() {
		return $this->mapper->getEntries();
	}

	public function getData($id) {
		return $this->mapper->getEntry($id);
	}

	public function getForm() {
		return new Documents_Data_Attachmentextensionrole_Form();
	}
}
