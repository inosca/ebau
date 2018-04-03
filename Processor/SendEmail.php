<?php

class Notification_Processor_SendEmail implements Notification_Manager_ProcessorInterface {

	public function process($instanceId, $recipient, $template) {
		$api = Notification_Manager_API::getInstance();
		// TODO: ensure we got the correct recipient's language
		$parsed = $api->parse($instanceId, $recipient, $template);

		$senderEmail = $api->getConfig()->sender_email;
		$senderName  = $api->getConfig()->sender_name;

		try {
			$mail = new Zend_Mail('UTF-8');

			$mail->setBodyText($parsed['BODY']);

			$mail->setFrom($senderEmail, $senderName);

			$mail->addTo(
				$recipient['EMAIL'],
				$recipient['NAME']
			);
			$mail->setSubject($parsed['SUBJECT']);
			$mail->send();

			return true;
		}
		catch (Exception $e) {
			// TODO: notify user somehow?
			return false;
		}
	}

	public function getTranslatedName() {
		$tr = Zend_Registry::get('Zend_Translate');
		return $tr->translate("Email senden");
	}
}
