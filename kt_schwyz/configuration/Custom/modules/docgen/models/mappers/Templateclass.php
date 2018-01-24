<?php

class Docgen_Model_Mapper_Templateclass {

	const TYPE_DOCX = 1;
	const TYPE_PDF  = 2;

	protected $model;

	public function __construct() {
		$this->model = new Docgen_Model_DbTable_Templateclass();
	}

	public function insert(Docgen_Model_Data_Templateclass $templateClass) {
		$data = array(
			'NAME' => $templateClass->name,
			'PATH' => $templateClass->path,
			'TYPE' => $templateClass->type
		);

		return $this->model->insert($data);
	}

	public function update(Docgen_Model_Data_Templateclass $templateClass) {
		$data = array(
			'NAME' => $templateClass->name,
			'PATH' => $templateClass->path
		);

		$this->model->update(
			$data,
			array('DOCGEN_TEMPLATE_CLASS_ID = ?' => $templateClass->docgenTemplateclassId)
		);
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->model->delete(array('DOCGEN_TEMPLATE_CLASS_ID = ?' => $id));
	}

	public function getTemplateClasses($typeId = null) {
		if ($typeId && ($typeId === self::TYPE_DOCX || $typeId === self::TYPE_PDF)) {
			$rows = $this->model->fetchAll(
				sprintf('type = %d', $typeId)
			);
		}
		else {
			$rows = $this->model->fetchAll();
		}

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Docgen_Model_Data_Templateclass(
				$row->DOCGEN_TEMPLATE_CLASS_ID,
				$row->NAME,
				self::getResourcePath($row->PATH),
				$row->TYPE
			);
		}

		return $results;
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function getTemplateClass($id) {
		$row = $this->model->find($id)->current();

		if (!$row) {
			throw new Exception(sprintf("Document class with id %s not found", $id));
		}
		$templateClass = new Docgen_Model_Data_Templateclass(
			$row->DOCGEN_TEMPLATE_CLASS_ID,
			$row->NAME,
			self::getResourcePath($row->PATH),
			$row->TYPE
		);

		return $templateClass;
	}

	public static function getResourcePath($filename) {
		return realpath(Zend_Registry::get('config')->docgen->templateClass . $filename);
	}

}
