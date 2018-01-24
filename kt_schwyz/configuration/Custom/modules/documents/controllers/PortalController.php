<?php

class Documents_PortalController extends Camac_Controller_Action {

	/**
	 * Edit Page IR ID
	 *
	 * This is the ID for the edit page instance resource in the portal
	 */
	const EDIT_PAGE_IR_ID = 671;

	/**
	 * Submit page IR ID
	 *
	 * This is the ID for the submit page instance resource in the portal
	 */
	const SUBMIT_IR_ID = 680;

	/**
	 * The ID of the page that allows re-submitting the form when it is in NFD
	 */
	const NFD_COMPLETE_IR_ID = 681;

	/**
	 * Class constructor
	 *
	 * @param Zend_Controller_Request_Abstract $request The request
	 * @param Zend_Controller_Response_Abstract $response The response
	 * @param array $invokeArgs A list invoked arguments
	 * @return void
	 */
	public function __construct(
			Zend_Controller_Request_Abstract $request,
			Zend_Controller_Response_Abstract $response,
			array $invokeArgs = array()
	) {
		parent::__construct($request, $response, $invokeArgs);
		$portalSessionMapper = new Portal_Model_Mapper_Session();
		$instanceMapper      = new Application_Model_Mapper_Instance();

		$this->instance  = $instanceMapper->getInstance(
			intval($this->getRequest()->getParam('instance-id'))
		);
		$this->instanceResourceId = intval($this->getRequest()->getParam('instance-resource-id'));
		$this->documentLib = new Documents_Lib_DocumentLib();
	}

	/**
	 * List action hook
	 *
	 * @return void
	 */
	public function listAction() {
		$attachmentMapper     = new Documents_Model_Mapper_Attachment();

		$this->view->instanceId = $this->instance->getInstanceId();
		$this->form             = new Documents_Data_UploadForm($this->view->instanceId);

		$this->form->initPortalForm();
		$this->view->maxFileSize = Zend_Registry::get('config')->attachment->upload_max_filesize;

		if ($this->getRequest()->isPost() && $this->form->isValid($_POST)) {
			$digitalSignature = (bool)$this->getRequest()->getParam('signature');
			$isConfidential   = (int)$this->getRequest()->getParam('isConfidential');

			$filename  = $this->documentLib->getFileName('file');

			try {
				$uploadMessages = $this->documentLib->uploadFile(
					'file',
					$this->instance->getInstanceId(),
					Custom_UriConstants::USER_PORTAL,
					Custom_UriConstants::ATTACHMENT_SECTION_APPLICANT_ID,
					null,
					$filename,
					$digitalSignature,
					false,
					$isConfidential
				);

				$this->_helper->MessageToFlash->addErrorMessagesToFlash($uploadMessages);
			}
			catch(Exception $e) {
				$this->_helper->MessageToFlash->addErrorMessagesToFlash($e->getMessage());
			}
		}
		else {
			$this->_helper->MessageToFlash->addErrorMessagesToFlash($this->form->getMessages());
		}

		$this->view->attachments     = $attachmentMapper->getAttachments(
			$this->instance->getInstanceId(),
			Custom_UriConstants::ATTACHMENT_SECTION_APPLICANT_ID
		);
		$this->view->canDelete = (int)$this->instance->getInstanceStateId() === Custom_UriConstants::INSTANCE_STATE_NEW_PORTAL;
		$this->view->messages = $this->_helper->FlashMessenger->getMessages();
		$this->view->form = $this->form;
	}

	public function downloadAction() {
		$attachmentMapper     = new Documents_Model_Mapper_Attachment();
		$attachmentIdentifier = $this->getRequest()->getParam('attachmentid');

		$this->_helper->layout()->disableLayout();

		$attachment = $attachmentMapper->findByIdentifier($attachmentIdentifier);

		$this->view->fileName = $attachment->name;
		$this->view->mimeType = $attachment->mimeType;
		$this->view->path     = $attachment->path;
	}

	public function previewAction() {
		$attachmentMapper     = new Documents_Model_Mapper_Attachment();
		$attachmentIdentifier = $this->getRequest()->getParam('attachmentid');

		$this->_helper->layout()->disableLayout();

		$attachment = $attachmentMapper->findByIdentifier($attachmentIdentifier);

		$this->view->fileName   = $attachment->name;
		$this->view->mimeType   = $attachment->mimeType;
		$this->view->path       = $attachment->path;
		$this->view->identifier = $attachment->identifier;
		$this->view->instanceID = $attachment->instanceID;
		$this->view->thumbPath  = Zend_Registry::get('config')->attachment->thumb_path;
	}

	public function deleteAction() {
		$attachmentIdentifier = $this->getRequest()->getParam('attachmentid');

		if ((int)$this->instance->getInstanceStateId() !== Custom_UriConstants::INSTANCE_STATE_NEW_PORTAL) {
			$this->_helper->FlashMessenger->addMessage($this->view->translate('Not allowed to delete this file'));
			$this->redirectBack();
		}

		try {
			$this->documentLib->deleteFile($attachmentIdentifier);
		}
		catch(Exception $e) {
			$this->_helper->FlashMessenger->addMessage($this->view->translate('Unable to delete file'));
		}

		$this->redirectBack();
	}

	/**
	 * Handle the next and previous button used in the portal
	 *
	 * @return void
	 */
	public function navigateAction() {
		$prev = $this->getRequest()->getParam('previous');

		if ($prev !== NULL) {
			$this->_helper->redirector('edit-page', 'form', 'default', array(
				'instance-resource-id' => self::EDIT_PAGE_IR_ID,
				'instance-id'          => $this->instance->getInstanceId()
			));

			return;
		}

		$next = $this->getRequest()->getParam('next');

		if ($next) {
			if ($this->isInstanceNew()) {
				$this->_helper->redirector('index', 'submit', 'documents', array(
					'instance-resource-id' => self::SUBMIT_IR_ID,
					'instance-id'          => $this->instance->getInstanceId()
				));
			}
			else {
				$this->_helper->redirector('index', 'page', 'default', array(
					'instance-resource-id' => self::NFD_COMPLETE_IR_ID,
					'instance-id'          => $this->instance->getInstanceId()
				));
			}
			return;
		}

		throw new Exception("This should not have happened");
	}

        /**
	 * Whether the instance is in NEW_PORTAL
	 *
	 * @return bool
	 */
	protected function isInstanceNew() {
		$newPortalStateId = Custom_UriConstants::INSTANCE_STATE_NEW_PORTAL;
		return $this->instance->getInstanceStateId() == $newPortalStateId;
	}

	/**
	 * Redirect back to the listing
	 */
	public function redirectBack() {
		$this->_helper->redirector('list', 'portal', 'documents', array(
			'instance-resource-id' => $this->instanceResourceId,
			'instance-id'          => $this->instance->getInstanceId()
		));
	}
}
