<?php

class Core_Resource_Simplelist_Form extends Admin_Form_Resource_Resource {

	public function init() {
		parent::init();

		// Retrieve all the states
		$instanceStateMapper = new Admin_Model_Mapper_Resource_InstanceState();
		$options = $instanceStateMapper->getInstanceStates();

		$multiOptions = array();
		foreach ($options as $option) {
			$multiOptions[$option->getInstanceStateId()] = $option->getName();
		}
		Zend_Registry::get('log')->log(print_r($multiOptions, true), Zend_Log::DEBUG);

		$this->addElement('multiCheckbox', 'instanceStates', array(
			'label' => 'Instance state',
			'multiOptions' => $multiOptions
		));
	}

	public function populate(Core_Resource_Simplelist_Data $resource) {

		$values = array();
		if ($resource->instanceStates) {
			$values['instanceStates'] = explode(",", $resource->instanceStates);
		}

		return parent::populate($values, $resource);
	}
}

