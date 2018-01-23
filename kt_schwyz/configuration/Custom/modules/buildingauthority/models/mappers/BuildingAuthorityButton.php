<?php

class Buildingauthority_Model_Mapper_BuildingAuthorityButton {

	const BUTTON_ID_BAUBEWILLIGUNG_ERSTELLEN = 2;
	const BUTTON_ID_BAUBEWILLIGUNG_ERTEILT   = 3;
	const BUTTON_ID_BAU_BEENDET_GEOMETER     = 4;
	const BUTTON_ID_BAU_BEENDET_LIEGENSCHAFT = 5;
	const BUTTON_ID_BAU_BEENDET_ABWASSER     = 6;
	const BUTTON_ID_GRUNDBUCHANMELDUNG       = 7;
	const BUTTON_ID_ABNAHME_SCHNURGERUEST    = 8;
	const BUTTON_ID_INFOBRIEF_GESUCHSTELLER  = 9;
	const BUTTON_ID_INFOBRIEF_ALLGEMEIN      = 10;
	const BUTTON_ID_BAUBEWILLIGUNG_ERTEILT_GEBAEUDE = 11;

	protected $model;

	public function __construct() {
		$this->model = new Buildingauthority_Model_DbTable_BuildingAuthorityButton();
	}

	public function save(Buildingauthority_Model_Data_BuildingAuthorityButton $baButton) {
		$data = array(
			'LABEL' => $baButton->label
		);

		return $this->model->insert($data);
	}

	public function update(Buildingauthority_Model_Data_Buildingauthoritybutton $baButton) {
		$data = array('LABEL' => $baButton->label);
		$this->model->update($data, array('BUILDING_AUTHORITY_BUTTON_ID = ?' => $baButton->baButtonId));
	}

	public function getButton($baButtonId) {
		$result = null;
		$row    = $this->model->find($baButtonId)->current();

		if ($row) {
			$result = new Buildingauthority_Model_Data_BuildingAuthorityButton(
				$baButtonId,
				$row->LABEL
			);
		}

		return $result;
	}

	public function getButtons() {
		$select = $this->model->select()->order(array('LABEL ASC'));
		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$id = $row->BUILDING_AUTHORITY_BUTTON_ID;
			$results[$id] = new Buildingauthority_Model_Data_BuildingAuthorityButton(
				$id,
				$row->LABEL
			);
		}

		return $results;
	}

	public function delete($baButtonId) {
		$this->model->delete(array(
			'BUILDING_AUTHORITY_BUTTON_ID = ?' => $baButtonId
		));
	}

	protected function handleEmailAction($buttonId, $instanceId) {
		$interpreter = Zend_Controller_Action_HelperBroker::getStaticHelper('Interpreter');
		$userMapper = new Admin_Model_Mapper_Account_User();
		$baEmailMapper = new Buildingauthority_Model_Mapper_BuildingAuthorityEmail();
		$baButtonStateMapper = new Buildingauthority_Model_Mapper_BuildingAuthorityButtonState();
		$emails = $baEmailMapper->getEmailsFromButton($buttonId);

		$user = $userMapper->getUser(Zend_Auth::getInstance()->getIdentity()->USER->USER_ID);

		if (count($emails) == 0) {
			return true;
		}

		try {
			foreach($emails as $emailData) {
				$recipients = $this->getRecipients($emailData->receiverQuery, $instanceId);

				// If we don't have any recipients skip this email
				if (count($recipients) === 0) {
					continue;
				}

				$mail = new Zend_Mail('UTF-8');
				foreach ($recipients as $recipient) {
					$mail->addTo($recipient);
				}

				$mail->setBodyText(
					$interpreter->direct($emailData->emailText, false)
				);
				$mail->setFrom($emailData->fromEmail, $emailData->fromName);
				if ($user->getEmail()) {
					$mail->addBcc($user->getEmail());
				}
				$mail->setSubject($interpreter->direct($emailData->emailSubject, false));
				$mail->send();
			}
		}
		catch(Exception $e) {
			return false;
		}

		// Update button state to isClicked
		$baButtonStateMapper->setIsClicked($buttonId, $instanceId);

		$this->setWorkflowDate($buttonId, $instanceId);

		return true;
	}

	protected function getRecipients($receiverQuery, $instanceId) {
		if (strpos($receiverQuery, '[') !== 0) {
			return array($receiverQuery);
		}

		if ($receiverQuery === '[fachstellen]') {
			$serviceEmails = array();
			$services = Custom_UriUtils::getActiveServices($instanceId);

			foreach ($services as $service) {
				$serviceEmails[] = $service->getEmail();
			}

			return $serviceEmails;
		}

		if ($receiverQuery === '[gesuchsteller]') {
			$gesuchsteller = Custom_UriUtils::getGesuchstellerEmail($instanceId);
			return $gesuchsteller ? array($gesuchsteller) : array();
		}

		return array();
	}

	public function handleDocAction($buttonId, $instanceId) {
		$baDocMapper = new Buildingauthority_Model_Mapper_BuildingAuthorityDoc();
		$typeDocx = Docgen_Model_Mapper_Templateclass::TYPE_DOCX;
		$docs = $baDocMapper->getDocsFromButton($buttonId);

		// Only one download can be triggered, so take the first doc
		$doc = array_shift($docs);

		if (!$doc) {
			return true;
		}

		try {
			$template = Docgen_TemplateController_Utils::getTemplateByID($doc->templateId);
			$renderer = Docgen_TemplateController_Utils::getRendererByID($doc->templateClassId);

			Docgen_TemplateController_Utils::outputDocument(
				$renderer,
				$template,
				(int)$template->type === $typeDocx ? Docgen_TemplateController_Utils::MIME_DOCX : Docgen_TemplateController_Utils::MIME_PDF
			);

			$this->setWorkflowDate($buttonId, $instanceId);
			exit();
		}
		catch(Exception $e) {
			return false;
		}
	}

	protected function setWorkflowDate($buttonId, $instanceId) {
		// WorkflowItem ids (wi = workflowItem)
		$wiVersandBaubewilligung  = 72;
		$wiMeldungBaubewilligung  = 66;
		$wiBauBeendetGeometer     = 68;
		$wiBauBeendetLiegenschaft = 69;
		$wiBauBeendetAbwasser     = 57;
		$wiGrundbuchanmeldung     = 70;
		$wiAbnahmeSchnurgeruest   = 56;

		switch((int)$buttonId) {
			case self::BUTTON_ID_BAUBEWILLIGUNG_ERSTELLEN:
				$this->makeWorkflowEntry($instanceId, $wiVersandBaubewilligung);
				break;
			case self::BUTTON_ID_BAUBEWILLIGUNG_ERTEILT:
				$this->makeWorkflowEntry($instanceId, $wiMeldungBaubewilligung);
				break;
			case self::BUTTON_ID_BAU_BEENDET_GEOMETER:
				$this->makeWorkflowEntry($instanceId, $wiBauBeendetGeometer);
				break;
			case self::BUTTON_ID_BAU_BEENDET_LIEGENSCHAFT:
				$this->makeWorkflowEntry($instanceId, $wiBauBeendetLiegenschaft);
				break;
			case self::BUTTON_ID_BAU_BEENDET_ABWASSER:
				$this->makeWorkflowEntry($instanceId, $wiBauBeendetAbwasser);
				break;
			case self::BUTTON_ID_GRUNDBUCHANMELDUNG:
				$this->makeWorkflowEntry($instanceId, $wiGrundbuchanmeldung);
				break;
			case self::BUTTON_ID_ABNAHME_SCHNURGERUEST:
				$this->makeWorkflowEntry(
					$instanceId,
					$wiAbnahmeSchnurgeruest,
					Workflow_Action_Workflow_Data::MULTI_VALUE_APPEND
				);
				break;
		}
	}

	protected function makeWorkflowEntry(
		$instanceId,
		$itemId,
		$multiValue = Workflow_Action_Workflow_Data::MULTI_VALUE_REPLACE
	) {
		$workflowEntryMapper  = new Workflow_Model_Mapper_WorkflowEntry();
		$workflowEntryMapper->makeEntry(
			$instanceId,
			$itemId,
			$multiValue
		);
	}

	public function handleAction($buttonId, $instanceId) {
		$messages = array(
			'success' => array(),
			'error'   => array()
		);

		// Handle email actions for this button
		if ($this->handleEmailAction($buttonId, $instanceId)) {
			$messages['success'][] = 'Email erfolgreich versandt';
		}
		else {
			$messages['error'][] = 'Email konnten nicht versandt werden';
		}

		// Handle doc actions for this button
		if (!$this->handleDocAction($buttonId, $instanceId)) {
			$messages['error'][] = 'Fehler beim Generieren des Dokuments';
		}

		return $messages;
	}
}
