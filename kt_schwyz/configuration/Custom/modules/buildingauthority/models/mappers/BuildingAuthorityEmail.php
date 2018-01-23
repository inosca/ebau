<?php

class Buildingauthority_Model_Mapper_BuildingAuthorityEmail extends Custom_CamacMapper {

	protected $dbTable = "Buildingauthority_Model_DbTable_BuildingAuthorityEmail";
	protected $pk_prop = "baEmailId";
	protected $pk_col  = "BUILDING_AUTHORITY_EMAIL_ID";

	public function rowToModel($row) {
		return new Buildingauthority_Model_Data_BuildingAuthorityEmail(
			$row['BUILDING_AUTHORITY_EMAIL_ID'],
			$row['BUILDING_AUTHORITY_BUTTON_ID'],
			$row['EMAIL_SUBJECT'],
			$row['EMAIL_TEXT'],
			$row['FROM_EMAIL'],
			$row['FROM_NAME'],
			$row['RECEIVER_QUERY']
		);
	}

	public function modelToRow($model) {
		return array(
			'BUILDING_AUTHORITY_BUTTON_ID' => $model->baButtonId,
			'EMAIL_SUBJECT'                => $model->emailSubject,
			'EMAIL_TEXT'                   => $model->emailText,
			'FROM_EMAIL'                   => $model->fromEmail,
			'FROM_NAME'                    => $model->fromName,
			'RECEIVER_QUERY'               => $model->receiverQuery
		);
	}

	public function getEmailsFromButton($buttonId) {
		$select = $this->model->select()->where(
			'BUILDING_AUTHORITY_BUTTON_ID = ?', $buttonId
		);

		return array_map(
			array($this, 'rowToModel'),
			$this->model->fetchAll($select)->toArray()
		);
	}
}
