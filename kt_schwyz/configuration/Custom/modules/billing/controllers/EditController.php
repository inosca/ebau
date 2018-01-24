<?php

/**
 * @SuppressWarnings(methods)
 * @SuppressWarnings(coupling)
 */
class Billing_EditController extends Camac_Controller_Action {

	protected $accountMapper;

	protected $entryMapper;

	protected $userRole;

	protected $userID;

	public function __construct(
		Zend_Controller_Request_Abstract $request,
		Zend_Controller_Response_Abstract $response,
		array $invokeArgs = array()
	) {
		parent::__construct($request, $response, $invokeArgs);

		$this->accountMapper = new Billing_Model_Mapper_Account();
		$this->entryMapper   = new Billing_Model_Mapper_Entry();

		$this->userRole  = Zend_Auth::getInstance()->getIdentity()->CURRENT_ROLE->getRoleId();
		$this->serviceID = Zend_Auth::getInstance()->getIdentity()->CURRENT_SERVICE->getServiceId();
		$this->serviceGroupID = Zend_Auth::getInstance()->getIdentity()->CURRENT_SERVICE->getServiceGroupId();
		$this->isKoord = Custom_UriUtils::isKoord();

		$this->userID    = Zend_Auth::getInstance()->getIdentity()->USER->USER_ID;

		$this->instanceID = intval($this->getRequest()->getParam('instance-id'));
	}

	public function editAction() {
		$form = new Billing_Data_Billing($this->serviceGroupID);
		$this->view->form = $form;

		$instanceMapper = new Application_Model_Mapper_Instance();
		$instance = $instanceMapper->getInstance($this->instanceID);
		$isBaubegleitung = Custom_UriUtils::isDoneOrArch($instance->getInstanceStateId());
		if ($this->getRequest()->isPost()) {
			if ($form->isValid($_POST)) {
				$account = $form->getValue('account');
				$amount  = $form->getValue('amount');
				$hours   = $form->getValue('hours');
				$basic   = $form->getValue('basic');

				if (!$amount && !$hours && !$basic) {
					$this->_helper->FlashMessenger->addMessage(
						"Bitte erfassen Sie eine Gebühr.", ERROR_MESSAGE);
				} else {
					$type = $isBaubegleitung ?
						BILLING_MODEL_MAPPER_ENTRY::TYPE_BAUBEGLEITUNG :
						BILLING_MODEL_MAPPER_ENTRY::TYPE_BAUBEWILLIGUNG;

					if ($hours) {
						$amountType = 1;
						$amount = $hours;
					} else if ($amount) {
						$amountType = 0;
					} else {
						$amountType = 2;
						$amount = $basic;
					}

					if ($account == -1) {
						$department = $form->getValue('other_dept');
						$name       = $form->getValue('other_name');
						$account    = $form->getValue('other_account');

						$billingAccount = new Billing_Model_Data_Account(
							null,
							$department,
							$name,
							$account,
							null,
							false
						);

						$account = $this->accountMapper->insert($billingAccount);
					}

					$billingEntry = new Billing_Model_Data_Entry(
						null,
						$amount,
						$account,
						$this->userID,
						$this->instanceID,
						$this->serviceID,
						new DateTime(),
						$type,
						$amountType,
						$isBaubegleitung ? $form->getValue('reason') : null,
						0
					);

					$this->entryMapper->insert($billingEntry);
				}
			}
			else {
				$this->_helper->MessageToFlash->addErrorMessagesToFlash($form->getMessages());
			}
		}

		$this->view->accountGroups = $this->accountMapper->getGroupedAccounts(true, $this->serviceGroupID, $instance->getInstanceStateId());
		$this->view->userRole = $this->userRole;
		$this->view->serviceID = $this->serviceID;
		$this->view->isKoord = $this->isKoord;
		$this->view->isBaubegleitung = $isBaubegleitung;
		$this->view->hourlyRate = Billing_Model_Mapper_Config::getConfigByName('hourly_rate');

		$this->view->TYPE_BAUBEGLEITUNG = BILLING_MODEL_MAPPER_ENTRY::TYPE_BAUBEGLEITUNG;
		$this->isKoord ?
			$this->view->entries = $this->entryMapper->getEntries($this->instanceID) :
			$this->view->entries = $this->entryMapper->getEntries($this->instanceID, $this->serviceID);
		$this->view->hasUninvoiced = count(array_filter($this->view->entries, function($entry) {
			return $entry->invoiced == 0;
		})) > 0;
	}

	public function deleteAction() {
		$deleteID = $this->getRequest()->getParam('entryid');

		$entry = $this->entryMapper->getEntry($deleteID);

		if ($entry->serviceID !== $this->serviceID && !$this->isKoord) {
			die('invalid request');
		}
		$this->entryMapper->delete($deleteID);
		$this->accountMapper->deleteIfNotPredefined($entry->billingAccountID);

		$this->_helper->redirector('edit', 'edit', 'billing', array(
			'instance-resource-id' => intval($this->getRequest()->getParam('instance-resource-id')),
			'instance-id'          => $this->instanceID
		));
	}

	/**
	 * This action is triggered when the Button
	 * "Aktuelle Rechnung abschliessen" is clicked.
	 *
	 * It marks all uninvoiced billing entries as invoiced
	 * and generates a bill, which is saved in the documents module.
	 */
	public function completeAction() {
		if ($this->getRequest()->isPost() && $this->isKoord) {
			try {
				$entries = $this->entryMapper->getUninvoicedEntries($this->instanceID);
				$hasBew = self::hasOfType($entries, 0);
				$hasBgl = self::hasOfType($entries, 1);

				// generate bill(s) and save in documents module
				if($hasBew) {
					$this->generateAndSaveBill(0);
				}
				if($hasBgl) {
					$this->generateAndSaveBill(1);
				}

				// mark all entries as invoiced
				foreach($entries as $entry) {
					$entry->invoiced = 1;
					$this->entryMapper->update($entry);
				}

				$this->_helper->FlashMessenger->addMessage(
					'Die Rechnung wurde erfolgreich generiert und unter "Dokumente" abgelegt.',
					SUCCESS_MESSAGE
				);
			} catch (Exception $e) {
				$this->_helper->FlashMessenger->addMessage(
					'Beim Erstellen der Rechnung ist ein Fehler aufgetreten',
					ERROR_MESSAGE
				);
				Zend_Registry::get('log')->log($e->getMessage(), Zend_Log::ERR);
			}
		}

		$this->_helper->redirector('edit', 'edit', 'billing', array(
			'instance-resource-id' => intval($this->getRequest()->getParam('instance-resource-id')),
			'instance-id'          => $this->instanceID
		));
	}

	private static function hasOfType($entries, $type) {
		return count(array_filter($entries, function($entry) use ($type) {
			return $entry->type == $type;
		}));
	}
	/**
	 * Generate a bill of the given type and save it in
	 * the documents module.
	 *
	 * @param {int} $typeId 0 for BEW, 1 for BGL
	 * @return void
	 */
	private function generateAndSaveBill($typeId) {
		$typeConf = self::getTypeConf($typeId);

		$output = Docgen_TemplateController_Utils::getRenderedDocument(
			$typeConf['rendererId'],
			self::getTemplateId($this->userRole, $typeId)
		);

		$documentLib = new Documents_Lib_DocumentLib();

		$filename = sprintf('Rechnung_%s_%s.docx', $typeConf['label'], date('Y-m-d-His'));
		$path = $documentLib->getUploadFolder($this->instanceID);
		$path = $path ."/". $filename;

		file_put_contents($path, $output);
		$size = filesize($path);

		$attachment = new Documents_Model_Data_Attachment(
			null,
			$filename,
			$this->instanceID,
			$path,
			$size,
			new DateTime('now'),
			$this->userID,
			md5(time() . $path . $size),
			Docgen_TemplateController_Utils::MIME_DOCX,
			62,
			$this->serviceID,
			false,
			false
		);

		$attachmentMapper = new Documents_Model_Mapper_Attachment();
		$attachmentMapper->save($attachment);
	}

	private static function getTemplateId($roleId, $typeId) {
		$templates = array();
		$templates[Custom_UriConstants::ROLE_BD] = array(
			'0' => 204,
			'1' => 206
		);
		$templates[Custom_UriConstants::ROLE_BG] = array(
			'0' => 121,
			'1' => 207
		);
		$templates[Custom_UriConstants::ROLE_NP] = array(
			'0' => 202,
			'1' => 205
		);
		return $templates[$roleId][$typeId];
	}

	private static function getTypeConf($typeId) {
		$conf = array(
			'0' => array(
				'rendererId' => 208,
				'label' => 'Baubewilligung'
			),
			'1' => array(
				'rendererId' => 225,
				'label' => 'Baubegleitung'
			)
		);
		return $conf[$typeId];
	}
}
