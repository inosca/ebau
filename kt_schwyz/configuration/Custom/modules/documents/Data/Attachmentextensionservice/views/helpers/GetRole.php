<?php

class Zend_View_Helper_GetService extends Zend_View_Helper_Abstract {

	private static $mapper = null;

	public static function mapper() {
		if (self::$mapper == null) {
			self::$mapper = new Application_Model_Mapper_Account_Service();
		}

		return self::$mapper;
	}

	public function getService($serviceID) {
		$service = self::mapper()->getService($serviceID);

		return $service->getName();
	}
}
