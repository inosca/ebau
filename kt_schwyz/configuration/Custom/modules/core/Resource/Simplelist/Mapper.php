<?php

class Core_Resource_Simplelist_Mapper extends Custom_CamacMapper {

	protected $dbTable = "Core_Resource_Simplelist_DbTable";
	protected $pk_method = "getResourceId";
	protected $pk_col  = "RESOURCE_ID";

	public function rowToModel($row) {
		throw new Exception('Not implemented');
	}

	public function modelToRow($model) {
		return array(
			'RESOURCE_ID' => $model->getResourceId(),
			'INSTANCE_STATES' => implode(",", $model->instanceStates)
		);
	}

	/**
	 * Returns a single resource.
	 *
	 * @param int $resourceId
	 * @return Camac_Resource_List_Data
	 */
	public function getResource($resourceId) {
		$result = NULL;

		$select = $this->model->select()
				->from('R_SIMPLE_LIST', '*')
				->joinLeft('RESOURCE', '"RESOURCE"."RESOURCE_ID" = "R_SIMPLE_LIST"."RESOURCE_ID"')
				->where('"R_SIMPLE_LIST"."RESOURCE_ID" = ?', $resourceId)
				->setIntegrityCheck(false);

		$row = $this->model->fetchAll($select)->current();

		if ($row) {
			$result = new Core_Resource_Simplelist_Data($row->RESOURCE_ID, $row->AVAILABLE_RESOURCE_ID, $row->NAME, $row->DESCRIPTION, $row->TEMPLATE, $row->CLASS, $row->HIDDEN, $row->SORT, $row->INSTANCE_STATES);
		}

		return $result;
	}
}
