<?php

class Buildingauthority_Data_Buildingauthoritybutton_Helper_DataBuildingauthorityBuildingauthoritybutton extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Buildingauthority_Model_Mapper_BuildingAuthorityButton();
	}

	public function add($form, $id, $mode) {
		$button = new Buildingauthority_Model_Data_BuildingAuthorityButton(
			null,
			$form->getValue('label')
		);
		return $this->mapper->save($button);
	}

	public function update($id, $form, $previousLanguage = null) {
		$button = new Buildingauthority_Model_Data_BuildingAuthorityButton(
			$id,
			$form->getValue('label')
		);
		$this->mapper->update($button);
	}

	public function delete($id) {
		$this->mapper->delete($id);
	}

	public function move($id, $targetId, $mode) {}

	public function getRows() {
		return $this->mapper->getButtons();
	}

	public function getData($id, $language = null) {
		return $this->mapper->getButton($id);
	}

	public function getForm() {
		return new Buildingauthority_Data_Buildingauthoritybutton_Form();
	}
}
