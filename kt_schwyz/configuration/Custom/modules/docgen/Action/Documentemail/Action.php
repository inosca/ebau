<?php

/**
 * Docgen_Action_Documentemail_Action.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Mailwithattchment
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */

/**
 * Docgen_Action_Documentemail_Action.
 *
 * @category Docgen
 * @package  Docgen\Action\Mailwithattchment
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Documentemail_Action extends Camac_Action_Action
{

	/**
	 * Constructor.
	 *
	 * @param Camac_Model_Data_Resource_Action $action Given action
	 *
	 * @return void
	 */
	public function __construct($action)
	{
		parent::__construct($action, true);
	}

	/**
	 * Handles the execution of this action.
	 *
	 * @param boolean $previousSuccess Success status of previous action
	 *
	 * @return boolean
	 * @SuppressWarnings(complexity)
	 */
	public function handleAction($previousSuccess = true)
	{
		$currentSuccess = $previousSuccess;
		$action = $this->getResourceAction();


		$request = Zend_Controller_Front::getInstance()->getRequest();
		$circulationId = $request->getParam('circulation-id');

		if ($action->isAlwaysExecutable() || $previousSuccess) {
			$result = false;

			try {
				$dba = Zend_Controller_Front::getInstance()->getParam(
					'bootstrap'
				)->getResource('db');
				$query = $action->getQuery();
				$query = str_replace('[CIRCULATION_ID]', $circulationId, $query);
				$rows = $dba->query($query)->fetchAll();

				foreach ($rows as $row) {

					if (isset($row['NAME']) && isset($row['EMAIL'])
						&& !empty($row['NAME']) && !empty($row['EMAIL'])
					) {
						$mail = new Zend_Mail('UTF-8');
						$mail->setBodyText($action->getText());
						$mail->setFrom(
							$action->getSenderEmail(),
							$action->getSenderName()
						);
						$email = $row['EMAIL'];
						$recipient = $row['NAME'];
						$mail->addTo($email, $recipient);

						$attachment = $this->getAttachment($row['ACTIVATIONID']);
						$mail->addAttachment($attachment);

						// Send mail only if there are recipients
						if ($rows) {
							$mail->setSubject($action->getTitle());
							try {
								$mail->send();
							}
							catch (Exception $e) {
								Zend_Registry::get('log')->log(
									sprintf(
										"Could not send email to %s because of %s",
										$email,
										$e->getMessage()),
									Zend_Log::WARN
								);
							}
						}
					} else {
						Zend_Registry::get('log')->log(
							sprintf(
								'Name and/or recipient for e-mail '.
								'was not set: %s <%s> skipping..',
								$row['NAME'],
								$row['EMAIL']
							),
							Zend_Log::WARN
						);
					}
				}

				$result = true;
			}
			catch (Exception $e) {
				Zend_Registry::get('log')->log(
					"There was an error sending e-mails: " . $e->getMessage(),
					Zend_Log::ERR
				);
			}

			$this->setMessage($result);
			$currentSuccess = $previousSuccess && $result;
		}
		return parent::handleAction($currentSuccess);
	}

	/**
	 * Generate the attachment of the circulation tracer PDF
	 *
	 * @param int $activationId The identifier of the activation
	 *
	 * @return void
	 */
	protected function getAttachment($activationId)
	{
		// yes they're hardcoded for now. Deadline is closing in
		// TODO make this properly configurable in the action
		// since this action isn't able to be used outside of the scope of
		// sending emails on the start of circulations, there's no point in
		// making the things configurable.

		$request = Zend_Controller_Front::getInstance()->getRequest();

		$instanceResourceId = $request->getParam('instance-resource-id');
		$templateClassId = 82;

		if ($instanceResourceId == 467) {
			# NP
			$templateId = 161;
		}
		elseif ($instanceResourceId == 625) {
			# BD
			$templateId = 203;
		}
		else  {
			# BG, Other (AFU, ALA, ...)
			$templateId = 81;
		}

		$templateMapper      = new Docgen_Model_Mapper_Template();
		$templateClassMapper = new Docgen_Model_Mapper_Templateclass();

		$template      = $templateMapper->getTemplate($templateId);
		$templateClass = $templateClassMapper->getTemplateClass($templateClassId);
		$className     = Docgen_TemplateController_Utils::getClassName($templateClass);

		include_once $templateClass->path;

		$renderer = new $className($activationId);

		// Add attachment(s)
		$attachment = new Zend_Mime_Part($renderer->render($template->path));
		$attachment->type = 'application/pdf';
		$attachment->disposition = Zend_Mime::DISPOSITION_ATTACHMENT;
		$attachment->encoding = Zend_Mime::ENCODING_BASE64;
		$attachment->filename = sprintf("%s.pdf", $className);

		return $attachment;
	}

}
