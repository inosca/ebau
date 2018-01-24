<?php

class Docgen_Data_Template_Form extends Camac_Form_Admin {

	/**
	 * Is editing mode
	 *
	 * @var           bool $isEdit
	 */
	protected $isEdit;

	/**
	 * 
	 */
	protected $fileElement;

	public function __construct($options, $isEdit) {
		$this->isEdit = $isEdit;
		parent::__construct($options);
	}

	public function init() {

		$this->addElement('text', 'name', array(
			'label' => $this->getTranslator()->translate('Name'),
			'class' => 'text',
			'required' => true,
		));


		$this->fileElement = $this->addElement('file', 'file', array(
			'label' => $this->getTranslator()->translate('Upload'),
			'class' => 'file',
			'required' => true,
			'validators' => array(
				'Extension' => new Zend_Validate_File_Extension(array('docx', 'zip'))
			)
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Docgen_Model_Data_Template $template) {
		$values = array();
		$values['name'] = $template->name;

		if ($template->type == Docgen_Model_Mapper_Template::TYPE_PDF) {
			$validator = new Zend_Validate_File_Extension(array('zip'));
			$this->getElement('file')->addValidator($validator);
		}
		else {
			$validator = new Zend_Validate_File_Extension(array('docx'));
			$this->getElement('file')->addValidator($validator);
		}

		parent::populate($values);
	}
}
