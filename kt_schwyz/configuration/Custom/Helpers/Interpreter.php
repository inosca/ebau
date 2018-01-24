<?php

/**
 * Custom extension of the Interpreter helper, ready to be modified at will.
 *
 * @author Alessandro Gaia <alessandro.gaia@blackpoints.ch>
 */

/**
 *
 * @package Custom\Helper
 */
class Custom_Helper_Interpreter extends Camac_Interpreter_Interpreter {

	// This is an example of how the local function to retrieve a tag's value should be implemented.

	/**
	 * Helper function, retrieves the value corresponding to the [EXAMPLE_1] tag.
	 *
	 * @return string|null The value corresponding to the [EXAMPLE_1] tag, or null if not found.
	 */
	//protected function evaluateExample1() {
	//	// execute value retrieval logic here...
	//	return 'example 1 value';
	//}

	/**
	 * Constructor
	 *
	 */
	public function __construct() {
		parent::__construct();

		// This array should be populated with pairs representing tags => function_names
		// to retrieve custom data ftom the DB using the interpreter.
		//
		// This example makes the interpreter to match all the tags "[EXAMPLE_1]" and use
		// the local function evaluateExample1() to retrieve the data.
		//
		// $this->customTags = array('[EXAMPLE_1]' => 'evaluateExample1');

	}

	/**
	 * Decodes the input
	 *
	 * Overwrites parent decode function and ads custom tag decode.
	 *
	 * @author        Adrian Wittwer <adrian.wittwer@adfinis-sygroup.ch>
	 * @param         string $input
	 * @param         bool $backendQueryEvaluation
	 * @return        string
	 */
	protected function decode($input, $backendQueryEvaluation = false) {
		$input = $this->convertCustomTag($input);
		$input = $this->convertURLTag($input);
		$input = $this->convertPortalUser($input);
		$input = $this->convertInstanceLocation($input);
		$input = $this->convertWorkflowDate($input);
		$input = $this->convertCurrentDate($input);

		return parent::decode($input, $backendQueryEvaluation);
	}

	/**
	 * Entry point function for the helper. Loads the custom tags and then calls the
	 * decode function of the superclass.
	 *
	 * @param string $input The text that may contain tags to decode.
	 * @param $backendQueryEvaluation Set the NULL value as text during evaluation
	 * @return string The input text, with all the recognized tags replaced by their corresponding value.
	 */
	public function direct($input, $backendQueryEvaluation = false) {
		return $this->decode($input, $backendQueryEvaluation);

	}

	/**
	 * Converts custom question tags into answer
	 *
	 * @author        Adrian Wittwer <adrian.wittwer@adfinis-sygroup.ch>
	 * @param         string $input
	 * @return        string
	 */
	private function convertCustomTag($input) {
		// Check if even a custom tag exists, otherwise skip all this (performance)
		if (strpos($input, '[@') === false) {
			return $input;
		}

		$matches = array();
		$searchRegex = '/\[@c(\d+)q(\d+)i(\d+)\]/'; // [@c2q1i1]
		$answerGateway = new Application_Model_Mapper_AnswerGateway();

		preg_match_all($searchRegex, $input, $matches);

		$tags      = $matches[0];
		$chapters  = $matches[1];
		$questions = $matches[2];
		$item      = $matches[3];

		foreach($tags as $key => $tag) {
			$answers = Custom_UriUtils::getMultianswers(
				Camac_Nest_Pigeon::getInstance()->instanceId,
				$questions[$key],
				$chapters[$key],
				$item[$key]
			);

			if (count($answers) > 0) {
				$answerString = implode(', ', $answers);
			}
			else {
				$answer = $answerGateway->getAnswer(
					Camac_Nest_Pigeon::getInstance()->instanceId,
					$questions[$key],
					$chapters[$key],
					$item[$key]
				);

				$answerString = $answer === null ? null : $answer->getAnswer();
			}

			if ($answerString === null) {
				$answerString = "";
			}

			$input = str_replace($tag, $answerString, $input);
		}

		return $input;
	}

	/**
	 * Converts URL tags
	 *
	 * @author        Adrian Wittwer <adrian.wittwer@adfinis-sygroup.ch>
	 * @param         string $input
	 * @return        string
	 */
	private function convertURLTag($input) {
		if (strpos($input, '[URL_FORM_ID]') !== false) {
			$formID = Zend_Controller_Front::getInstance()->getRequest()->getParam('form-id');
			if (!$formID) {
				$instanceId = Camac_Nest_Pigeon::getInstance()->instanceId;
				$mapper = new Application_Model_Mapper_Instance();
				$instance = $mapper->getInstance($instanceId);
				if ($instance) {
					$formID = $instance->getFormId();
				}
			}
			$input = str_replace('[URL_FORM_ID]', $formID, $input);
		}

		return $input;
	}

	/**
	 * Converts portal user ID
	 *
	 * @author        Christian Zosel <christian.zosel@adfinis-sygroup.ch>
	 * @param         string $input
	 * @return        string
	 */
	private function convertPortalUser($input) {
		if (strpos($input, '[PORTAL_USER]') !== false) {
			$session = new Zend_Session_Namespace('portal');
			$input = str_replace('[PORTAL_USER]', $session->id, $input);
		}

		return $input;
	}

	/**
	 * Convert INSTANCE_LOCATION
	 *
	 * @param string $input
	 * @return string
	 */
	private function convertInstanceLocation($input) {
		if (strpos($input, '[INSTANCE_LOCATION]') !== false) {
			$instanceId = Camac_Nest_Pigeon::getInstance()->instanceId;
			$mapper = new Application_Model_Mapper_InstanceLocation();
			$instanceLocations = $mapper->getInstanceLocations($instanceId);

			// There is no location mapper, so get it directly
			$dbAdapter = Zend_Db_Table::getDefaultAdapter();
			$locations = $dbAdapter->fetchAll(
				$dbAdapter->select()
					->from('LOCATION')
					->where('LOCATION_ID = ?', $instanceLocations[0]->getLocationId())
			);

			// we only ever assign one location to an instance
			$location = array_pop($locations);

			$input = str_replace('[INSTANCE_LOCATION]', $location['NAME'], $input);
		}

		return $input;
	}

	/**
	 * Convert a date from the workflow [WORKFLOW_<ID>]
	 *
	 * @param string $input
	 * @return string
	 */
	private function convertWorkflowDate($input) {
		if (preg_match("/\[WORKFLOW_(\d)+\]/", $input, $matches)) {
			$id = $matches[1];
			$instanceId = Camac_Nest_Pigeon::getInstance()->instanceId;

			$mapper = new Workflow_Model_Mapper_WorkflowEntry();
			$entries = $mapper->getEntries($instanceId, $id);
			// let's take the first entry, makes more sense where
			// we want to use this
			if (count($entries)) {
				$first_entry = array_shift($entries);
				if ($first_entry) {
					$date = $first_entry->workflowDate->format('d.m.Y');

					preg_replace("/\[WORKFLOW_$id\]/", $date, $input);
				}
			}
		}

		return $input;
	}

	/**
	 * Convert current date from [DATE]
	 *
	 * @param string $input
	 * @return string
	 */
	private function convertCurrentDate($input) {
		if (strpos($input, '[DATE]') !== false) {
			$date = Camac_Date::getStringFromDateTime(
				Zend_Registry::get('config')->date->application->phpFormat,
				new DateTime('now')
			);
			$input = str_replace('[DATE]', $date, $input);
		}

		return $input;
	}
}
