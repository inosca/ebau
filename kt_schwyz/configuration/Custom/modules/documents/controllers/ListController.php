<?php
require_once APPLICATION_PATH . '/../library/fpdf/fpdf.php';
require_once APPLICATION_PATH . '/../library/fpdi/fpdf_tpl.php';
require_once APPLICATION_PATH . '/../library/fpdi/fpdi.php';

function getDuplicates($attachments, $attachment) {
	return array_filter($attachments, function($candidate) use ($attachment) {
		return $candidate->name === $attachment->name;
	});
}


/**
 * @SuppressWarnings(methods)
 * @SuppressWarnings(coupling)
 */
class Documents_ListController extends Camac_Controller_Action {

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
	 * Privileges
	 *
	 * @var           int $_privileges
	 */
	protected $_privileges;

	/**
	 * The upload form
	 *
	 * @var           Documents_Data_UploadForm $form
	 */
	protected $form;

	/**
	 * The document lib which holds the main functions
	 *
	 * @var           Documents_Lib_DocumentLib $documentLib
	 */
	protected $documentLib;

	/**
	 * Class constructor
	 *
	 * @param Zend_Controller_Request_Abstract $request The request
	 * @param Zend_Controller_Response_Abstract $response The response
	 * @param array $invokeArgs List of invoked arguments
	 * @return void
	 */
	public function __construct(
			Zend_Controller_Request_Abstract $request,
			Zend_Controller_Response_Abstract $response,
			array $invokeArgs = array()
	) {
		parent::__construct($request, $response, $invokeArgs);

		$this->instanceID         = intval($this->getRequest()->getParam('instance-id'));
		$this->instanceResourceID = intval($this->getRequest()->getParam('instance-resource-id'));

		$this->attachmentMapper = new Documents_Model_Mapper_Attachment();
		$this->session          = new Zend_Session_Namespace('module_documents');
		$this->documentLib      = new Documents_Lib_DocumentLib();

		$this->lisagServiceId = Zend_Registry::get('config')->attachment->lisag_service_id;
		$this->maxFileSize    = Zend_Registry::get('config')->attachment->upload_max_filesize;
	}

	/**
	 * List the attachments
	 */
	public function listAction() {
		if ($this->session->messages) {
			foreach ($this->session->messages as $message) {
				$this->_helper->FlashMessenger->addMessage($message, ERROR_MESSAGE);
			}
			$this->session->messages = NULL;
		}

		$attachmentSectionMapper = new Documents_Model_Mapper_AttachmentSection();

		$this->form = new Documents_Data_UploadForm($this->instanceID);
		$this->form->initForm();

		if ($this->getRequest()->isPost()) {
			if ($this->form->isValid($_POST)) {
				$userID  = $this->uploadUserID();
				$service = $this->getCurrentService();

				$attachmentSection = $this->form->getValue('upload_target');

				if (!$this->isAllowedToUpload($attachmentSection)) {
					$this->_helper->FlashMessenger->addMessage("Sie dürfen hier nicht hochladen", ERROR_MESSAGE);
					return;
				}

				try {
					$allMessages = array();
					foreach ($this->documentLib->getUploadedFiles() as $fieldname => $fileinfo) {
						// $fieldname is formatted like file_0_ - we're interested in the number.
						preg_match('/file_(\d)_/', $fieldname, $fieldnameMatches);
						$index = $fieldnameMatches[1];
						$params = $this->getRequest()->getParams();
						$isConfidential = isset($params['isConfidential'][$index]) && intval($params['isConfidential'][$index]);

						$messages = $this->documentLib->uploadFile(
							$fieldname,
							$this->instanceID,
							$userID,
							$attachmentSection,
							$this->getCurrentService(),
							null, // target filename
							false, // digital signature,
							false, // is parcel picture
							$isConfidential
						);

						if (is_array($messages)) {
							$allMessages = array_merge($allMessages, $messages);
						}
					}

					$this->_helper->MessageToFlash->addErrorMessagesToFlash($allMessages);
				}
				catch(Exception $e) {
					$this->_helper->MessageToFlash->addErrorMessagesToFlash($e->getMessage());
				}
			}
			else {
				$this->_helper->MessageToFlash->addErrorMessagesToFlash($this->form->getMessages());
			}
		}

		$sections = $attachmentSectionMapper->getEntries();

		$attachments = array();
		/**
		 * In order to assign versions to multiple occurences of the same filename, we map
		 * each $attachment to array(
		 *   "attachment" => (attachment),
		 *   "version" => (number)
		 * )
		 */
		foreach ($sections as $section) {
			$sectionAttachments = array();
			$sectionContent = $this->attachmentMapper->getAttachments(
				$this->instanceID,
				$section->attachmentSectionID
			);
			foreach ($sectionContent as $attachment) {
				if (array_key_exists($attachment->attachmentID, $sectionAttachments)) {
					continue;
				}
				$duplicates = getDuplicates($sectionContent, $attachment);
				if (count($duplicates) === 1) {
					$sectionAttachments[array_values($duplicates)[0]->attachmentID] = array(
						"attachment" => $attachment,
						"version" => null
					);
					continue;
				}
				foreach (array_values($duplicates) as $index => $duplicate) {
					$sectionAttachments[$duplicate->attachmentID] = array(
						"attachment" => $duplicate,
						"version" => $index + 1
					);
				}
			}
			$attachments[$section->attachmentSectionID] = $sectionAttachments;
		}

		$this->view->attachments       = $attachments;
		$this->view->maxFileSize       = $this->maxFileSize;
		$this->view->allowedExtensions = $this->documentLib->getAllowedExtensions();
		$this->view->userRole          = $this->getCurrentRole();

		$this->view->privileges = $this->getPrivileges();

		$this->view->downloadSectionAction = sprintf(
			"/documents/list/download-section/instance-resource-id/%d/instance-id/%d",
			$this->instanceResourceID,
			$this->instanceID
		);
		$this->view->uploadAction = sprintf(
			"/documents/list/list/instance-resource-id/%d/instance-id/%d",
			$this->instanceResourceID,
			$this->instanceID
		);

		$this->view->controller = $this;
		$this->view->form = $this->form;
		$this->view->sections = $sections;
	}

	public function uploadParcelPictureAction() {
		$this->_helper->layout()->disableLayout();
		$this->_helper->viewRenderer->setNoRender(true);
		if (!$this->getRequest()->isPost()) {
			return;
		}

		try {
			$userID  = $this->uploadUserID();
			$this->deleteExisting();
			$messages = $this->documentLib->uploadFile(
				'file',
				$this->instanceID,
				$userID,
				21,
				$this->getCurrentService(),
				null,
				false,
				true
			);

			if (is_array($messages)) {
				$this->_helper->json($messages);
				$this->getResponse()->setHttpResponseCode('400');
			}
			else {
				$this->_helper->json(true);
			}
		}
		catch(Exception $e) {
			$this->_helper->json($e->getMessage());
			$this->getResponse()->setHttpResponseCode('400');
		}
	}

	protected function deleteExisting() {
		$attachmentMapper = new Documents_Model_Mapper_Attachment();
		$pic = $attachmentMapper->getParcelPictures(
			$this->instanceID
		);

		if (count($pic) == 0) {
			return;
		}
		$pic = $pic[0];

		unlink($pic->path);

		$attachmentMapper->delete($pic->attachmentID);
	}

	/**
	 * Check whether the currently logged in user is allowed to
	 * upload to given section
	 */
	private function isAllowedToUpload($attachmentSectionID) {
		$privileges = $this->getPrivileges();

		if (array_key_exists($attachmentSectionID, $privileges)) {
			if (in_array($privileges[$attachmentSectionID], array('write', 'admin'))) {
				return true;
			}
		}

		return false;
	}

	/**
	 * Return the user info on uploading
	 *
	 * Either use the currently logged in user or, in case it's allowed,
	 * the chosen user from the form
	 *
	 * @return int
	 */
	private function uploadUserID() {
		if (Custom_UriUtils::isKoord() &&
			isset($this->form) && $this->form->getValue('upload_as') != 0) {

			$userID = $this->form->getValue('upload_as');
		}
		else {
			$userID = $this->getCurrentUserID();
		}

		return $userID;
	}

	/**
	 * Return the ID of the currently logged in user
	 */
	private function getCurrentUserID() {
		return Zend_Auth::getInstance()->getIdentity()->USER->USER_ID;
	}

	/**
	 * Return the service ID of the currently selected group
	 */
	private function getCurrentService() {
		if (Zend_Auth::getInstance()->getIdentity()->CURRENT_SERVICE) {
			return Zend_Auth::getInstance()->getIdentity()->CURRENT_SERVICE->getServiceId();
		}

		return null;
	}

	/**
	 * Return the role ID of the currently selected group
	 */
	private function getCurrentRole() {
		return Custom_UriUtils::getCurrentRole();
	}

	/**
	 * Assemble the privileges
	 *
	 * Get the privileges from both, the role and the service relations.
	 * Mingle them so as when both have a privilege to a section, following
	 * precedence is enforced:
	 * admin > write > read
	 */
	private function getPrivileges() {
		if ($this->_privileges == null) {
			$rolePrivileges    = $this->getRolePrivileges();
			$servicePrivileges = $this->getServicePrivileges();

			# those that are prsent in both
			$inter = array_uintersect($rolePrivileges, $servicePrivileges, function($a, $b) {
				if ($a == 'admin' || $b == 'admin') {
					return 'admin';
				}
				else if ($a == 'write' || $b == 'write') {
					return 'write';
				}

				return $a;
			});

			$a = array_diff_key($rolePrivileges,    $servicePrivileges);
			$b = array_diff_key($servicePrivileges, $rolePrivileges);

			# astonished that this is even possible
			$this->_privileges = $inter + $a + $b;
		}

		return $this->_privileges;
	}

	/**
	 * Return the privileges from the currently logged in Role
	 */
	private function getRolePrivileges() {
		$attachmentSectionRoleMapper = new Documents_Model_Mapper_AttachmentSectionRole();
		$rows = $attachmentSectionRoleMapper->getEntries($this->getCurrentRole());

		$privileges = array();
		foreach ($rows as $row) {
			$privileges[$row->attachmentSectionID] = $row->mode;
		}

		return $privileges;
	}

	/**
	 * Return the privileges from the currently logged in service
	 */
	private function getServicePrivileges() {
		$attachmentSectionServiceMapper = new Documents_Model_Mapper_AttachmentSectionService();
		$rows = $this->getCurrentService() ?
			$attachmentSectionServiceMapper->getEntries($this->getCurrentService()) :
			array();

		$privileges = array();
		foreach ($rows as $row) {
			$privileges[$row->attachmentSectionID] = $row->mode;
		}

		return $privileges;
	}

	public function downloadAction() {
		$attachmentIdentifier = $this->getRequest()->getParam('attachmentid');

		$this->_helper->layout()->disableLayout();

		$attachment = $this->attachmentMapper->findByIdentifier($attachmentIdentifier);

		$this->view->fileName = $attachment->name;
		$this->view->mimeType = $attachment->mimeType;
		$this->view->path     = $attachment->path;
	}

	public function downloadSectionAction() {
		$selected = $this->getRequest()->getParam('selected');
		$sectionId = $this->getRequest()->getParam('section');

		if (empty($selected)) {
			$this->session->messages = array('Bitte wählen Sie mindestens eine Datei zum Download aus.');
			$this->redirectBack();
		}

		if (!array_key_exists($sectionId, $this->getPrivileges())) {
			$this->session->messages = array('Es ist ein technischer Fehler aufgetreten (Fehlende Berechtigung).');
			$this->redirectBack();
		}

		$instanceId = $this->getRequest()->getParam('instance-id');
		$table = new Custom_Model_DbTable_AnswerDokNr();
		$row = $table->find($instanceId)->current();

		$dossierNr = $row->ANSWER;
		if (!$row->ANSWER) {
			$this->session->messages = array('Es ist ein technischer Fehler aufgetreten (Dossier-Nr. konnte nicht geladen werden).');
			$this->redirectBack();
		}

		$zip = new ZipArchive();
		$name = "Export_" . $dossierNr . ".zip";
		$path = "/tmp/" . $name;
		$result = $zip->open($path, ZipArchive::CREATE | ZipArchive::OVERWRITE);
		if (!$result) {
			throw new Exception("ZIP Error: ".$result);
		}
		foreach ($selected as $attachmentIdentifier) {
			$attachment = $this->attachmentMapper->findByIdentifier($attachmentIdentifier);
			Zend_Registry::get('log')->log('adding'.$attachment->path, Zend_Log::DEBUG);
			$zip->addFile($attachment->path, basename($attachment->path));
		}
		$zip->close();
		$this->_helper->layout()->disableLayout();

		$this->view->name = $name;
		$this->view->path = $path;
	}

	public function previewAction() {
		$attachmentIdentifier = $this->getRequest()->getParam('attachmentid');

		$this->_helper->layout()->disableLayout();

		$attachment = $this->attachmentMapper->findByIdentifier($attachmentIdentifier);

		$this->view->fileName   = $attachment->name;
		$this->view->mimeType   = $attachment->mimeType;
		$this->view->path       = $attachment->path;
		$this->view->identifier = $attachment->identifier;
		$this->view->instanceID = $attachment->instanceID;
		$this->view->thumbPath  = Zend_Registry::get('config')->attachment->thumb_path;
	}

	public function deleteAction() {
		$attachmentIdentifier = $this->getRequest()->getParam('attachmentid');
		$attachment           = $this->attachmentMapper->findByIdentifier($attachmentIdentifier);

		if (!$this->isDeleteAllowed($attachment)) {
			$this->session->messages = array('not allowed to delete this file');

			$this->redirectBack();
		}

		try {
			$this->documentLib->deleteFile($attachmentIdentifier);
		}
		catch(Exception $e) {
			$this->session->messages = $this->view->translate('Unable to delete file');
		}

		$this->redirectBack();
	}

	public function togglePublishAction() {
		$attachmentID = $this->getRequest()->getParam('attachmentid');
		$attachment   = $this->attachmentMapper->findByIdentifier($attachmentID);

		$sectionID = $attachment->attachmentSectionID;
		if (!$this->isAdmin($sectionID)) {
			return $this->redirectBack();
		}
		$newSection = $sectionID == Custom_UriConstants::ATTACHMENT_SECTION_APPLICANT_ID
			? Custom_UriConstants::ATTACHMENT_SECTION_PUBLICATION_ID
			: Custom_UriConstants::ATTACHMENT_SECTION_APPLICANT_ID;

		$attachment->attachmentSectionID = $newSection;
		$mapper = new Documents_Model_Mapper_Attachment();
		$mapper->update($attachment);

		$this->redirectBack();
	}

	/**
	 * Redirect back to the listing
	 */
	public function redirectBack() {
		$this->_helper->redirector('list', 'list', 'documents', array(
			'instance-resource-id' => $this->instanceResourceID,
			'instance-id'          => $this->instanceID
		));
	}

	/**
	 * Check whether delete is allowed for the current user
	 *
	 * @param Model_Section $section The Section model
	 * @param Model_Attachment $attachment The Attachment model
	 * @return bool
	 */
	public function isDeleteAllowed(Documents_Model_Data_Attachment $attachment) {
		if ($this->isAdmin($attachment->attachmentSectionID)) {
			return true;
		}

		# everyone can delete their own files
		if ($attachment->userID == $this->getCurrentUserID()) {
			return true;
		}

		# last but not least: you can delete files if they are from
		# the same service as currently logged in

		return false;
	}

	public function isAdmin($sectionID) {
		$privileges = $this->getPrivileges();
		if (!array_key_exists($sectionID, $privileges)) {
			return false;
		}
		return $privileges[$sectionID] == 'admin';
	}

	public function showPublish($sectionID) {
		return $sectionID == Custom_UriConstants::ATTACHMENT_SECTION_APPLICANT_ID &&
			$this->isAdmin($sectionID);
	}

	public function showUnpublish($sectionID) {
		return $sectionID == Custom_UriConstants::ATTACHMENT_SECTION_PUBLICATION_ID &&
			$this->isAdmin($sectionID);
	}
}
