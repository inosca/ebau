<?php

class Notification_Bootstrap extends Zend_Application_Module_Bootstrap {
	protected function _initAutoloader() {
		$loader = new Zend_Loader_Autoloader_Resource(array(
			'basePath' => CONFIGURATION_PATH . '/Custom/modules/notification',
			'namespace' => 'Notification',
		));
		$loader->addResourceType('action',    'Action',    'Action');
		$loader->addResourceType('data',      'Data',      'Data');
		$loader->addResourceType('manager',   'Manager',   'Manager');
		$loader->addResourceType('processor', 'Processor', 'Processor');
	}

}
