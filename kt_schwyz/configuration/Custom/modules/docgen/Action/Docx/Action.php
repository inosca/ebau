<?php

class Docgen_Action_Docx_Action extends Camac_Action_Action {

	/**
	 * @SuppressWarnings(unused)
	 */
	public function handleAction($success = true) {

		//error_reporting(0);

		$currentSuccess = $success;
		$action = $this->getResourceAction();


		if ($action->isAlwaysExecutable() || $success) {
			$result = false;

			$actionMapper = new Docgen_Action_Docx_Mapper();
			$renderer = Docgen_TemplateController_Utils::getRenderer($action, $actionMapper);
			$template = Docgen_TemplateController_Utils::getTemplate($action, $actionMapper);

			$result = true;

			$this->setMessage($result);
			$currentSuccess = $success && $result;

			Docgen_TemplateController_Utils::outputDocument(
				$renderer,
				$template,
				Docgen_TemplateController_Utils::MIME_DOCX
			);
		}
	}


}
