<?php
/**
 * Validates an array of dates, as needed on the workflow form.
 */
class Workflow_Data_DateValidator extends Zend_Validate_Abstract {
	const FLOAT = 'float';

	protected $_messageTemplates = array(
		self::FLOAT => "'%value%' ist kein gültiges Datum."
	);

	public function isValid($values) {
		$this->_setValue($values);

		foreach($values as $value) {
			Zend_Registry::get('log')->log('checking' . $value, Zend_Log::DEBUG);

			date_create_from_format('d.m.y', $value);
			$date_errors = DateTime::getLastErrors();

			if($value != null && ($date_errors['warning_count'] + $date_errors['error_count'] > 0)) {
				Zend_Registry::get('log')->log('invalid!', Zend_Log::DEBUG);
				$this->_error(self::FLOAT);
				return false;
			}
		}

		return true;
	}
}
