<?php

class Portal_Model_Mapper_ProjectSubmitterData extends Custom_CamacMapper {

	protected $dbTable = "Portal_Model_DbTable_ProjectSubmitterData";
	protected $pk_prop = "instanceId";
	protected $pk_col  = "INSTANCE_ID";

	public function rowToModel($row) {
		return new Portal_Model_Data_ProjectSubmitterData(
			$row['INSTANCE_ID'],
			$row['NAME'],
			$row['EMAIL'],
			$row['ANSWER']
		);
	}

	public function modelToRow($model) {
		return array(
			'INSTANCE_ID' => $model->instanceId,
			'NAME'        => $model->name,
			'EMAIL'       => $model->email,
			'ANSWER'      => $model->answer
		);
	}

}
