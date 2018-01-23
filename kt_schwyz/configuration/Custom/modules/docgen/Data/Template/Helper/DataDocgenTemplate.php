<?php
class Docgen_Data_Template_Helper_DataDocgenTemplate extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Docgen_Model_Mapper_Template();
		$this->config = new Zend_Config_Ini(
			CONFIGURATION_PATH . '/Custom/modules/docgen/configs/module.ini',
			APPLICATION_ENV,
			array('allowModifications' => false)
		);
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function add($form, $id, $mode) {
		$upload = new Zend_File_Transfer_Adapter_Http();
		$uploadPath = $this->config->templateUploadPath;

		$upload->setDestination($uploadPath);
		$fileInfo = $upload->getFileInfo();

		if ($upload->receive('file')) {

			$fileInfo = pathinfo($upload->getFileName('file'));
			$type = strtolower($fileInfo['extension']) == 'docx'
				? Docgen_Model_Mapper_Template::TYPE_DOCX
				: Docgen_Model_Mapper_Template::TYPE_PDF;

			$template = new Docgen_Model_Data_Template(
				null,
				$form->getValue('name'),
				$upload->getFileName('file', false),
				$type
			);

			$this->mapper->insert($template);
		}
		else {
			throw new Exception($upload->getMessages());
		}
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function update($id, $form, $previousLanguage = null) {
		$upload = new Zend_File_Transfer_Adapter_Http();
		$uploadPath = $this->config->templateUploadPath;

		$currentTemplate = $this->mapper->getTemplate($id);
		$temporaryPath = sprintf("%s.temp_moved", $currentClass->path);
		rename($currentTemplate->path, $temporaryPath);

		$upload->setDestination($uploadPath);

		if ($upload->receive('file')) {
			$template = new Docgen_Model_Data_Template(
				$id,
				$form->getValue('name'),
				$upload->getFileName('file', false),
				$currentTemplate->type
			);

			$this->mapper->update($template);

			unlink($temporaryPath);
		}
		else {
			rename($temporaryPath, $currentTemplate->path);
			throw new Exception($upload->getMessages());
		}
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function delete($id) {
		$template = $this->mapper->getTemplate($id);
		$this->mapper->delete($id);
		unlink($template->path);
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function move($id, $targetId, $mode) {
	}

	public function getRows() {
		return $this->mapper->getTemplates();
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function getData($id, $language = null) {
		return $this->mapper->getTemplate($id);
	}

	public function getForm() {
		return new Docgen_Data_Template_Form(array(), true);
	}

}
