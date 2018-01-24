<?php

class Docgen_Action_Docx_Mapper {

	protected $model;

	public function __construct() {
		$this->model = new Docgen_Action_Docx_DbTable();
	}

	public function save(Docgen_Action_Docx_Data $docxAction) {
		$data = array(
			'DOCGEN_TEMPLATE_CLASS_ID' => $docxAction->getTemplateclassId(),
			'DOCGEN_TEMPLATE_ID'       => $docxAction->getTemplateId(),
			'ACTION_ID'                => $docxAction->getActionId(),
		);

		$this->model->insert($data);
	}

	public function update(Docgen_Action_Docx_Data $docxAction) {
		$data = array(
			'DOCGEN_TEMPLATE_CLASS_ID' => $docxAction->getTemplateclassId(),
			'DOCGEN_TEMPLATE_ID'       => $docxAction->getTemplateId(),
		);

		$this->model->update($data, array('ACTION_ID = ?' => $docxAction->getActionId()));
	}

	public function delete(Docgen_Action_Docx_Data $docxAction) {
		$this->model->delete(array('ACTION_ID = ?' => $docxAction->getActionId()));
	}

	public function getAction($actionId) {
		$sel = $this->model->select()
			->from('DOCGEN_DOCX_ACTION', "*")
			->joinLeft('ACTION', 'ACTION.ACTION_ID = DOCGEN_DOCX_ACTION.ACTION_ID')
			->where('DOCGEN_DOCX_ACTION.ACTION_ID = ?', $actionId)
			->setIntegrityCheck(false);
		$row = $this->model->fetchAll($sel)->current();

		$result = new Docgen_Action_Docx_Data(
			$row->ACTION_ID,
			$row->AVAILABLE_ACTION_ID,
			$row->BUTTON_ID,
			$row->NAME,
			$row->DESCRIPTION,
			$row->SUCCESS_MESSAGE,
			$row->ERROR_MESSAGE,
			$row->EXECUTE_ALWAYS,
			$row->SORT,
			$row->DOCGEN_TEMPLATE_CLASS_ID,
			$row->DOCGEN_TEMPLATE_ID
		);

		return $result;
	}
}
