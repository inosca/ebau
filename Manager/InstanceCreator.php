<?php

class Notification_Manager_InstanceCreator implements Notification_Manager_RecipientTypeInterface {

	public function getRecipients($instanceId) {
		// TODO: implement
		return [];
	}

	public function getTranslatedName() {
		$tr = Zend_Registry::get('Zend_Translate');
		return $tr->translate("Gesuch-Ersteller");
	}

}
