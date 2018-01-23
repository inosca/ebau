<?php

class Portal_Bootstrap extends Zend_Application_Module_Bootstrap {
	protected function _initAutoloader() {
		$loader = new Zend_Loader_Autoloader_Resource(array(
			'basePath' => CONFIGURATION_PATH . '/Custom/modules/portal',
			'namespace' => 'Portal',
		));
		
		$loader->addResourceType('resource', 'Resource', 'Resource');

	}
}
