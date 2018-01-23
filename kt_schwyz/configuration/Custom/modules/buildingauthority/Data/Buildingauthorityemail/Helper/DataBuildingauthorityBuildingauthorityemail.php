<?php

class Buildingauthority_Data_Buildingauthorityemail_Helper_DataBuildingauthorityBuildingauthorityemail extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Buildingauthority_Model_Mapper_BuildingAuthorityEmail();
	}

	public function add($form, $id, $mode) {
		$email = new Buildingauthority_Model_Data_BuildingAuthorityEmail(
			null,
			$form->getValue('buttonId'),
			$form->getValue('emailSubject'),
			$form->getValue('emailText'),
			$form->getValue('fromEmail'),
			$form->getValue('fromName'),
			$form->getValue('receiverQuery')
		);
		return $this->mapper->save($email);
	}

	public function update($id, $form, $previousLanguage = null) {
		$email = new Buildingauthority_Model_Data_BuildingAuthorityEmail(
			$id,
			$form->getValue('buttonId'),
			$form->getValue('emailSubject'),
			$form->getValue('emailText'),
			$form->getValue('fromEmail'),
			$form->getValue('fromName'),
			$form->getValue('receiverQuery')
		);
		return $this->mapper->update($email);
	}

	public function delete($id) {
		$this->mapper->delete($id);
	}

	public function move($id, $targetId, $mode) {}

	public function getRows() {
		return $this->mapper->getAll();
	}

	public function getData($id, $language = null) {
		return $this->mapper->getEntry($id);
	}

	public function getForm() {
		return new Buildingauthority_Data_Buildingauthorityemail_Form();
	}
}
