<?php

class Zend_View_Helper_GetAttachmentSection extends Zend_View_Helper_Abstract {

	private static $mapper = null;

	public static function mapper() {
		if (self::$mapper == null) {
			self::$mapper = new Documents_Model_Mapper_AttachmentSection();
		}

		return self::$mapper;
	}

	public function getAttachmentSection($attachmentSectionID) {
		$section = self::mapper()->getEntry($attachmentSectionID);

		return $section->name;
	}
}

