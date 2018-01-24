<?php

class Docgen_TemplateController_Utils {

	const MIME_PDF = 'application/pdf';
	const MIME_DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';

	public static function getClassName(Docgen_Model_Data_TemplateClass $templateClass) {
		$contents = file_get_contents($templateClass->path);

		$classes =  self::get_php_classes($contents);
		return $classes[0];
	}

	public static function get_php_classes($php_code) {
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

	public static function outputDocument($renderer, $template, $mimeType) {
		Zend_Layout::getMvcInstance()->disableLayout();
		Zend_Controller_Action_HelperBroker::getStaticHelper('viewRenderer')->setNoRender();

		if ($mimeType == self::MIME_PDF) {
			header('Content-Disposition: attachment; filename="'.$template->name.'.pdf"');
			header("Content-Type: " . self::MIME_PDF);
		}
		else {
			header('Content-Disposition: attachment; filename="'.$template->name.'.docx"');
			header("Content-Type: " . self::MIME_DOCX);
		}

		echo $renderer->render($template->path);
	}

	public static function getRenderer($action, $actionMapper) {
		$actionAction = $actionMapper->getAction($action->getActionId());
		$templateClassId = $actionAction->getTemplateClassId();

		return self::getRendererByID($templateClassId);
	}

	public static function getRendererByID($templateClassId) {
		$templateClassMapper = new Docgen_Model_Mapper_Templateclass();
		$templateClass = $templateClassMapper->getTemplateClass($templateClassId);
		$className = Docgen_TemplateController_Utils::getClassName($templateClass);
		require_once($templateClass->path);

		return new $className();
	}

	public static function getTemplate($action, $actionMapper) {
		$actionAction = $actionMapper->getAction($action->getActionId());

		return self::getTemplateByID($actionAction->getTemplateId());
	}

	public static function getTemplateByID($templateId) {
		$templateMapper = new Docgen_Model_Mapper_Template();
		$template = $templateMapper->getTemplate($templateId);

		return $template;
	}

	public static function getRenderedDocument($rendererId, $templateId) {
		return self::getRendererByID($rendererId)->render(
			self::getTemplateByID($templateId)->path
		);
	}
}
