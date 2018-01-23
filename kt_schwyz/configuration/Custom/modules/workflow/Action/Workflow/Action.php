<?php


class Workflow_Action_Workflow_Action extends Camac_Action_Action {

	public function handleAction($previousSuccess) {
		$action = $this->getResourceAction();

		$success = $previousSuccess;
		if ($action->isAlwaysExecutable() || $previousSuccess) {
			$result = false;

			$workflowEntryMapper = new Workflow_Model_Mapper_WorkflowEntry();
			$workflowActionMapper = new Workflow_Action_Workflow_Mapper();
			$workflowAction       = $workflowActionMapper->getWorkflowAction($action->getActionId());
			$workflowItemID       = $workflowAction->getWorkflowItemID();
			$multiValue           = $workflowAction->getMultiValue();

			$pigeon = Camac_Nest_Pigeon::getInstance();
			$instanceID = $pigeon->instanceId;

			$workflowEntryMapper->makeEntry(
				$instanceID,
				$workflowItemID,
				$multiValue
			);

			$result = true;
		}
		$success = $previousSuccess && $result;

		return parent::handleAction($success);
	}
}
