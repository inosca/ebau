<?php

abstract class Docgen_TemplateController_TemplateControllerAbstract {

	/**
	 * Questiontags
	 *
	 * @var           $questiontags = array(tagname => value);
	 */
	protected $questionTags;

	/**
	 * Current instance
	 *
	 * @var           Camac_Model_Data_Instance $instance
	 */
	protected $instance;
	
	/**
	 * The form of the instance
	 *
	 * @var           Camac_Model_Data_Form $form
	 */
	protected $form;
	

	public function __construct() {
		$this->questionTags = array();

		$instanceMapper = new Application_Model_Mapper_Instance();
		$formMapper     = new Application_Model_Mapper_Form_Form();

		$this->instanceId = Camac_Nest_Pigeon::getInstance()->instanceId;
		$this->instance   = $instanceMapper->getInstance($this->instanceId);
		$formId           = $this->instance->getFormId();
		$this->form       = $formMapper->getForm($formId);

		$this->constructQuestiontags();
	}

	/**
	 * Construct all tags of the available questions
	 *
	 * This provides all the questions and their answer to the document
	 * renderer
	 */
	protected function constructQuestionTags() {
		$answerGateway = new Application_Model_Mapper_AnswerGateway();
		$questionMapper = new Application_Model_Mapper_Form_Question();
		
		foreach ($this->form->getPages() as $page) {
			foreach ($page->getChapters($this->form->getFormId()) as $chapter) {

				foreach ($chapter->getQuestions($this->form->getFormId(), $page->getPageId()) as $question) {
					$chapterId  = intval($chapter->getChapterId());
					$questionId = intval($question->getQuestionId());
					$itemId     = 1;

					$tagName = sprintf("c%dq%di%d",
						$chapterId, $questionId, $itemId
					);

					$question = $questionMapper->getQuestion($questionId);
					if (in_array($question->getQuestionTypeId(), array(4, 7))) {
						$multiAnswer = Custom_UriUtils::getMultianswers(
							$this->instanceId,
							$questionId,
							$chapterId,
							$itemId
						);
						$this->questionTags[$tagName] = $multiAnswer;
					}
					else {
						$answer = $answerGateway->getAnswer(
							$this->instanceId,
							$questionId,
							$chapterId,
							$itemId
						);

						if ($answer) {
							$this->questionTags[$tagName] = $answer->getAnswer();
						}
						else {
							$this->questionTags[$tagName] = "";
						}
					}
				}
			}
		}
	}

	/**
	 * Return available tag names
	 *
	 * Return a list of tag names that are available from the controller
	 */
	public function getAvailableTags() {
		$individualTags = $this->getTagNames();
		$questionTags   = $this->questionTags;

		return array_merge(
			array_keys($individualTags),
			array_keys($questionTags)
		);
	}

	/**
	 * Render the document and return it
	 *
	 * @param         string $template The path to the template
	 */ 
	public abstract function render($template);

	/**
	 * Function to return individual tags
	 *
	 * This function should be implemented by the final
	 * template controller. It returns 
	 */
	protected abstract function getIndividualTags();

	/**
	 * Return a list of the tag names that are provided by the sub class
	 */
	protected abstract function getTagNames();

}
