<?php

/**
 * @SuppressWarnings(methods)
 * @SuppressWarnings(coupling)
 */
class Workflow_ListController extends Camac_Controller_Action {

	/**
	 * Instance ID
	 *
	 * @var           int $instanceID
	 */
	protected $instanceID;

	/**
	 * The current user role
	 *
	 * @var           int $userRole
	 */
	protected $userRole;


	public function __construct(
		Zend_Controller_Request_Abstract $request,
		Zend_Controller_Response_Abstract $response,
		array $invokeArgs = array()
	) {
		parent::__construct($request, $response, $invokeArgs);

		$this->instanceID            = intval($this->getRequest()->getParam('instance-id'));
		$this->instanceResourceID    = intval($this->getRequest()->getParam('instance-resource-id'));
		$this->userRole              = Zend_Auth::getInstance()->getIdentity()->CURRENT_ROLE->getRoleId();
		$this->workflowSectionMapper = new Workflow_Model_Mapper_WorkflowSection;
		$this->workflowEntryMapper   = new Workflow_Model_Mapper_WorkflowEntry;
	}

	public function listAction() {
		$form = new Workflow_Data_Form();

		if ($this->getRequest()->isPost()) {
			if ($form->isValid($_POST)) {
				$workflowEntries = $this->getRequest()->getParam('workflowEntries');

				foreach ($workflowEntries as $workflowItemID => $workflowEntryDate) {
					if (is_array($workflowEntryDate)) {
						$this->workflowEntryMapper->updateDate(
							key($workflowEntryDate),
							DateTime::createFromFormat(
								Zend_Registry::get('config')->date->application->phpFormat,
								$workflowEntryDate[key($workflowEntryDate)]
							)
						);
					}
					elseif ($workflowEntryDate == '') {
						continue;
					}
					else {
						$workflowEntry = new Workflow_Model_Data_WorkflowEntry(
							null,
							$this->instanceID,
							DateTime::createFromFormat(
								Zend_Registry::get('config')->date->application->phpFormat,
								$workflowEntryDate
							),
							$workflowItemID,
							1
						);

						$this->workflowEntryMapper->save($workflowEntry);
					}
				}
			}
			else {
				$this->_helper->MessageToFlash->addErrorMessagesToFlash($form->getMessages());
			}
		}

		$this->view->form = $form;
		$this->view->workflowSections = $this->workflowSectionMapper->getAll();
		$this->view->userRole = $this->userRole;
		$this->view->instanceID = $this->instanceID;
	}

	public function deleteAction() {
		$workflowEntryID = $this->getRequest()->getParam('workflowentryid');
		$this->workflowEntryMapper->delete($workflowEntryID);

		$this->_helper->redirector('list', 'list', 'workflow', array(
			'instance-resource-id' => $this->instanceResourceID,
			'instance-id'          => $this->instanceID
		));
	}
}
