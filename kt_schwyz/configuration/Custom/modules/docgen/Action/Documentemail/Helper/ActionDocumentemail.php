<?php

class Docgen_Action_Documentemail_Helper_ActionDocumentemail extends Camac_Action_Email_Helper_ActionEmail implements Camac_Action_Helper_Interface {

	/**
	 *
	 * Retrieves the instance of the concrete handler action
	 *
	 * @param int $actionId
	 * @return Camac_Action_Email_Action
	 */
	public function getHandlerAction($actionId) {
		$resourceAction = $this->getAction($actionId, true);
		return new Docgen_Action_Documentemail_Action($resourceAction);

	}

}
