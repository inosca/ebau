<?php

class Buildingauthority_Bootstrap extends Zend_Application_Module_Bootstrap {
	protected function _initAutoloader() {
		$loader = new Zend_Loader_Autoloader_Resource(array(
			'basePath' => CONFIGURATION_PATH . '/Custom/modules/buildingauthority',
			'namespace' => 'Buildingauthority',
		));

		$loader->addResourceType('instanceresource', 'InstanceResource', 'InstanceResource');
		//$loader->addResourceType('action', 'Action', 'Action');
		$loader->addResourceType('data', 'Data', 'Data');
	}
}
