<?php

class Buildingauthority_View_Helper_IsItemDisabled extends Zend_View_Helper_Abstract {

	public function isItemDisabled($workflowItemId, $instanceId, $group) {
		$baItemDisMapper = new Buildingauthority_Model_Mapper_BuildingAuthorityItemDis();
		return $baItemDisMapper->isDisabled($workflowItemId, $instanceId, $group);
	}
}
