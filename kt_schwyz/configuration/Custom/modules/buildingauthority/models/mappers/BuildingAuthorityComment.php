<?php

class Buildingauthority_Model_Mapper_BuildingAuthorityComment {

	protected $model;

	public function __construct() {
		$this->model = new Buildingauthority_Model_DbTable_BuildingAuthorityComment();
	}

	public function save(Buildingauthority_Model_Data_BuildingAuthorityComment $baComment) {
		$data = array(
			'BUILDING_AUTHORITY_SECTION_ID' => $baComment->baSectionId,
			'INSTANCE_ID'                   => $baComment->instanceId,
			'TEXT'                          => $baComment->text,
			'GROUP'                         => $baComment->group
		);

		return $this->model->insert($data);
	}

	public function update(Buildingauthority_Model_Data_BuildingauthorityComment $baComment) {
		$data = array('TEXT' => $baComment->text, 'GROUP' => $baComment->group);
		$this->model->update(
			$data,
			array('BUILDING_AUTHORITY_COMMENT_ID = ?' => $baComment->baCommentId)
		);
	}

	public function getComment($baCommentId) {
		$result = null;
		$row    = $this->model->find($baCommentId)->current();

		if ($row) {
			$result = new Buildingauthority_Model_Data_BuildingAuthorityComment(
				$baCommentId,
				$row->BUILDING_AUTHORITY_SECTION_ID,
				$row->INSTANCE_ID,
				$row->TEXT,
				$row->GROUP
			);
		}

		return $result;
	}

	public function getCommentsByInstance($instanceId) {
		$select = $this->model->select()->where(
			sprintf('INSTANCE_ID = %d', $instanceId)
		)->order(array('BUILDING_AUTHORITY_SECTION_ID'));

		$results = array();
		foreach ($this->model->fetchAll($select) as $row) {
			$baSectionId = $row->BUILDING_AUTHORITY_SECTION_ID;
			$results[$baSectionId][$row->GROUP] = new Buildingauthority_Model_Data_BuildingAuthorityComment(
				$row->BUILDING_AUTHORITY_COMMENT_ID,
				$baSectionId,
				$row->INSTANCE_ID,
				$row->TEXT,
				$row->GROUP
			);
		}

		return $results;
	}

	public function delete($baCommentId) {
		$this->model->delete(array(
			'BUILDING_AUTHORITY_COMMENT_ID = ?' => $baCommentId
		));
	}
}
