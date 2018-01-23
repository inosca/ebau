<?php
/**
 * Validates an array of dates, as needed in the diffrent sections
 */
class Buildingauthority_Data_DateValidator extends Zend_Validate_Abstract {
	const FLOAT = 'float';

	protected $_messageTemplates = array(
		self::FLOAT => "'%value%' ist kein gültiges Datum."
	);

	public function isValid($value) {
		if (!is_array($value)) {
			$value = array($value);
		}

		foreach ($value as $singleValue) {
			if (strlen($singleValue) == 0) {
				continue;
			}

			$this->_setValue($singleValue);

			date_create_from_format('d.m.y', $singleValue);
			$date_errors = DateTime::getLastErrors();

			if($singleValue != null && ($date_errors['warning_count'] + $date_errors['error_count'] > 0)) {
				$this->_error(self::FLOAT);
				return false;
			}
		}

		return true;
	}
}
