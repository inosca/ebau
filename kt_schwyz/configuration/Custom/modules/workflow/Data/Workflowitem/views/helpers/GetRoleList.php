<?php

class Zend_View_Helper_GetRoleList extends Zend_View_Helper_Abstract {

	public function getRoleList($workflow) {

		$workflowRoleMapper = new Workflow_Model_Mapper_WorkflowRole();
		$roles = $workflowRoleMapper->getWorkflowItemRoles($workflow->workflowItemID);

		$roleMapper = new Application_Model_Mapper_Account_Role();
		$result = array();

		foreach ($roles as $role) {
			$result[] = $roleMapper->getRole($role->roleID)->getName();
		}

		return join(', ', $result);

	}
}
