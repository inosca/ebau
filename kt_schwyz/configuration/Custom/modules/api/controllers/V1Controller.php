<?php

class Api_V1Controller extends Camac_Controller_Action {

	protected $instanceId;

	protected $instanceResourceId;

	public function __construct(
		Zend_Controller_Request_Abstract $request,
		Zend_Controller_Response_Abstract $response,
		array $invokeArgs = array()
	) {
		parent::__construct($request, $response, $invokeArgs);

		$this->questionTable = new Camac_Model_DbTable_Form_Question();
		$this->answerListTable = new Camac_Model_DbTable_Form_AnswerList();
		$this->answerTable = new Camac_Model_DbTable_Answer();
	}

	public function questionAction() {
		$ids = explode(",", $this->getRequest()->getParam("id"));
		$chapter = intval($this->getRequest()->getParam("chapter"));
		$item = intval($this->getRequest()->getParam("item"));
		$include = explode(",", $this->getRequest()->getParam("include"));
		$instanceId = intval($this->getRequest()->getParam('instance-id'));

		if (!Custom_UriUtils::validateArray($ids, function($id) {
			return is_numeric($id);
		})) {
			$this->_response->setHttpResponseCode(400);
			return $this->_helper->json("Missing or invalid parameter id");
		}

		if (!$chapter || !$item) {
			$this->_response->setHttpResponseCode(400);
			return $this->_helper->json("Missing or invalid parameter chapter or item");
		}

		$questions = $this->questionTable->find($ids)->toArray();
		$result = array("questions" => array_map(function($question) use ($chapter, $item) {
			$question['CHAPTER_ID'] = $chapter;
			$question['ITEM'] = $item;
			return $question;
		}, $questions));

		if (in_array("answerList", $include)) {
			$select = $this->answerListTable->select()->where('QUESTION_ID IN (?)', $ids);
			$answerList = $this->answerListTable->fetchAll($select)->toArray();
			$result["answerLists"] = $answerList;
		}

		if (in_array("answer", $include) && $instanceId) {
			$select = $this->answerTable->select()
				->where('QUESTION_ID IN (?)', $ids)
				->where('CHAPTER_ID = ?', $chapter)
				->where('ITEM = ?', $item)
				->where('INSTANCE_ID = ?', $instanceId);

			$answers = $this->answerTable->fetchAll($select)->toArray();
			$result["answers"] = array_map(function($answer) {
				$answer['ANSWER'] = self::normalizeList($answer['ANSWER']);
				return $answer;
			}, $answers);
		}

		return $this->_helper->json($result);
	}

	public function answerAction() {
		$instanceId = intval($this->getRequest()->getParam('instance-id'));
		if (!$instanceId || !is_numeric($instanceId)) {
			$this->_response->setHttpResponseCode(400);
			return $this->_helper->json("Missing or invalid parameter instance-id");
		}

		if ($this->_request->isPost()) {
			return $this->saveAnswer($instanceId);
		}

		$ids = self::filterNumeric(explode(",", $this->getRequest()->getParam("question-id")));

		if (empty($ids)) {
			$this->_response->setHttpResponseCode(400);
			return $this->_helper->json("Missing parameter question-id");
		}


		$select = $this->answerTable->select()
			->where('QUESTION_ID IN (?)', $ids)
			->where('INSTANCE_ID = ?', $instanceId);
		$answers = $this->answerTable->fetchAll($select)->toArray();

		$results = array_map(function($answer) {
			$answer['ANSWER'] = self::normalizeList($answer['ANSWER']);
			return $answer;
		}, $answers);

		return $this->_helper->json($results[0]);
	}

	private function saveAnswer($instanceId) {
		$data = Zend_Json::decode($this->getRequest()->getRawBody());

		$validate = function($entry) {
			return array_key_exists('QUESTION_ID', $entry)
				&& array_key_exists('ANSWER', $entry)
				&& is_numeric($entry['QUESTION_ID']);
		};

		if (!Custom_UriUtils::validateArray($data, $validate)) {
			$this->_response->setHttpResponseCode(400);
			return $this->_helper->json("Missing or invalid request body");
		}

		$mapper = new Camac_Model_Mapper_Answer();
		foreach ($data as $answer) {
			$answerObj = new Camac_Model_Data_Answer(
				$instanceId,
				$answer['QUESTION_ID'],
				$answer['CHAPTER_ID'],
				$answer['ITEM'],
				$answer['ANSWER']
			);
			if ($answer['ANSWER']) {
				$mapper->update($answerObj);
			}
			else {
				$mapper->delete($answerObj);
			}
		}

		return $this->_helper->json(true);
	}

	/**
	 * This function converts the ad-hoc string-based lists in the DB
	 * to actual PHP arrays. Example:
	 * "[\"I\",\"D\"]" => array("I", "D")
	 *
	 * (Is there an easier way to do this?)
	 */
	private static function normalizeList($str) {
		return substr($str, 0, 2) === '["' && substr($str, -2) === '"]'
			? explode(",", str_replace(array("[", "]", "\""), "", $str))
			: $str;
	}

	/**
	 * Filters a list for numeric contents
	 */
	private static function filterNumeric($list) {
		return array_filter($list, function ($entry) {
			return is_numeric($entry);
		});
	}

	/*
	private static function filterIdentifiers($identifiers, $prop) {
		return array_map(function($identifier) {
			return self::splitQuestionID($identifier)[$prop];
		}, $identifiers);
	}
	 */

	/**
	 * Splits a CAMAC question ID:
	 * "c2q12i1" => array("chapter" => 2, "question" => 12, "item" => 1)
	 */
	/*
	private static function splitQuestionID($identifier) {
		return array(
			"chapter" => substr($identifier, 1, strpos($identifier, "q")),
			"question" => substr($identifier, strpos($identifier, "q") + 1, strpos($identifier, "i")),
			"item" => substr($identifier, strpos($identifier, "i") + 1)
		);
	}*/
}
