<?php

class Documents_Data_Attachmentextension_Helper_DataDocumentsAttachmentextension extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface { 

	public function __construct() {
		$this->mapper = new Documents_Model_Mapper_AttachmentExtension();
	}

	public function add($form, $id, $mode) {
		$attachmentExtension = new Documents_Model_Data_AttachmentExtension(
			null,
			$form->getValue('name'),
			1
		);
		$this->mapper->save($attachmentExtension);
	}

	public function update($id, $form, $previousLanguage = null) {
		$attachmentExtension  = $this->mapper->getEntry($id);
		$attachmentExtension->name = $form->getValue('name');

		$this->mapper->update($attachmentExtension);
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
		return new Documents_Data_Attachmentextension_Form();
	}
}
