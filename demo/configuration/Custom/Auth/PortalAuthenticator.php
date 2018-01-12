<?php

class Custom_Auth_PortalAuthenticator extends Camac_Authentication {

	/**
	 * Implementation of the superclass method. Performs the authentication
	 * process as needed by the current Camac instance.
	 *
	 * @return void
	 */
	public function authenticate() {
		$authAdapter = $this->getAuthAdapter();
		$authAdapter->setIdentity('portalUser');
		$authAdapter->setCredential('123qwe');

		if ($authAdapter->authenticate()->isValid()) {
			$this->loginSuccessful();
		}
		else {
			$this->logFailedAttempt('portalUser');
			$this->loginError();
		}
	}

	/**
	 * Implementation of the superclass method. Returns the Zend auth adapter
	 * configured as needed by the current Camac instance.
	 *
	 * @return Zend_Auth_Adapter_Interface
	 */
	public function getAuthAdapter() {

		if ($this->authAdapter === null) {

			// Istantiate auth adapter
			$db = Zend_Controller_Front::getInstance()->getParam('bootstrap')->getResource('db');

			$this->authAdapter = new Zend_Auth_Adapter_DbTable($db);
			$this->authAdapter->setTableName('USER');
			$this->authAdapter->setIdentityColumn('USERNAME');
			$this->authAdapter->setCredentialColumn('PASSWORD');
			$this->authAdapter->setCredentialTreatment("lower(md5(concat('" . Zend_Registry::get('config')->password->salt . "', ?)))");
			$select = $this->authAdapter->getDbSelect();
			$select->where('DISABLED = 0');
		}

		return $this->authAdapter;

	}

}
