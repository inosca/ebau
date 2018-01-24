<?php

class Buildingauthority_Model_Mapper_BuildingAuthorityDoc extends Custom_CamacMapper {

	protected $dbTable = "Buildingauthority_Model_DbTable_BuildingAuthorityDoc";
	protected $pk_prop = "baDocId";
	protected $pk_col  = "BUILDING_AUTHORITY_DOC_ID";

	public function rowToModel($row) {
		return new Buildingauthority_Model_Data_BuildingAuthorityDoc(
			$row['BUILDING_AUTHORITY_DOC_ID'],
			$row['BUILDING_AUTHORITY_BUTTON_ID'],
			$row['TEMPLATE_CLASS_ID'],
			$row['TEMPLATE_ID']
		);
	}

	public function modelToRow($model) {
		return array(
			'BUILDING_AUTHORITY_BUTTON_ID' => $model->baButtonId,
			'TEMPLATE_CLASS_ID'            => $model->templateClassId,
			'TEMPLATE_ID'                  => $model->templateId
		);
	}

	public function getDocsFromButton($buttonId) {
		$select = $this->model->select()->where(
			'BUILDING_AUTHORITY_BUTTON_ID = ?', $buttonId
		);

		return array_map(
			array($this, 'rowToModel'),
			$this->model->fetchAll($select)->toArray()
		);
	}
}
