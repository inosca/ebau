<?php

class Zend_View_Helper_GetRole extends Zend_View_Helper_Abstract {

	private static $mapper = null;

	public static function mapper() {
		if (self::$mapper == null) {
			self::$mapper = new Application_Model_Mapper_Account_Role();
		}

		return self::$mapper;
	}

	public function getRole($roleID) {
		$role = self::mapper()->getRole($roleID);

		return $role->getName();
	}
}
