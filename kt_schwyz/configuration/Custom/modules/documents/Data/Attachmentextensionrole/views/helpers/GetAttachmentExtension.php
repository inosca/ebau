<?php

class Zend_View_Helper_GetAttachmentExtension extends Zend_View_Helper_Abstract {

	private static $mapper = null;

	public static function mapper() {
		if (self::$mapper == null) {
			self::$mapper = new Documents_Model_Mapper_AttachmentExtension();
		}

		return self::$mapper;
	}

	public function getAttachmentExtension($attachmentExtensionID) {
		$extension = self::mapper()->getEntry($attachmentExtensionID);

		return $extension->name;
	}
}

