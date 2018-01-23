<?php

/**
 * This class exposes the public API for the i-web portal.
 * For doc generation see the make targets
 * "install-api-doc" and "generate-api-doc"
 *
 * @author Christian Zosel <christian.zosel@adfinis-sygroup-ch>
 * @package Portal\Controller
 */
class Portal_UserController extends Camac_Controller_Action {

	/**
	 * Get a new session hash for a portal user.
	 * This method is called directly from the i-web portal server.
	 *
	 * @api {post} /session/resource-id/248 Get a new session hash
	 * @apiName PostSession
	 * @apiGroup User
	 * @apiDescription This endpoint has to be called first. It generates
	 * a random session hash for a given portal user ID. Call this directly
	 * from your server and make sure that the X-Auth secret is never
	 * sent to users.
	 *
	 * @apiHeader {String} X-Auth The common secret auth token
	 * @apiHeader {String} User-Agent Set this to any value (e.g. 'i-web')
	 * @apiParam {String} portalId Unique identifier for the user (e.g. user ID)
	 *
	 * @apiSuccess {String} hash The generated session hash
	 * @apiError 400 Invalid method or portalId missing
	 * @apiError 401 X-Auth missing or invalid
	 *
	 * @apiVersion 0.0.0
	 */
	public function sessionAction() {
		if (!$this->_request->isPost()) {
			return self::error(400, 'invalid request method '.$this->_request->getMethod());
		}
		$auth = $this->_request->getHeader('X-Auth');
		if ($auth !== Zend_Registry::get('config')->portal->secret) {
			Zend_Registry::get('log')->log(__FILE__."::".__LINE__."> " .
				"Portal auth failed in hash generator", Zend_Log::DEBUG);
			return self::error(401, 'authentication failed');
		}
		$portalId = $this->_request->getParam('portalId');
		if (!$portalId) {
			return self::error(400, 'portalId missing');
		}

		$hash = Portal_Model_Mapper_Session::getNewSession($portalId);

		return $this->_helper->json(array('hash' => $hash));
	}

	/**
	 * Invalidates a session.
	 *
	 * @api {get/post} /logout/resource-id/248 Invalidate a session
	 * @apiName PostLogout
	 * @apiGroup User
	 * @apiDescription This endpoint has to be called when the user logs out
	 * of the i-web portal to clean up the associated CAMAC session.
	 * This method needs to be called directly by the client.
	 *
	 * @apiHeader {String} X-Camac-Session The user's session hash, as returned from /session
	 * @apiHeader {String} X-Redirect-To The URL to which the user should be redirected
	 *
	 * @apiError 401 X-Camac-Session missing or invalid
	 *
	 * @apiVersion 0.0.0
	 */
	public function logoutAction() {
		$hash = $this->_request->getParam('X-Camac-Session');
		$result = Portal_Model_Mapper_Session::logout($hash);

		if (!$result) {
			Zend_Registry::get('log')->log(__FILE__."::".__LINE__."> "
				. "Portal auth failed in logout", Zend_Log::DEBUG);
			return self::error(401, 'authentication failed');
		}

		Zend_Session::destroy();

		// empty response
		$this->_helper->layout->disableLayout();
		$this->_helper->viewRenderer->setNoRender(TRUE);

		$redirectTo = $this->_request->getParam('X-Redirect-To');
		if (!$redirectTo) {
			$redirectTo = $this->_request->getHeader('Referer');
		}
		Zend_Controller_Action_HelperBroker::getStaticHelper('Redirector')
			->gotoUrl($redirectTo, array('prependBase' => false));
	}

	public function overviewAction() {
		$session  = new Zend_Session_Namespace('portal');
		$portalId = $session->id;

		if (!$portalId) {
			Zend_Registry::get('log')->log(__FILE__."::".__LINE__."> " .
				"Portal auth in dossier overview failed", Zend_Log::DEBUG);
			return self::error(401, 'authentication failed');
		}

		$overview = Portal_Model_Mapper_Session::getOverview($portalId);
		if (count($overview) === 0) {
			$view = Zend_Controller_Front::getInstance()->getParam('bootstrap')->getResource('view');
			$this->redirect($view->url(array(
				'module' => 'default',
				'controller' => 'index',
				'action' => 'index',
				'resource-id' => 251
			)));
		}
		$this->view->overview = $overview;
	}

	/**
	 * Entry point for portal users who want to enter CAMAC. This method
	 * is called by the portal user, who is redirected from the i-web portal.
	 * @api {get/post} /entry/resource-id/248/instance-id/:instance-id enter CAMAC
	 * @apiName PostEntry
	 * @apiGroup User
	 * @apiDescription Send the user to this URL, when he wants to enter CAMAC.
	 *
	 * @apiParam {Number} instance-id Optional URL parameter. Redirects the user to the given instance after login.
	 * @apiParam {String} X-Camac-Session The user's session hash, as returned from /session
	 * @apiParam {String} firstName The user's first name
	 * @apiParam {String} lastName The user's last name
	 * @apiParam {String} street The user's street name
	 * @apiParam {String} zip The user's ZIP code
	 * @apiParam {String} city The user's city name
	 * @apiError 401 X-Camac-Session missing or invalid
	 *
	 * @apiVersion 0.0.0
	 */
	public function entryAction() {
		$hash = $this->_request->getParam('X-Camac-Session');
		$portalId = Portal_Model_Mapper_Session::getUserByHash($hash);

		if (!$portalId) {
			Zend_Registry::get('log')->log(__FILE__."::".__LINE__."> "
				. "Portal auth entry point failed", Zend_Log::DEBUG);
			return self::error(401, 'authentication failed');
		}

		// sign in as portal user
		$session            = new Zend_Session_Namespace('portal');
		$session->id        = $portalId;
		$fields = array(
			"organisation",
			"salutation",
			"firstName",
			"lastName",
			"email",
			"street",
			"streetNumber",
			"zip",
			"city",
			"addressSupplement",
			"phonePrivate",
			"phoneWork",
			"phoneMobile"
		);
		$personalData = array();
		foreach ($fields as $field) {
			$personalData[$field] = $this->_request->getParam($field);
		}
		$session->personalData = $personalData;

		$view = Zend_Controller_Front::getInstance()->getParam('bootstrap')->getResource('view');
		$session->redirectTo = $view->url(array(
			'module' => 'portal',
			'controller' => 'user',
			'action' => 'overview'
		));

		$authenticator = new Custom_Auth_PortalAuthenticator();
		$authenticator->authenticate();
	}

	/**
	 * Error handling for API requests
	 *
	 * @param int $code HTTP status code
	 * @param string $message error message
	 * @return string JSON payload
	 */
	private function error($code, $message) {
		$this->_response->setHttpResponseCode($code);
		return $this->_helper->json(array('error' => $message));
	}
}
