<?php

require_once(APPLICATION_PATH . '/../library/tbs/tbs_class.php');
require_once(APPLICATION_PATH . '/../library/tbs/tbs_plugin_opentbs.php');


abstract class Docgen_TemplateController_DocxController extends Docgen_TemplateController_TemplateControllerAbstract {

	/**
	 * TBS instance
	 *
	 * @var           clsTinyButStrong $tbs
	 */
	protected $tbs;

	public function __construct() {
		parent::__construct();


		$this->tbs = new clsTinyButStrong();
		$this->tbs->plugin(TBS_INSTALL, OPENTBS_PLUGIN);
	}

	/**
	 * Render the document and return it
	 *
	 * @param         string  $template The template location
	 * @returns       binary The document
	 */
	public function render($template) {
		$this->tbs->LoadTemplate($template, OPENTBS_ALREADY_UTF8);

		foreach ($this->getMergeBlockData() as $block => $blockData) {
			$this->tbs->MergeBlock($block, $blockData);
		}

		$data = array_merge(
			$this->questionTags,
			$this->getIndividualTags()
		);

		$this->tbs->VarRef = $data;
		$this->tbs->Show(OPENTBS_STRING);
		return $this->tbs->Source;
	}

	/**
	 * Overwrite this if you want to add merge blocks
	 *
	 * Return an array of the format
	 * array(
	 *     'blockName' => array(
	 *         'tagName' => 'data'
	 *      )
	 * )
	 */
	protected function getMergeBlockData() {
		return array();
	}

}
