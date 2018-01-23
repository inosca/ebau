<?php

class Documents_Data_Attachmentextensionservice_Helper_DataDocumentsAttachmentextensionservice extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface { 

	public function __construct() {
		$this->mapper = new Documents_Model_Mapper_AttachmentExtensionService();
	}

	public function add($form, $id, $mode) {
		$attachmentExtensionService = new Documents_Model_Data_AttachmentExtensionService(
			null,
			$form->getValue('serviceID'),
			$form->getValue('attachmentExtensionID')
		);


		$this->mapper->save($attachmentExtensionService);
	}

	public function update($id, $form) {
		$attachmentExtensionService                        = $this->mapper->getEntry($id);
		$attachmentExtensionService->serviceID             = $form->getValue('serviceID');
		$attachmentExtensionService->attachmentExtensionID = $form->getValue('attachmentExtensionID');

		$this->mapper->update($attachmentExtensionService);
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
		return new Documents_Data_Attachmentextensionservice_Form();
	}
}
