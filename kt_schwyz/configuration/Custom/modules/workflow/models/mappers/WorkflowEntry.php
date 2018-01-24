<?php


class Workflow_Model_Mapper_WorkflowEntry {


	/**
	 * Model
	 *
	 * @var           Documents_Model_DbTable_Attachments  $model
	 */
	protected $model;

	public function __construct() {
		$this->model = new Workflow_Model_DbTable_WorkflowEntry();
	}


	public function save(Workflow_Model_Data_WorkflowEntry $workflowEntry) {
		$data = array(
			'INSTANCE_ID'      => $workflowEntry->instanceID,
			'WORKFLOW_DATE'    => Camac_Date::getDbStringFromDateTime($workflowEntry->workflowDate),
			'WORKFLOW_ITEM_ID' => $workflowEntry->workflowItemID,
			'GROUP'            => $workflowEntry->group
		);

		return $this->model->insert($data);
	}

	public function updateDate($workflowEntryID, $date, $group = null) {
		$data = array(
			'WORKFLOW_DATE' => Camac_Date::getDbStringFromDateTime($date)
		);

		if ($group !== null) {
			$data['GROUP'] = $group;
		}

		$this->model->update($data, array('WORKFLOW_ENTRY_ID = ?' => $workflowEntryID));
	}

	public function getEntries($instanceID, $workflowItemID) {
		$select = $this->model->select()
			->where('"INSTANCE_ID" = ?', $instanceID)
			->where('"WORKFLOW_ITEM_ID" = ?', $workflowItemID)
			->order(array('WORKFLOW_DATE ASC'));

		$rows = $this->model->fetchAll($select);

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Workflow_Model_Data_WorkflowEntry(
				$row->WORKFLOW_ENTRY_ID,
				$row->INSTANCE_ID,
				Camac_Date::getDateTimeFromDbString($row->WORKFLOW_DATE),
				$row->WORKFLOW_ITEM_ID,
				$row->GROUP
			);
		}

		return $results;
	}

	public function getEntry($workflowEntryID) {
		$result = NULL;
		$row = $this->model->find($workflowEntryID)->current();
		if ($row) {
			$result = new Workflow_Model_Data_WorkflowEntry(
				$row->WORKFLOW_ENTRY_ID,
				$row->INSTANCE_ID,
				Camac_Date::getDateTimeFromDbString($row->WORKFLOW_DATE),
				$row->WORKFLOW_ITEM_ID,
				$row->GROUP
			);
		}

		return $result;
	}

	public function getEntryByUniqueKey($instanceId, $workflowItemId, $group) {
		$result = null;
		$select = $this->model->select()
			->where('INSTANCE_ID = ?', $instanceId)
			->where('WORKFLOW_ITEM_ID = ?', $workflowItemId)
			->where('"GROUP" = ?', $group);

		$row = $this->model->fetchRow($select);
		if ($row) {
			$result = new Workflow_Model_Data_WorkflowEntry(
				$row->WORKFLOW_ENTRY_ID,
				$row->INSTANCE_ID,
				Camac_Date::getDateTimeFromDbString($row->WORKFLOW_DATE),
				$row->WORKFLOW_ITEM_ID,
				$row->GROUP
			);
		}

		return $result;
	}

	public function getMaxGroupCount($instanceId) {
		$select = $this->model->select()
			->from($this->model, 'MAX("GROUP") AS max_group')
			->where('INSTANCE_ID = ?', $instanceId);
		return (int)$this->model->fetchRow($select)->max_group;
	}

	public function delete($workflowEntryID) {
		$this->model->delete(array('WORKFLOW_ENTRY_ID = ?' => $workflowEntryID));
	}

	public function makeEntry(
		$instanceId,
		$workflowItemId,
		$multiValue,
		DateTime $date = null,
		$group = null
	) {
		$workflowEntry = null;
		$entries       = $this->getEntries($instanceId, $workflowItemId);

		if ($date === null) {
			$date = new DateTime('now');
		}

		// In RANGE mode we only want the first and newest entry (max 2), so delete
		// one if there is already more than one entry.
		if (
			$multiValue === Workflow_Action_Workflow_Data::MULTI_VALUE_RANGE &&
			count($entries) > 1
		) {
			$lastEntry = array_pop($entries);
			$this->delete($lastEntry->workflowEntryID);
		}

		// In APPEND and RANGE mode or if there is no entry, create and save a new one
		if (
			$multiValue === Workflow_Action_Workflow_Data::MULTI_VALUE_APPEND ||
			$multiValue === Workflow_Action_Workflow_Data::MULTI_VALUE_RANGE ||
			count($entries) === 0
		) {
			$workflowEntry = new Workflow_Model_Data_WorkflowEntry(
				null,
				$instanceId,
				$date,
				$workflowItemId,
				$group === null ? count($entries) + 1 : $group
			);

			$this->save($workflowEntry);
		}

		// In REPLACE mode just update the current date
		if (
			$multiValue === Workflow_Action_Workflow_Data::MULTI_VALUE_REPLACE &&
			count($entries) > 0
		) {
			$workflowEntry = array_shift($entries);
			$this->updateDate(
				$workflowEntry->workflowEntryID,
				$date,
				$group !== null ? $group : null
			);
		}

		return $workflowEntry;
	}
}
