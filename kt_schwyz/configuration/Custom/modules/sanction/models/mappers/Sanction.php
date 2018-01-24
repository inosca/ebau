<?php

class Sanction_Model_Mapper_Sanction extends Custom_CamacMapper {

	public $dbTable = "Sanction_Model_DbTable_Sanction";
	public $pk_prop = "sanctionID";
	public $pk_col = "SANCTION_ID";

	public function getEntries($instanceID, $serviceID = null) {
		$select = $this->model->select()
			->from('SANCTION')
			->setIntegrityCheck(false)
			->joinLeft(array('U' =>'USER'), 'U.USER_ID = SANCTION.USER_ID', array('USERNAME'))
			->joinLeft(array('U2' =>'USER'), 'U2.USER_ID = SANCTION.FINISHED_BY_USER_ID', array('FINISHED_BY_USERNAME' => 'USERNAME'))
			->where('INSTANCE_ID = ?', $instanceID)
			->order(array('START_DATE ASC'));

		if ($serviceID) {
			$select = $select->where('SERVICE_ID = ?', $serviceID);
		}

		return array_map(array($this, 'rowToModel'), $this->model->fetchAll($select)->toArray());
	}

	public function isFinished($instanceID) {
		$select = $this->model->select()
			->from('SANCTION')
			->where('INSTANCE_ID = ?', $instanceID)
			->where('IS_FINISHED = 0');

		return count($this->model->fetchAll($select)) === 0;
	}

	public function rowToModel($row) {
		return new Sanction_Model_Data_Sanction(
			$row['SANCTION_ID'],
			$row['INSTANCE_ID'],
			$row['SERVICE_ID'],
			$row['USER_ID'],
			array_key_exists('USERNAME', $row) ? $row['USERNAME'] : null,
			$row['TEXT'],
			Camac_Date::getDateTimeFromDbString($row['START_DATE']),
			Camac_Date::getDateTimeFromDbString($row['DEADLINE_DATE']),
			Camac_Date::getDateTimeFromDbString($row['END_DATE']),
			$row['NOTICE'],
			$row['IS_FINISHED'],
			$row['FINISHED_BY_USER_ID'],
			array_key_exists('FINISHED_BY_USERNAME', $row) ? $row['FINISHED_BY_USERNAME'] : null
		);
	}

	public function modelToRow($sanction) {
		return array(
			'INSTANCE_ID'         => $sanction->instanceID,
			'SERVICE_ID'          => $sanction->serviceID,
			'USER_ID'             => $sanction->userID,
			'TEXT'                => $sanction->text,
			'NOTICE'              => $sanction->notice,
			'START_DATE'          => Camac_Date::getDbStringFromDateTime($sanction->startDate),
			'DEADLINE_DATE'       => Camac_Date::getDbStringFromDateTime($sanction->deadlineDate),
			'END_DATE'            => Camac_Date::getDbStringFromDateTime($sanction->endDate),
			'IS_FINISHED'         => $sanction->isFinished,
			'FINISHED_BY_USER_ID' => $sanction->finishedByUserID
		);
	}
}
