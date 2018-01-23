<?php

class Workflow_Model_Mapper_WorkflowSection extends Custom_CamacMapper {

	public $dbTable = "Workflow_Model_DbTable_WorkflowSection";
	public $pk_prop = "workflowSectionID";
	public $pk_col = "WORKFLOW_SECTION_ID";

	public function getAll($select = null) {
		$select = $select ? $select : $this->model->select()
			->from('WORKFLOW_SECTION')
			->order('SORT ASC');

		return array_map('self::rowToModel', $this->model->fetchAll($select)->toArray());
	}

	public function rowToModel($row) {
		return new Workflow_Model_Data_WorkflowSection(
			$row['WORKFLOW_SECTION_ID'],
			$row['NAME'],
			$row['SORT']
		);
	}

	public function modelToRow($model) {
		return array(
			'WORKFLOW_SECTION_ID' => $model->workflowSectionID,
			'NAME'                => $model->name,
			'SORT'                => $model->sort
		);
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function updateSort($id, $sort) {
		$data = array(
			'SORT' => $sort
		);
		$this->model->update($data, array('WORKFLOW_SECTION_ID = ?' => $id));
	}
}
