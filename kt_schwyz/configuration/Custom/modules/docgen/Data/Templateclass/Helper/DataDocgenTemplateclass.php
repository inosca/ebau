<?php

class Docgen_Data_Templateclass_Helper_DataDocgenTemplateclass extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	protected $mapper;

	/**
	 * Upload errors
	 *
	 * @var           string $uploadErrors
	 */
	protected $uploadErrors;


	public function __construct() {
		$this->mapper = new Docgen_Model_Mapper_Templateclass();
		$this->config = new Zend_Config_Ini(
			CONFIGURATION_PATH . '/Custom/modules/docgen/configs/module.ini',
			APPLICATION_ENV,
			array('allowModifications' => false)
		);
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function add($form, $id, $mode) {
		$upload     = new Zend_File_Transfer_Adapter_Http();
		$uploadPath = $this->config->templateclassUploadPath;

		$upload->setDestination($uploadPath);

		if ($upload->receive('file')) {
			$templateClass = new Docgen_Model_Data_Templateclass(
				null,
				$form->getValue('name'),
				$upload->getFileName('file', false),
				$form->getValue('type')
			);

			$this->checkFile($upload->getFileName('file'));

			$this->mapper->insert($templateClass);
		}
		else {
			throw new Exception($upload->getMessages());
		}
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function update($id, $form) {
		$upload     = new Zend_File_Transfer_Adapter_Http();
		$uploadPath = $this->config->templateclassUploadPath;

		$currentClass = $this->mapper->getTemplateClass($id);
		$temporaryPath = sprintf("%s.temp_moved", $currentClass->path);
		rename($currentClass->path, $temporaryPath);

		$upload->setDestination($uploadPath);
		$fileInfo = $upload->getFileInfo();


		if ($upload->receive('file')) {
			$this->checkFile($upload->getFileName('file'));

			$templateClass = new Docgen_Model_Data_Templateclass(
				$id,
				$form->getValue('name'),
				$upload->getFileName('file', false),
				$currentClass->type
			);

			$this->mapper->update($templateClass);
			unlink($temporaryPath);
		}
		else {
			// if something goes wrong, put it back
			rename($temporaryPath, $currentClass->path);
			throw new Exception($upload->getMessages());
		}
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function delete($id) {
		$templateClass = $this->mapper->getTemplateClass($id);
		$this->mapper->delete($id);
		unlink($templateClass);
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function move($id, $targetId, $mode) {
	}

	public function getRows() {
		return $this->mapper->getTemplateclasses();
	}

	/**
	 * @SuppressWarnings(short)
	 * @SuppressWarnings(unused)
	 */
	public function getData($id) {
		return $this->mapper->getTemplateClass($id);
	}

	public function getForm() {
		if ($this->getRequest()->getParam('action') == 'edit')  {
			return new Docgen_Data_Templateclass_Form(array(), true);
		}

		return new Docgen_Data_Templateclass_Form(array(), false);
	}

	/**
	 * Check the file for correct usage
	 */
	protected function checkFile($filePath) {
		set_error_handler(array($this, 'errorHandler'), E_ALL);
		$contents = file_get_contents($filePath);
		$classes = $this->get_php_classes($contents);
		switch (count($classes)) {
			case 0:
				throw new Exception("No classes found in " . $filePath);
				break;
			case 1:
				$className = $classes[0];
				break;
			default:
				throw new Exception("Too many classes found in " . $filePath . ". Don't know which to take");
		}
		exec(sprintf('php -l %s 2>&1', $filePath), $output, $retVar);
		if ($retVar) {
			$msg = "Could not check the PHP file:\n" . join('<br />', $output);
			Zend_Controller_Action_HelperBroker::getStaticHelper('FlashMessenger')->addMessage($msg, ERROR_MESSAGE);
			return;
		}
		require_once $filePath;

		if (!is_subclass_of($className, 'Docgen_TemplateController_TemplateControllerAbstract')) {
			throw new Exception('The class does not extend TemplateControllerAbstract');
		}

	}

	public function errorHandler($errno, $errstr, $errfile, $errline, $errcontext) {
		$this->uploadErrors =
			sprintf("%i %s %s %s %s", $errno, $errfile, $errline, $errstr, $errcontext);

		throw new ErrorException($this->uploadErrors);
	}

	protected function get_php_classes($php_code) {
		$classes = array();
		$tokens = token_get_all($php_code);
		$count = count($tokens);
		for ($i = 2; $i < $count; $i++) {
			if (   $tokens[$i - 2][0] == T_CLASS
				&& $tokens[$i - 1][0] == T_WHITESPACE
				&& $tokens[$i][0] == T_STRING) {

				$class_name = $tokens[$i][1];
				$classes[] = $class_name;
			}
		}
		return $classes;
	}
}
