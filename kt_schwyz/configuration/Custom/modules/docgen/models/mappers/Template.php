<?php


class Docgen_Model_Mapper_Template {

	const TYPE_DOCX = 1;
	const TYPE_PDF = 2;

	protected $model;

	public function __construct() {
		$this->model = new Docgen_Model_DbTable_Template();
	}

	public function insert(Docgen_Model_Data_Template $template) {
		$data = array(
			'NAME'               => $template->name,
			'PATH'               => $template->path,
			'TYPE'               => $template->type
		);

		return $this->model->insert($data);
	}

	public function update(Docgen_Model_Data_Template $template) {
		$data = array(
			'NAME'   => $template->name,
			'PATH'   => $template->path
		);

		$this->model->update(
			$data,
			array('DOCGEN_TEMPLATE_ID = ?' => $template->docgenTemplateId)
		);
	}

	public function getTemplates($typeId = null) {
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
			$results[] = new Docgen_Model_Data_Template(
				$row->DOCGEN_TEMPLATE_ID,
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
	public function getTemplate($id) {
		$row = $this->model->find($id)->current();

		if (!$row) {
			throw new Exception(sprintf("Template with id %s not found", $id));
		}

		return new Docgen_Model_Data_Template(
			$row->DOCGEN_TEMPLATE_ID,
			$row->NAME,
			self::getResourcePath($row->PATH),
			$row->TYPE
		);
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->model->delete(array('DOCGEN_TEMPLATE_ID = ?' => $id));
	}

	public static function getResourcePath($filename) {
		return realpath(Zend_Registry::get('config')->docgen->template . $filename);
	}
}
