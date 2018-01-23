<?php


class Buildingauthority_EditController extends Camac_Controller_Action {

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
	}

	public function editAction() {
		$form = new Buildingauthority_Data_Form();
		$baSectionMapper = new Buildingauthority_Model_Mapper_BuildingAuthoritySection();
		$baCommentMapper = new Buildingauthority_Model_Mapper_BuildingAuthorityComment();
		$baItemDisMapper = new Buildingauthority_Model_Mapper_BuildingAuthorityItemDis();
		$baButtonMapper  = new Buildingauthority_Model_Mapper_BuildingAuthorityButton();
		$baButtonStateMapper  = new Buildingauthority_Model_Mapper_BuildingAuthorityButtonState();
		$workflowItemMapper   = new Workflow_Model_Mapper_WorkflowItem();
		$workflowEntryMapper  = new Workflow_Model_Mapper_WorkflowEntry();

		$savedComments = $baCommentMapper->getCommentsByInstance($this->instanceId);

		if ($this->getRequest()->isPost()) {
			if ($form->isValid($_POST)) {
				$workflowItems = $this->getRequest()->getParam('workflowItem');
				$comments      = $this->getRequest()->getParam('comment');

				foreach ($workflowItems as $itemId => $date) {
					if (!$date) {
						continue;
					}

					if (is_array($date)) {
						foreach ($date as $group => $singleDate) {
							if (!$singleDate) {
								continue;
							}

							$preparedDate = DateTime::createFromFormat(
								Zend_Registry::get('config')->date->application->phpFormat,
								$singleDate
							);

							// Check if such an entry already exists
							$existingEntry = $workflowEntryMapper->getEntryByUniqueKey(
								$this->instanceId,
								$itemId,
								$group
							);

							if (!$existingEntry) {
								$workflowEntryMapper->makeEntry(
									$this->instanceId,
									$itemId,
									Workflow_Action_Workflow_Data::MULTI_VALUE_APPEND,
									$preparedDate,
									$group
								);
							}
							else {
								$workflowEntryMapper->updateDate(
									$existingEntry->workflowEntryID,
									$preparedDate,
									$group
								);
							}
						}
					}
					else {
						$preparedDate = DateTime::createFromFormat(
							Zend_Registry::get('config')->date->application->phpFormat,
							$date
						);
						$workflowEntryMapper->makeEntry(
							$this->instanceId,
							$itemId,
							Workflow_Action_Workflow_Data::MULTI_VALUE_REPLACE,
							$preparedDate
						);
						$this->workflowSideEffect($itemId, $preparedDate);
					}
				}

				// Save comments, check if new or update
				foreach($comments as $sectionId => $comment) {
					if (!is_array($comment)) {
						$comment = array(1 => $comment);
					}

					foreach ($comment as $group => $groupComment) {
						if (!$groupComment) {
							continue;
						}

						if (isset($savedComments[$sectionId][$group])) {
							$currentComment = $savedComments[$sectionId][$group];
							$currentComment->text = $groupComment;
							$currentComment->group = $group;

							$baCommentMapper->update($currentComment);
						}
						else {
							$newComment = new Buildingauthority_Model_Data_BuildingAuthorityComment(
								null,
								$sectionId,
								$this->instanceId,
								$groupComment,
								$group
							);
							$newCommentId = $baCommentMapper->save($newComment);
							$savedComments[$sectionId][$group] = $baCommentMapper->getComment($newCommentId);
						}
					}
				}

				// First enable all sections before disabling the selected ones
				$baSectionMapper->enableAll($this->instanceId);

				// Save disabled elements
				$disabledSections = $this->getRequest()->getParam('disabledSections', array());
				foreach ($disabledSections as $sectionId => $flag) {
					$baSectionMapper->disable($sectionId, $this->instanceId);
				}

				// Enable all items before disabling the selected ones
				$baItemDisMapper->enableAll($this->instanceId);

				$disabledItems = $this->getRequest()->getParam('disabledItems', array());
				foreach($disabledItems as $itemId => $groups) {
					foreach($groups as $group => $flag) {
						$baItemDisMapper->disable($itemId, $this->instanceId, $group);
					}
				}

				$baButtonStateMapper->enableAll($this->instanceId);
				$disabledButtons = $this->getRequest()->getParam('disabledButtons', array());
				foreach($disabledButtons as $buttonId => $flag) {
					$baButtonStateMapper->setIsDisabled($buttonId, $this->instanceId);

					// @HACK
					// There is exactly one exception when disabling buttons.. because of
					// time/resource management we will solve this exception with a hack.
					// Cleaner way would be to handle all the disable checkboxes and values
					// with hidden input values for each disabled button (or something like this).
					$exceptionButtonId = Buildingauthority_Model_Mapper_BuildingAuthorityButton::BUTTON_ID_BAUBEWILLIGUNG_ERTEILT;
					if ($buttonId === $exceptionButtonId) {
						$baButtonStateMapper->setIsDisabled(
							Buildingauthority_Model_Mapper_BuildingAuthorityButton::BUTTON_ID_BAU_BEENDET_GEOMETER,
							$this->instanceId
						);
					}
				}
			} else {
				$this->_helper->MessageToFlash->addErrorMessagesToFlash($form->getMessages());
			}
		}

		$availableWorkflowItems = array();
		foreach ($workflowItemMapper->getBuildingAuthorityWorkflows() as $item) {
			$availableWorkflowItems[$item->getID()] = $item;
		}

		// Get group count
		$workflowGroupCount = $workflowEntryMapper->getMaxGroupCount($this->instanceId);
		$commentGroupCount  = isset($savedComments[3]) ? max(array_keys($savedComments[3])) : 0;

		$this->view->instanceId    = $this->instanceId;
		$this->view->sections      = $baSectionMapper->getSections(
			array('BUILDING_AUTHORITY_SECTION_ID ASC')
		);
		$this->view->groupCount    = max($workflowGroupCount, $commentGroupCount, 1); // Minimum max value needs to be 1
		$this->view->workflowItems = $availableWorkflowItems;
		$this->view->comments      = $savedComments;
		$this->view->buttons       = $baButtonMapper->getButtons();
		$this->view->buttonClass   = 'Buildingauthority_Model_Mapper_BuildingAuthorityButton';
		$this->view->dateFormat    = Zend_Registry::get('config')->date->application->jsFormat;
		$this->view->form          = $form;
	}

	public function notifyAction() {
		$buttonId        = key($this->getRequest()->getParam('button'));
		$baButtonMapper  = new Buildingauthority_Model_Mapper_BuildingAuthorityButton();

		$messages = $baButtonMapper->handleAction($buttonId, $this->instanceId);

		foreach($messages['success'] as $message) {
			$this->_helper->FlashMessenger->addMessage(
				$message,
				SUCCESS_MESSAGE
			);
		}

		foreach($messages['error'] as $message) {
			$this->_helper->FlashMessenger->addMessage(
				$message,
				ERROR_MESSAGE
			);
		}

		$this->_helper->redirector('edit', 'edit', 'buildingauthority', array(
			'instance-resource-id' => $this->instanceResourceId,
			'instance-id'          => $this->instanceId
		));
	}

	private function workflowSideEffect($itemId, DateTime $date) {
		$workflowEntryMapper  = new Workflow_Model_Mapper_WorkflowEntry();

		$bauEinspracheentscheidId = 47;
		$baubewilligungGueltigBisId = 71;
		if ($itemId === $bauEinspracheentscheidId) {
			$newDate = new DateTime();
			$newDate->setTimestamp(strtotime('+1 year', $date->getTimestamp()));

			$workflowEntryMapper->makeEntry(
				$this->instanceId,
				$baubewilligungGueltigBisId,
				Workflow_Action_Workflow_Data::MULTI_VALUE_REPLACE,
				$newDate
			);
		}

		$versandBaubewilligung = 72;
		$versandBaubewilligungBtn = 12;
		if ($itemId === $versandBaubewilligung) {
			$baButtonMapper  = new Buildingauthority_Model_Mapper_BuildingAuthorityButton();
			$button12 = $baButtonMapper->getButton($versandBaubewilligungBtn);

			if (!$button12->isClicked($this->instanceId)) {
				$baButtonMapper->handleAction($versandBaubewilligungBtn, $this->instanceId);
			}
		}
	}
}
