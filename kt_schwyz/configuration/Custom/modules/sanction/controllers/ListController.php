<?php

class Sanction_ListController extends Camac_Controller_Action {

	public function __construct(
		Zend_Controller_Request_Abstract $request,
		Zend_Controller_Response_Abstract $response,
		array $invokeArgs = array()
	) {
		parent::__construct($request, $response, $invokeArgs);

		$this->instanceID = intval($this->getRequest()->getParam('instance-id'));
		$instanceMapper = new Application_Model_Mapper_Instance();
		$instance = $instanceMapper->getInstance($this->instanceID);
		$this->instanceStateID = $instance->getInstanceStateId();

		$this->serviceID = Zend_Auth::getInstance()->getIdentity()->CURRENT_SERVICE->getServiceId();
		$this->serviceGroupID = Zend_Auth::getInstance()->getIdentity()->CURRENT_SERVICE->getServiceGroupId();
		$this->isKoord = Custom_UriUtils::isKoord();
		$this->isCommunity = Custom_UriUtils::isCommunity();
		$this->userID    = Zend_Auth::getInstance()->getIdentity()->USER->USER_ID;

		$this->sanctionMapper = new Sanction_Model_Mapper_Sanction();
		$this->workflowEntryMapper = new Workflow_Model_Mapper_WorkflowEntry();
	}

	public function listAction() {
		$showAll = $this->isKoord || $this->isCommunity;
		$entries = $this->sanctionMapper->getEntries(
			$this->instanceID,
			$showAll ? null : $this->serviceID
		);
		$result = array();
		foreach ($entries as $row) {
			if (isset($result[$row->serviceID])) {
				$result[$row->serviceID][] = $row;
			} else {
				$result[$row->serviceID] = array($row);
			}
		}
		$this->view->groupedEntries = $result;
		$this->view->showAll = $showAll;
		$this->view->canAdd = (!$this->isKoord && !$this->isCommunity)
			&& $this->instanceStateID == Custom_UriConstants::INSTANCE_STATE_CIRC;
		$this->view->canEdit = !$this->isCommunity;
		$this->view->isKoord = $this->isKoord;
	}

	public function editAction() {
		$form = new Sanction_Data_Sanction();
		$this->view->form = $form;

		$sanctionID = $this->getRequest()->getParam('sanctionID');
		if ($sanctionID) {
			$this->view->sanction = $this->sanctionMapper->getEntry($sanctionID);
		}
		else {
			$this->view->sanction = Sanction_Model_Data_Sanction::getEmpty();
		}

		if ($this->getRequest()->isPost()) {
			if (!$form->isValid($_POST)) {
				$this->_helper->MessageToFlash->addErrorMessagesToFlash($form->getMessages());
				return;
			}

			$sanction = $this->view->sanction;
			$wasFinished = $sanction->isFinished === '1';

			if (!$sanction->isFinished && $form->getValue('isFinished')) {
				$sanction->finishedByUserID = $this->userID;
			}

			$sanction->text = $form->getValue('text');
			$sanction->startDate = Custom_Date::getDateTimeFromView($form->getValue('startDate'));
			$sanction->deadlineDate = Custom_Date::getDateTimeFromView($form->getValue('deadlineDate'));
			$sanction->endDate = Custom_Date::getDateTimeFromView($form->getValue('endDate'));
			$sanction->notice = $form->getValue('notice');
			$sanction->isFinished = $form->getValue('isFinished');

			if (!$sanction->sanctionID) {
				// create new
				$this->setWorkflowDate(Custom_UriConstants::WORKFLOW_ITEM_AC_START);
				$sanction->instanceID = $this->instanceID;
				$sanction->serviceID = $this->serviceID;
				$sanction->userID = $this->userID;
			}

			$this->sanctionMapper->save($sanction);

			if ($this->instanceStateID != Custom_UriConstants::INSTANCE_STATE_CIRC) {
				$isFinished = $this->sanctionMapper->isFinished($this->instanceID);
				if (!$wasFinished && $isFinished) {
					$this->setWorkflowDate(Custom_UriConstants::WORKFLOW_ITEM_AC_FINISH);
				}
				else if($wasFinished && !$isFinished) {
					$this->removeWorkflowDate(Custom_UriConstants::WORKFLOW_ITEM_AC_FINISH);
				}
			}

			$this->redirectToList();
		}
	}

	private function removeWorkflowDate($workflowItemID) {
		$entries = $this->workflowEntryMapper->getEntries(
			$this->instanceID,
			$workflowItemID
		);
		foreach ($entries as $entry) {
			$this->workflowEntryMapper->delete($entry->workflowEntryID);
		}
	}

	private function setWorkflowDate($workflowItemID) {
		$this->workflowEntryMapper->makeEntry(
			$this->instanceID,
			$workflowItemID,
			Workflow_Action_Workflow_Data::MULTI_VALUE_IGNORE
		);
	}

	public function deleteAction() {
		$id = $this->getRequest()->getParam('sanctionID');

		if (!$id || !is_numeric($id)) {
			die('invalid request'.$id);
		}

		$entry = $this->sanctionMapper->getEntry($id);

		if ($entry->serviceID !== $this->serviceID && !$this->isKoord) {
			die('invalid request');
		}

		$this->sanctionMapper->delete($id);
		$this->redirectToList();
	}

	private function redirectToList() {
		$this->_helper->redirector('list', 'list', 'sanction', array(
			'instance-resource-id' => intval(
				$this->getRequest()->getParam('instance-resource-id')),
			'instance-id'          => $this->instanceID
		));
	}
}
