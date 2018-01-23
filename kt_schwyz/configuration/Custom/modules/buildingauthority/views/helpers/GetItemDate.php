<?php

class Buildingauthority_View_Helper_GetItemDate extends Zend_View_Helper_Abstract {

	public function getItemDate($workflowItem, $instanceId, $group = 1) {
		$entries = $workflowItem->getEntries($instanceId);
		if (count($entries) == 0) {
			return null;
		}

		$result = array_filter(
			$entries,
			function($workflowEntry) use($group) {
				return (int)$workflowEntry->group === $group;
			}
		);

		return count($result) ? array_shift($result)->workflowDate : null;
	}
}
