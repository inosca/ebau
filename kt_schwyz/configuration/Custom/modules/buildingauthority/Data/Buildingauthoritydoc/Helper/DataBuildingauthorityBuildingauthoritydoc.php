<?php

class Buildingauthority_Data_Buildingauthoritydoc_Helper_DataBuildingauthorityBuildingauthoritydoc extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Buildingauthority_Model_Mapper_BuildingAuthorityDoc();
	}

	public function add($form, $id, $mode) {
		$doc = new Buildingauthority_Model_Data_BuildingAuthorityDoc(
			null,
			$form->getValue('buttonId'),
			$form->getValue('templateClassId'),
			$form->getValue('templateId')
		);
		return $this->mapper->save($doc);
	}

	public function update($id, $form, $previousLanguage = null) {
		$doc = new Buildingauthority_Model_Data_BuildingAuthorityDoc(
			$id,
			$form->getValue('buttonId'),
			$form->getValue('templateClassId'),
			$form->getValue('templateId')
		);
		return $this->mapper->update($doc);
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
		return new Buildingauthority_Data_Buildingauthoritydoc_Form();
	}
}
