<?php

class Zend_View_Helper_GetWorkflowSectionName extends Zend_View_Helper_Abstract {

	public function getWorkflowSectionName($id) {
		$mapper = new Workflow_Model_Mapper_WorkflowSection();
		$entry = $mapper->getEntry($id);
		return $entry ? $entry->name : '';
	}
}
