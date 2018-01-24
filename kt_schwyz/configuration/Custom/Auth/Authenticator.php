<?php

/**
 * Default implementation of the Camac_Authentication class.
 * Requires user name and password from a form, checks the password hash against
 * the value stored in the database.
 *
 * @author Alessandro Gaia <alessandro.gaia@blackpoints.ch>
 */

/**
 * Default implementation of the Camac_Authentication class.
 * Requires user name and password from a form, checks the password hash against
 * the value stored in the database.
 *
 * @package Custom\Auth
 */
class Custom_Auth_Authenticator extends Camac_Authentication {

	/**
	 * Implementation of the superclass method. Performs the authentication
	 * process as needed by the current Camac instance.
	 *
	 * @return void
	 */
	public function authenticate() {

		$form = new Application_Form_Login();

		// Get front controller and request
		$frontController = Zend_Controller_Front::getInstance();
		$request = $frontController->getRequest();

		// Check if request is post
		if ($request->isPost()) {

			// Check if the form is valid
			if ($form->isValid($_POST) && !$this->isLocked()) {
				$data = $form->getValues();

				$authAdapter = $this->getAuthAdapter();

				$authAdapter->setIdentity($data['username']);
				$authAdapter->setCredential($data['password']);

				if ($authAdapter->authenticate()->isValid()) {
					$this->loginSuccessful();
				}
				else {
					$this->logFailedAttempt($data['username']);
					$this->loginError();
				}
			}
			else {
				$this->loginError();
			}
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
			$select->where('"DISABLED" = 0');
		}

		return $this->authAdapter;

	}

}
