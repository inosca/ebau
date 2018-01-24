<?php

class Publication_PublishController extends Camac_Controller_Action {

	/**
	 * The workflow item that stands for the publication
	 */
	const _WORKFLOW_ITEM = 15;

	/**
	 * The workflow item for the objection deadline
	 *
	 * This will be autofilled 20 days after the publish date
	 */
	const _WORKFLOW_ITEM_OBJECTION_DEADLINE = 65;

	/**
	 * Instance ID
	 *
	 * @var           int $instanceID
	 */
	protected $instanceID;

	/**
	 * The current user role
	 *
	 * @var           int $userRole
	 */
	protected $userRole;

	/**
	 * The current publication entry of the active instance
	 *
	 * @var           Publication_Model_Data_PublicationEntry $publicationEntry
	 */
	protected $publicationEntry;

	public function __construct(
		Zend_Controller_Request_Abstract $request,
		Zend_Controller_Response_Abstract $response,
		array $invokeArgs = array()
	) {
		parent::__construct($request, $response, $invokeArgs);

		$this->session            = new Zend_Session_Namespace('module_publication');
		$this->instanceID         = intval($this->getRequest()->getParam('instance-id'));
		$this->instanceResourceID = intval($this->getRequest()->getParam('instance-resource-id'));
		$this->userRole           = Zend_Auth::getInstance()->getIdentity()->CURRENT_ROLE->getRoleId();
		$this->publicationEntryMapper = new Publication_Model_Mapper_PublicationEntry();

		$publicationEntry = $this->publicationEntryMapper->getEntriesByInstance($this->instanceID);
		if (isset($publicationEntry[0])) {
			$this->publicationEntry = $publicationEntry[0];
		}
		else {
			$this->publicationEntry = new Publication_Model_Data_PublicationEntry(
				null, $this->instanceID, null, null
			);
		}
	}

	public function listAction() {
		// If it is already published, there is no list needed, only preview
		if ($this->publicationEntry->isPublished) {
			$this->_helper->redirector('preview', 'publish', 'publication', array(
				'instance-resource-id' => $this->instanceResourceID,
				'instance-id'          => $this->instanceID
			));
		}

		$pubSettingMapper = new Publication_Model_Mapper_PublicationSetting();

		// Get needed answers and assign them
		$info = array();
		$info['organisation']      = $this->getAnswer($this->instanceID, 221, 1, 1);
		$info['person']            = $this->getAnswer($this->instanceID, 23, 1, 1);
		$info['place']['parcelNr'] = $this->getAnswer($this->instanceID, 91, 21, 1);
		$info['place']['lawNr']    = $this->getAnswer($this->instanceID, 92, 21, 1);
		$info['place']['street']   = $this->getAnswer($this->instanceID, 93, 21, 1);
		$info['intent']            = Custom_UriUtils::getMultianswers($this->instanceID, 97, 21, 1);
		$info['intent'][]          = $this->getAnswer($this->instanceID, 98, 21, 1);
		$info['duration']          = $pubSettingMapper->getEntryByKey('duration');

		if ($this->session->messages) {
			foreach ($this->session->messages as $message) {
				$this->_helper->FlashMessenger->addMessage($message, ERROR_MESSAGE);
			}
			$this->session->messages = NULL;
		}
		else {
			$this->view->messages = array();
		}

		$mapper = new Documents_Model_Mapper_Attachment();
		$this->view->showWarning = count($mapper->getAttachments(
			$this->instanceID,
			Custom_UriConstants::ATTACHMENT_SECTION_PUBLICATION_ID
		)) === 0;

		$this->view->info = $info;
		$this->view->publicationEntry = $this->publicationEntry;
		$this->view->userRole = $this->userRole;
		$this->view->instanceID = $this->instanceID;
	}

	public function saveAction() {
		if ($this->getRequest()->getParam('preview') !== null) {
			if ($this->publicationEntry->publicationEntryID === null) {
				$this->session->messages = array($this->view->translate('Please first set a date and note!'));
				$this->_helper->redirector('list', 'publish', 'publication', array(
					'instance-resource-id' => $this->instanceResourceID,
					'instance-id'          => $this->instanceID
				));
				return;
			}
			else {
				$this->_helper->redirector('preview', 'publish', 'publication', array(
					'instance-resource-id' => $this->instanceResourceID,
					'instance-id'          => $this->instanceID
				));
				return;
			}
		}

		$this->publicationEntry->note            = $this->getRequest()->getParam('note');
		$this->publicationEntry->publicationDate = DateTime::createFromFormat(
			Zend_Registry::get('config')->date->application->phpFormat,
			$this->getRequest()->getParam('publishDate')
		);

		if ($this->publicationEntry->publicationDate === false) {
			$this->session->messages = array($this->view->translate('Please set a date!'));
			$this->_helper->redirector('list', 'publish', 'publication', array(
				'instance-resource-id' => $this->instanceResourceID,
				'instance-id'          => $this->instanceID
			));
			return;
		}

		$this->publicationEntryMapper->save($this->publicationEntry);

		$this->_helper->redirector('list', 'publish', 'publication', array(
			'instance-resource-id' => $this->instanceResourceID,
			'instance-id'          => $this->instanceID
		));
	}

	public function previewAction() {
		$pubSettingMapper = new Publication_Model_Mapper_PublicationSetting();

		// Get current account location
		$group = Zend_Auth::getInstance()->getIdentity()->CURRENT_GROUP;

		// Get intent
		$intent   = Custom_UriUtils::getMultianswers($this->instanceID, 97, 21, 1);
		$intent[] = $this->getAnswer($this->instanceID, 98, 21, 1);

		$customTags = array(
			'authority'   => $this->getAuthority(),
			'date'        => date('d.m.Y'),
			'publishDate' => $this->publicationEntry->publicationDate->format('d.m.Y'),
			'community'   => $this->getCommunity(),
			'note'        => $this->getNote((int)$this->publicationEntry->note),
			'intent'      => implode(', ', $intent),
			'location'    => $group->getCity(),
			'zip'         => $group->getZip()
		);

		$interpreter = Zend_Controller_Action_HelperBroker::getStaticHelper('Interpreter');
		$text = $interpreter->direct($pubSettingMapper->getEntryByKey('text')->value);

		foreach ($customTags as $tag => $value) {
			$text = str_replace(sprintf('[@%s]', $tag), $value, $text);
		}

		$this->view->publicationText  = $text;
		$this->view->publicationEntry = $this->publicationEntry;
	}

	/**
	 * The Action when the print button was pressed on the preview
	 */
	protected function printButtonPressed() {
		$instanceResourceId = (int) $this->getRequest()->getParam('instance-resource-id');
		$instanceResource   = $this->_helper->InstanceResourcePublication->getResource($instanceResourceId);

		if ($this->getRequest()->isPost()) {
			$buttons = $instanceResource->getButtons();
			$this->handleActions($buttons);
		}
	}

	/**
	 * The action when the cancel butto was clicked on the preview
	 */
	protected function cancelButtonPressed() {
		$this->_helper->redirector('list', 'publish', 'publication', array(
			'instance-resource-id' => $this->instanceResourceID,
			'instance-id'          => $this->instanceID
		));
	}

	/**
	 * Save the date to the workflow
	 */
	protected function setWorkflowDate() {
		$workflowEntryMapper = new Workflow_Model_Mapper_WorkflowEntry();
		$workflowEntryMapper->makeEntry(
			$this->instanceID,
			self::_WORKFLOW_ITEM,
			Workflow_Action_Workflow_Data::MULTI_VALUE_IGNORE,
			$this->publicationEntry->publicationDate
		);

		// Set the objection deadline 20 days after the publication date
		$deadlineDate = new DateTime();
		$deadlineDate->setTimestamp(
			strtotime('+20 days', $this->publicationEntry->publicationDate->getTimestamp())
		);

		$workflowEntryMapper->makeEntry(
			$this->instanceID,
			self::_WORKFLOW_ITEM_OBJECTION_DEADLINE,
			Workflow_Action_Workflow_Data::MULTI_VALUE_IGNORE,
			$deadlineDate
		);
	}

	/**
	 * Send a publication e-mail
	 *
	 * Send an e-mail containing the publication text to the address that is
	 * configured in the admin
	 */
	protected function sendPublicationEmail() {
		$pubSettingMapper = new Publication_Model_Mapper_PublicationSetting();
		$userMapper = new Admin_Model_Mapper_Account_User();

		$user = $userMapper->getUser(Zend_Auth::getInstance()->getIdentity()->USER->USER_ID);

		$mail = new Zend_Mail('UTF-8');
		$mail->setSubject('Publikation vom ' . $this->publicationEntry->publicationDate->format('d.m.Y'));
		$mail->setBodyText($this->publicationEntry->text);
		$mail->setFrom($pubSettingMapper->getEntryByKey('fromEmail')->value);
		$mail->addTo($pubSettingMapper->getEntryByKey('toEmail')->value);

		if (strlen($user->getEmail()) > 0) {
			$mail->addBcc($user->getEmail());
		}
		$mail->send();
	}

	/**
	 * Save the entered text as publication entry
	 */
	protected function savePublicationEntry() {
		$this->publicationEntry->text        = $this->getRequest()->getParam('publicationText');
		$this->publicationEntry->isPublished = 1;

		$this->publicationEntryMapper->save($this->publicationEntry);
	}

	/**
	 * The action when the publish button was pressed
	 *
	 * Save the publication entry, set a workflow date, then send an email
	 */
	protected function publishButtonPressed() {
		$this->savePublicationEntry();

		// Set workflow date
		$this->setWorkflowDate();

		// Send email
		$this->sendPublicationEmail();

		$this->_helper->redirector('preview', 'publish', 'publication', array(
			'instance-resource-id' => $this->instanceResourceID,
			'instance-id'          => $this->instanceID
		));
	}

	/**
	 * The action on the publish page
	 *
	 * Depending on the button that was clicked, decide the action
	 * @TODO by sh: Maybe it would have been easier to really implement
	 * different actions? this looks hacky man
	 */
	public function publishAction() {
		// Cancel: Return to publication overview if the preview is cancelled
		if ($this->getRequest()->getParam('cancel') !== null) {
			$this->cancelButtonPressed();
		}

		// Print: Generate and offer document when print was pressed
		if ($this->getRequest()->getParam('button_293') !== null) {
			$this->printButtonPressed();
			return;
		}

		// it looks like the publish button was presed!
		$this->publishButtonPressed();
	}

	private function getAnswer($instanceID, $questionID, $chapterID, $itemID) {
		$answerGateway = new Application_Model_Mapper_AnswerGateway();
		$answer = $answerGateway->getAnswer($instanceID, $questionID, $chapterID, $itemID);

		return $answer === null ? null : $answer->getAnswer();
	}

	private function getCommunity() {
		$instLocModel = new Camac_Model_DbTable_InstanceLocation();

		$row = $instLocModel->fetchRow(
			$instLocModel->select()
			->setIntegrityCheck(false)
			->from('INSTANCE_LOCATION')
			->joinLeft('LOCATION', 'LOCATION.LOCATION_ID = INSTANCE_LOCATION.LOCATION_ID', 'NAME')
			->where('INSTANCE_LOCATION.INSTANCE_ID = ?', $this->instanceID));

		return $row['NAME'];
	}

	private function getAuthority() {
		$config = Zend_Registry::get('config');
		$isOracle = in_array($config->resources->db->adapter, array('Oracle', 'Pdo_Oci'));

		$mapper = new Camac_Model_DbTable_Answer();
		$select = $mapper->select()
			->from("ANSWER", "")
			->where("ANSWER.CHAPTER_ID = ?", Custom_UriConstants::AUTHORITY_CHAPTER_ID)
			->where("ANSWER.QUESTION_ID = ?", Custom_UriConstants::AUTHORITY_QUESTION_ID)
			->where("ANSWER.ITEM = ?", Custom_UriConstants::AUTHORITY_ITEM_ID)
			->where("ANSWER.INSTANCE_ID = ?", $this->instanceID)
			->setIntegrityCheck(false);
		if ($isOracle) {
			$select->join("AUTHORITY", 'AUTHORITY_ID = TO_NUMBER("ANSWER"."ANSWER")', "NAME");
		} else {
			$select->join("AUTHORITY", 'AUTHORITY_ID = cast("ANSWER"."ANSWER" as int)', "NAME");
		}
		return $mapper->fetchAll($select)->current()->NAME;
	}

	private function getNote($noteID) {
		if ($noteID === 1) {
			return 'Profilierung auf Verlangen';
		}
		elseif ($noteID === 2) {
			return 'Profiliert';
		}
		elseif ($noteID === 3) {
			return 'Verpflockt';
		}
		else {
			return '';
		}
	}
}
