<?php


class Bab_EditController extends Camac_Controller_Action {

	protected $instanceId;

	protected $instanceResourceId;

	public function __construct(
		Zend_Controller_Request_Abstract $request,
		Zend_Controller_Response_Abstract $response,
		array $invokeArgs = array()
	) {
		parent::__construct($request, $response, $invokeArgs);

		$this->instanceId         = intval($this->getRequest()->getParam('instance-id'));
		$this->instanceResourceId = intval($this->getRequest()->getParam('instance-resource-id'));
		$this->babMapper = new Bab_Model_Mapper_Bab();
	}

	public function editAction() {
		$this->view->instanceId = $this->instanceId;
		$this->view->instanceResourceId = $this->instanceResourceId;
		$this->view->readonly = Custom_UriUtils::isKoord();
	}

	public function getAction() {
		$result = $this->babMapper->get($this->instanceId);
		return $this->_helper->json($result);
	}

	public function saveAction() {
		Custom_UriUtils::checkCSRF($this->getRequest());
		$body = $this->getRequest()->getRawBody();
		$entries = Zend_Json::decode($body);
		$result = $this->babMapper->save($this->instanceId, $entries);

		return $this->_helper->json($result);
	}

}
