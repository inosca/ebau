<?php

class Documents_Data_Attachmentsectionservice_Helper_DataDocumentsAttachmentsectionservice extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface { 

	public function __construct() {
		$this->mapper = new Documents_Model_Mapper_AttachmentSectionService();
	}

	public function add($form, $id, $mode) {
		$attachmentSectionService = new Documents_Model_Data_AttachmentSectionService(
			null,
			$form->getValue('serviceID'),
			$form->getValue('attachmentSectionID'),
			$form->getValue('mode')
		);
		$this->mapper->save($attachmentSectionService);
	}

	public function update($id, $form) {
		$attachmentSectionService                      = $this->mapper->getEntry($id);
		$attachmentSectionService->serviceID           = $form->getValue('serviceID');
		$attachmentSectionService->attachmentSectionID = $form->getValue('attachmentSectionID');
		$attachmentSectionService->mode                = $form->getValue('mode');

		$this->mapper->update($attachmentSectionService);
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
		return new Documents_Data_Attachmentsectionservice_Form();
	}
}
