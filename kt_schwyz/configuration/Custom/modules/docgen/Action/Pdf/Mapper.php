<?php

class Docgen_Action_Pdf_Mapper {

	protected $model;

	public function __construct() {
		$this->model = new Docgen_Action_Pdf_DbTable();
	}

	public function save(Docgen_Action_Pdf_Data $pdfAction) {
		$data = array(
			'DOCGEN_TEMPLATE_CLASS_ID' => $pdfAction->getTemplateclassId(),
			'DOCGEN_TEMPLATE_ID'       => $pdfAction->getTemplateId(),
			'ACTION_ID'                => $pdfAction->getActionId()
		);

		$this->model->insert($data);
	}

	public function update(Docgen_Action_Pdf_Data $pdfAction) {
		$data = array(
			'DOCGEN_TEMPLATE_CLASS_ID' => $pdfAction->getTemplateclassId(),
			'DOCGEN_TEMPLATE_ID'       => $pdfAction->getTemplateId()
		);

		$this->model->update($data, array('ACTION_ID = ?' => $pdfAction->getActionId()));
	}

	public function delete(Docgen_Action_Pdf_Data $pdfAction) {
		$this->model->delete(array('ACTION_ID = ?' => $pdfAction->getActionId()));
	}

	public function getAction($actionId) {
		$sel = $this->model->select()
			->from('DOCGEN_PDF_ACTION', "*")
			->joinLeft('ACTION', 'ACTION.ACTION_ID = DOCGEN_PDF_ACTION.ACTION_ID', '*')
			->where('DOCGEN_PDF_ACTION.ACTION_ID = ?', $actionId)
			->setIntegrityCheck(false);


		$row = $this->model->fetchAll($sel)->current();

		$result = new Docgen_Action_Pdf_Data(
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
