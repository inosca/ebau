<?php

class Core_Resource_Simplelist_Data extends Camac_Model_Data_Resource_Resource {

	public $instanceStates;

	public function __construct($resourceId, $availableResourceId, $name, $description, $template, $class, $hidden, $sort, $instanceStates) {

		$this->instanceStates = $instanceStates;

		parent::__construct($resourceId, $availableResourceId, $name, $description, $template, $class, $hidden, $sort);

	}
}
