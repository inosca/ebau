<?php

class Documents_Data_Attachmentsection_Helper_DataDocumentsAttachmentsection extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface { 

	public function __construct() {
		$this->mapper = new Documents_Model_Mapper_AttachmentSection();
	}

	public function add($form, $id, $mode) {
		$attachmentSection = new Documents_Model_Data_AttachmentSection(
			null,
			$form->getValue('name'),
			1
		);
		$this->mapper->save($attachmentSection);
	}

	public function update($id, $form) {
		$attachmentSection  = $this->mapper->getEntry($id);
		$attachmentSection->name = $form->getValue('name');

		$this->mapper->update($attachmentSection);
	}

	public function delete($id) {
		$this->mapper->delete($id);
	}

	public function move($id, $targetId, $mode) {
		$currentPosition = $this->mapper->getEntry($id)->sort;
		$targetPosition  = $this->mapper->getEntry($targetId)->sort;

		$sections = $this->mapper->getEntries();

		$newPosition = $mode == 'after' ? $targetPosition + 1 : $targetPosition;
		$elem = array_splice($sections, $currentPosition -1, 1);
		$result = array_merge(
			array_slice($sections, 0, $newPosition -1), 
			$elem,
			array_slice($sections, $newPosition - 1)
		);

		foreach ($result as $key => $section) {
			$this->mapper->updatePosition($section->attachmentSectionID, $key + 1);
		}
	}

	public function getRows() {
		return $this->mapper->getEntries();
	}

	public function getData($id) {
		return $this->mapper->getEntry($id);
	}

	public function getForm() {
		return new Documents_Data_Attachmentsection_Form();
	}
}
