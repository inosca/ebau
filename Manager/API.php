<?php

class Notification_Manager_API {
	private static $_instance;
	private $_moduleCache;

	private $recipientTypes = [];
	private $processors     = [];


	public static function getInstance() {
		if (is_null(self::$_instance)) {
			self::$_instance = new self();
		}
		return self::$_instance;
	}

	private function __construct() {
		foreach($this->modules() as $moduleConfig) {
			if ($moduleConfig->notification_processors) {
				foreach ($moduleConfig->notification_processors as $proc) {
					$obj = new $proc;
					if (!$obj instanceof Notification_Manager_ProcessorInterface) {
						throw new Exception("Processor class $proc does not implement required interface");
					}
					$this->processors[] = new $obj;
				}
			}
			if ($moduleConfig->notification_recipients) {
				foreach ($moduleConfig->notification_recipients as $rec) {
					$obj = new $rec;
					if (!$obj instanceof Notification_Manager_RecipientTypeInterface) {
						throw new Exception("class $rec does not implement required interface");
					}
					$this->recipientTypes[] = $obj;
				}
			}
		}

		// Get per-project recipient definitions as well
		$config = Zend_Registry::get('config');
		if ($config->module->notification->recipients) {
			foreach($config->module->notification->recipients as $recipient) {
				$obj = new $recipient;
				if (!$obj instanceof Notification_Manager_RecipientTypeInterface) {
					throw new Exception("class $recipient does not implement required interface");
				}
				$this->recipientTypes[] = $obj;
			}
		}

		usort($this->processors,     [$this, '_sort']);
		usort($this->recipientTypes, [$this, '_sort']);
	}

	private function _sort($a, $b) {
		return $a->getTranslatedName() <=> $b->getTranslatedName();
	}

	public function getRecipientTypes() {
		return $this->recipientTypes;
	}

	public function getProcessors() {
		return $this->processors;
	}

	public function getParser() {
		try {
			$class = $this->getConfig()->parser;
			if (class_exists($class)) {
				return new $class;
			}
		}
		catch (Exception $e) {
			$log = Zend_Registry::get('log');
			$log->log(
				Camac_Utility::formatError($e->getMessage()),
				Zend_Log::CRIT
			);
		}
		return new Notification_Manager_DefaultParser;
	}
	public function getPlaceholderSource() {
		$sourceClass = $this->getConfig()->placeholder_source;
		if (class_exists($sourceClass)) {
			return new $sourceClass;
		}
		else {
			$log = Zend_Registry::get('log');
			$log->log(
				Camac_Utility::formatError("Placeholder source calss not found, using default: $sourceClass"),
				Zend_Log::CRIT
			);
		}
		return new Notification_Manager_DefaultPlaceholderSource();
	}

	/**
	 * Return the notification module config from the application.ini
	 */
	public function getConfig() {
		$config = Zend_Registry::get('config');
		return $config->module->notification;
	}

	/**
	 * Returns template help text from the parser, with information about the
	 * available placeholders.
	 */
	public function getTemplateHelpText() {
		$ph = $this->getPlaceholderSource();
		$parser = $this->getParser();

		return $parser->getTemplateHelpText($ph->getAvailablePlaceholders());
	}

	/**
	 * All-in-one function to parse a notification template for a
	 * given instance / recipient / template combination.
	 */
	public function parse($instanceId, $recipient, $template) {
		$placeholders = $this->getPlaceholderSource();
		$parser       = $this->getParser($template);

		$variables = $placeholders->getPlaceholders($instanceId, $recipient);

		return $parser->parse($template, $variables);
	}

	private function modules() {
		if ($this->_moduleCache) {
			return $this->_moduleCache;
		}

		// This code is copied from Admin_Module_ModuleController::indexAction.
		$modules = array();

		$files = scandir(CONFIGURATION_PATH . '/Custom/modules');
		foreach ($files as $file) {

			if (is_dir(CONFIGURATION_PATH . '/Custom/modules/' . $file) && $file != '.' && $file != '..') {
				if (file_exists(CONFIGURATION_PATH . '/Custom/modules/' . $file . '/configs/module.ini')) {
					$module = new Zend_Config_Ini(CONFIGURATION_PATH . '/Custom/modules/' . $file . '/configs/module.ini', APPLICATION_ENV, array('allowModifications' => true));
					$module->merge(new Zend_Config(array('directory' => $file)));
					$module->setReadOnly();
					$modules[] = $module;
				}
			}
		}
		$this->_moduleCache = $modules;
		return $modules;
	}
}
