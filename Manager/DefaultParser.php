<?php

/**
 * Notification parser, default implementation.
 */
class Notification_Manager_DefaultParser extends Zend_Validate_Abstract {


	/**
	 * message templates - part of the Zend_Validate API
	 */
	protected $_messageTemplates = array(
		'unknownVars' => 'Unknown variables in template: %s',
		'parse'       => 'Parse error: %s',
	);

	public function parse($template, $variables) {
		$ret = [];

		foreach ($template as $key => $text) {
			$ret[$key] = $this->_doParse($text, $variables);
		}
		return $ret;
	}

	private function _doParse($text, $variables) {
		foreach ($variables as $key => $value) {
			$placeholder = '{{'.$key.'}}';
			$text = str_replace($placeholder, $value, $text);
		}
		return $text;
	}

	public function getTemplateHelpText($variables) {
		$tr = Zend_Registry::get('Zend_Translate');
		$introText = $tr->translate("Der Vorlagen-Inhalt wird bei einer Notifikation mit den folgenden Platzhaltern verarbeitet: %s");

		$placeholders = array_map(
			function($text) {
				return sprintf('{{%s}}', $text);
			},
			$variables
		);

		return sprintf(
			$introText,
			implode(', ', $placeholders)
		);
	}

	/**
	 * Check if the given template fragment is valid.
	 *
	 * Note this is part of the Zend_Validate API, but only validates a single
	 * template fragment, not the usual array structure
	 */
	public function isValid($template) {

		$this->_setValue($template);

		// Get the available placeholders, and generate a
		// bunch of "variables" to parse into the template
		$api = Notification_Manager_API::getInstance();
		$ph  = $api->getPlaceholderSource();
		$vars = array_combine(
			$ph->getAvailablePlaceholders(),
			$ph->getAvailablePlaceholders()
		);

		try {
			$parsed = $this->_doParse($template, $vars);
		}
		catch(Exception $e) {
			$this->setMessage($e->getMessage(), 'parse');
			$this->_error('parse');
			return false;
		}

		// Okay, so it parses, but let's check for unknown variables and
		// other curly-braces syntax that might hint at a broken template

		if (preg_match_all('/\{\{\w+\}\}/', $parsed, $unknownVars)) {
			$tr = Zend_Registry::get('Zend_Translate');
			$this->setMessages([
				'unknownVars' =>
				sprintf(
					$tr->translate("Unbekannte Variablen in der Vorlage: %s"),
					implode(', ', $unknownVars[0])
				)
			]);
			$this->_error('unknownVars');
			return false;
		}

		return true;
	}
}
