<?php

class Workflow_Model_Mapper_WorkflowItem extends Custom_CamacMapper {

	public $dbTable = "Workflow_Model_DbTable_WorkflowItem";
	public $pk_prop = "workflowItemID";
	public $pk_col = "WORKFLOW_ITEM_ID";

	/**
	 * @SuppressWarnings(short)
	 */
	public function updatePosition($id, $position) {
		$data = array(
			'POSITION' => $position
		);
		$this->model->update($data, array('WORKFLOW_ITEM_ID = ?' => $id));
	}

	public function countWorkflows() {
		return count($this->getAll());
	}

	public function getAllWorkflows() {
		$select = $this->model->select()->order(array('POSITION ASC'));
		return $this->getAll($select);
	}

	public function getWorkflows() {
		$select = $this->model->select()
			->where('"IS_WORKFLOW" = 1')->order(array('POSITION ASC'));
		return $this->getAll($select);
	}

	public function getAutomaticalWorkflows() {
		$select = $this->model->select()->order(array('POSITION ASC'))->where('"AUTOMATICAL" = 1');
		return $this->getAll($select);
	}

	public function getBuildingAuthorityWorkflows() {
		$select = $this->model->select()
			->where('"IS_BUILDING_AUTHORITY" = 1')->order(array('POSITION ASC'));
		return $this->getAll($select);
	}

	public function getAll($select = null) {
		$select = $select ? $select : $this->model->select()
			->order(array('POSITION ASC'));

		return array_map(array($this, 'rowToModel'), $this->model->fetchAll($select)->toArray());
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function getBySection($id, $workflowOnly = true) {
		$select = $this->model->select()
			->where('"WORKFLOW_SECTION_ID" = ?', $id)
			->order('POSITION ASC');
		if ($workflowOnly) {
			$select->where('"IS_WORKFLOW" = 1');
		}
		return $this->getAll($select);
	}

	public function rowToModel($row) {
		return new Workflow_Model_Data_WorkflowItem(
			$row['WORKFLOW_ITEM_ID'],
			$row['NAME'],
			$row['AUTOMATICAL'],
			$row['DIFFERENT_COLOR'],
			$row['POSITION'],
			$row['WORKFLOW_SECTION_ID'],
			$row['IS_WORKFLOW'],
			$row['IS_BUILDING_AUTHORITY']
		);
	}

	public function modelToRow($model) {
		return array(
			'WORKFLOW_ITEM_ID'      => $model->workflowItemID,
			'NAME'                  => $model->name,
			'AUTOMATICAL'           => (int)$model->automatical,
			'DIFFERENT_COLOR'       => (int)$model->differentColor,
			'POSITION'              => $model->position,
			'WORKFLOW_SECTION_ID'   => intval($model->workflowSectionID),
			'IS_WORKFLOW'           => (int)$model->isWorkflow,
			'IS_BUILDING_AUTHORITY' => (int)$model->isBuildingAuthority
		);
	}
}
