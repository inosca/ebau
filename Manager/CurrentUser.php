<?php

class Notification_Manager_CurrentUser implements Notification_Manager_RecipientTypeInterface {

	public function getRecipients($instanceId) {
		$identity = Zend_Auth::getInstance()->getIdentity();
		$user = $identity->USER;
		return [[
			'NAME'   => sprintf("%s %s", $user->NAME, $user->SURNAME),
			'EMAIL'  => $user->EMAIL
		]];
	}

	public function getTranslatedName() {
		$tr = Zend_Registry::get('Zend_Translate');
		return $tr->translate("Aktiver Benutzer");
	}

}
