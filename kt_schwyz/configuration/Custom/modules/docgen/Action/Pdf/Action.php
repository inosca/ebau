<?php

class Docgen_Action_Pdf_Action extends Camac_Action_Action {

	public function handleAction($success = true) {
		$currentSuccess = $success;
		$action = $this->getResourceAction();

		if ($action->isAlwaysExecutable() || $success) {
			$result = false;

			$actionMapper = new Docgen_Action_Pdf_Mapper();
			$renderer = Docgen_TemplateController_Utils::getRenderer($action, $actionMapper);
			$template = Docgen_TemplateController_Utils::getTemplate($action, $actionMapper);

			$result = true;

			$this->setMessage($result);
			$currentSuccess = $success && $result;

			Docgen_TemplateController_Utils::outputDocument(
				$renderer,
				$template,
				Docgen_TemplateController_Utils::MIME_PDF
			);

		}

		return $success;
	}
}
