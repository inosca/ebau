<?php


/**
 * Action workflow data model.
 *
 * @package Workflow\Action\Workflow
 */
class Workflow_Action_Workflow_Data extends Camac_Model_Data_Resource_Action {

	/**
	 * Only first and newest date
	 */
	const MULTI_VALUE_RANGE   = 0;

	/**
	 * List of all dates
	 */
	const MULTI_VALUE_APPEND  = 1;

	/**
	 * Only the newest date (update)
	 */
	const MULTI_VALUE_REPLACE = 2;

	/**
	 * Only the first date,
	 * additional entries are ignored
	 */
	const MULTI_VALUE_IGNORE  = 3;

	protected $workflowItemID;

	protected $multiValue;

	/**
	 * Constructor.
	 *
	 * @param int $actionId
	 * @param string $availableActionId
	 * @param int $buttonId
	 * @param string $name
	 * @param string $description
	 * @param string $confirmMessage
	 * @param string $errorMessage
	 * @param bool $executeAlways
	 * @param int $sort
	 * @param string $query
	 * @return void
	 */
	public function __construct($actionId, $availableActionId, $buttonId, $name, $description, $confirmMessage, $errorMessage, $executeAlways, $sort, $workflowItemID, $multiValue) {

		parent::__construct($actionId, $availableActionId, $buttonId, $name, $description, $confirmMessage, $errorMessage, $executeAlways, $sort);

		$this->workflowItemID = $workflowItemID;
		$this->setMultiValue($multiValue);
	}

	public function getWorkflowItemID() {
		return $this->workflowItemID;
	}

	public function getMultiValue() {
		return (int)$this->multiValue;
	}

	public function setMultiValue($multiValue) {
		$multiValue = (int)$multiValue;

		$possibleValues = array(
			self::MULTI_VALUE_RANGE,
			self::MULTI_VALUE_APPEND,
			self::MULTI_VALUE_REPLACE,
			self::MULTI_VALUE_IGNORE
		);

		if (!in_array($multiValue, $possibleValues)) {
			throw new InvalidArgumentException(
				'Invalid workflow multivalue value'
			);
		}

		$this->multiValue = $multiValue;
	}
}
