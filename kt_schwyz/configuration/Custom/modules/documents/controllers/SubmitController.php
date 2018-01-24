<?php

/**
 * Controller for the page where the user uploads a sign document
 * and finally submits the form
 */
class Documents_SubmitController extends Camac_Controller_Action {

	/**
	 * The IR id of the documents page in the portal
	 */
	const PORTAL_DOCS_IR_ID = 678;

	/**
	 *  The IR id of the page that shows the submitted confirmation
	 */
	const SUBMITTED_PAGE_IR_ID = 674;

	/**
	 * This is the IR id of the current page
	 *
	 * Could've used the query param I know, but does it matter since
	 * the other ones are hard coded as well?
	 */
	const SUBMIT_INDEX_IR_ID = 680;

	/**
	 * The name of the file to be uploaded
	 */
	const SIGN_FILENAME = 'unterschriftenblatt.pdf';

	/**
	 * The instance state after submitting the form
	 */
	const SUBM_STATE = 30;

	/**
	 * The workflow item id after the instance is submitted
	 */
	const SUBMIT_WORKFLOW_ITEM_ID = 10;

	public function __construct(Zend_Controller_Request_Abstract $request,
								Zend_Controller_Response_Abstract $response,
								array $invokeArgs = array())
	{
		parent::__construct($request, $response, $invokeArgs);
		$this->instanceId = intval($this->getRequest()->getParam('instance-id'));

		$this->view->instanceId = $this->instanceId;
		$this->documentLib = new Documents_Lib_DocumentLib();
	}

	/**
	 * Show some text and the upload form
	 *
	 * @return void
	 */
	public function indexAction() {
		$form = new Documents_Data_UploadForm($this->instanceId);
		$form->initSubmitForm();

		$this->view->form = $form;

		$this->handleUploadedState();

		if ($this->getRequest()->isPost()) {
			// why don't we just post to the action directly?
			// well then we'd have to tell the form object what action it is,
			// which seems overkill, or else it would be tightly coupled to this
			// controller here
			$this->_uploadAction();
		}
	}

	/**
	 * Check the uploaded state
	 *
	 * When the sign paper was uploaded, the uploaded param will be
	 * set to true. Save this in the session and to the view, and check
	 * the session content next time the site is accessed
	 * @return void
	 */
	protected function handleUploadedState() {
		$uploaded = false;

		if ($this->getRequest()->getParam('uploaded', 0)) {
			$uploaded = true;
		}

		// this needs to be on a per instance basis
		$session = new Zend_Session_Namespace('portal');
		if (array_key_exists('signPaperUpload', $session) &&
			array_key_exists($this->instanceId, $session->signPaperUploaded) &&
			$session->signPaperUploaded[$this->instanceId]) {
			$uploaded = true;
		}

		$session->signPaperUploaded[$this->instanceId] = $uploaded;
		$this->view->isUploaded = $uploaded;
	}

	/**
	 * Navigate back to the documents portal page
	 *
	 * Perform a redirect to the portal documents page
	 * @return void
	 */
	public function backAction() {
		$this->_helper->redirector('list', 'portal', 'documents', array(
			'instance-resource-id' => self::PORTAL_DOCS_IR_ID,
			'instance-id'          => $this->instanceId
		));
	}

	/**
	 * Upload the file
	 *
	 * @return void
	 */
	public function _uploadAction() {
		$form = new Documents_Data_UploadForm($this->instanceId);

		$form->initSubmitForm();

		if (!($this->getRequest()->isPost() && $form->isValid($_POST))) {
			$this->_helper->MessageToFlash->addErrorMessagesToFlash($form->getMessages());
			return;
		}

		try {
			$uploadMessages = $this->documentLib->uploadFile(
				'file',
				$this->instanceId,
				Custom_UriConstants::USER_PORTAL,
				Custom_UriConstants::ATTACHMENT_SECTION_APPLICANT_ID,
				null, // serviceId
				self::SIGN_FILENAME,
				true // signature
			);
		}
		catch (Exception $e) {
			$this->_helper->MessageToFlash->addErrorMessagesToFlash($e->getMessage());
		}
		$this->_helper->MessageToFlash->addErrorMessagesToFlash($uploadMessages);

		// redirect anyway to prevent reloading
		$this->_helper->redirector('index', 'submit', 'documents', array(
			'instance-resource-id' => self::SUBMIT_INDEX_IR_ID,
			'instance-id'          => $this->instanceId,
			'uploaded'             => true
		));
	}

	/**
	 * Submit the dossier
	 *
	 * Set the dossier state to SUBM
	 * Perform a redirection to the page that shows the
	 * confirmation message
	 * @return void
	 */
	public function submitAction() {
		$instanceMapper      = new Application_Model_Mapper_Instance();
		$workflowEntryMapper = new Workflow_Model_Mapper_WorkflowEntry();
		$interpreter = Zend_Controller_Action_HelperBroker::getStaticHelper('Interpreter');

		$pigeon = Camac_Nest_Pigeon::getInstance();
		$instanceMapper->changeState(
			$pigeon->instanceId,
			NULL,
			self::SUBM_STATE
		);

		$workflowEntryMapper->makeEntry(
			$pigeon->instanceId,
			self::SUBMIT_WORKFLOW_ITEM_ID,
			Workflow_Action_Workflow_Data::MULTI_VALUE_IGNORE
		);

		// send email to Gesuchsteller
		$body = 'CAMAC Info (automatisch generierte E-Mail von CAMAC, bitte nicht darauf antworten)

EINGANGSBESTÄTIGUNG

Sehr geehrte Dame
Sehr geehrter Herr

Vielen Dank für Ihre Eingabe. Das Dossier mit der ID Nr. [INSTANCE_ID] wird umgehend von der zuständigen Gemeindebaubehörde auf Vollständigkeit geprüft. Falls zusätzliche Unterlagen notwendig sind oder wenn das Prüfverfahren / Bewilligungsverfahren gestartet wird, erhalten Sie eine entsprechende Statusmeldung.

Dossiers bei denen sämtliche Unterlagen und Angaben fehlen, können zurückgewiesen werden.

Mit freundlichen Grüssen
Gemeindebaubehörde [INSTANCE_LOCATION]';

		$mail = new Zend_Mail('UTF-8');
		$mail->setBodyText(
			$interpreter->direct($body, false)
		);
		$mail->setFrom('camac@ur.ch', 'Camac Kanton Uri');
		$mail->addTo(Custom_UriUtils::getGesuchstellerEmail($pigeon->instanceId));
		$mail->setSubject('Eingangsbestätigung');
		$mail->send();

		// send email to Gemeinde
		$body = 'CAMAC Info (automatisch generierte E-Mail von CAMAC, bitte nicht darauf antworten)

NEUES ONLINE DOSSIER

Sehr geehrte Dame
Sehr geehrter Herr

Via Online Portal wurde ein neues Dossier mit der ID Nr. [INSTANCE_ID] eingereicht. Bitte prüfen Sie das Dossier auf Vollständigkeit. Falls zusätzliche Unterlagen notwendig sind, schreiben Sie die entsprechende Nachricht in das dafür vorgesehene Feld «Mitteilung an Gesuchsteller» und klicken Sie auf «Nachforderung». Das Dossier wird blau hinterlegt und der Gesuchsteller erhält Ihre Mitteilung per E-Mail.

Falls es sich offensichtlich um ein Fake-Gesuch handelt (z.B. wenn ein leeres Formular versehentlich abgeschickt wurde), können Sie dieses abweisen. Durch klicken auf «Abweisen» wird das Dossier gelöscht.

Wenn das Dossier vollständig ist, klicken Sie auf «Dossier annehmen». Das Dossier wird in der Pendenzenliste Start angezeigt und erhält vom System die zugehörige CAMAC Nummer. Der Gesuchsteller erhält eine entsprechende Annahmebestätigung per E-Mail.

Bei Bedarf wandeln Sie das Dossier um in ein entsprechendes Verfahren mit kantonaler Beteiligung.


Bei Fragen stehen wir Ihnen gerne zur Verfügung.

Amt für Raumentwicklung
Koordinationsstelle für Baueingaben
Rathausplatz 5
6460 Altdorf

Tel. 041 875 24 29
E-Mail: raumplanung@ur.ch';

		$recipients = Custom_UriUtils::getGemeindeEmails($pigeon->instanceId);
		if (count($recipients) > 0) {
			$mail = new Zend_Mail('UTF-8');
			$mail->setBodyText(
				$interpreter->direct($body, false)
			);
			$mail->setFrom('camac@ur.ch', 'Camac Kanton Uri');
			foreach ($recipients as $recipient) {
				$mail->addTo($recipient->EMAIL, $recipient->SURNAME + $recipient->NAME);
			}
			$mail->setSubject('Neues Online Dossier');
			$mail->send();
		}

		$this->_helper->redirector('index', 'page', 'default', array(
			'instance-resource-id' => self::SUBMITTED_PAGE_IR_ID,
			'instance-id'          => $this->instanceId
		));
	}
}

