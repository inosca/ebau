<?php
class Docgen_Data_Templateclass_Form extends Camac_Form_Admin {
	/**
	 * If the type is fixed (edit mode)
	 *
	 * @var           bool $fixedType
	 */
	protected $fixedType;
	

	public function __construct($options = null, $fixedType = false) {
		$this->fixedType = $fixedType;

		parent::__construct($options);
	}

	public function init() {
		$this->addElement('text', 'name', array(
			'label' => $this->getTranslator()->translate('Name'),
			'class' => 'text',
			'required' => true
		));

		if (!$this->fixedType) {
			$this->addElement('radio', 'type', array(
				'label'        => $this->getTranslator()->translate('Type'),
				'class'        => 'radio',
				'required'     => true,
				'multiOptions' => array(
					Docgen_Model_Mapper_Templateclass::TYPE_DOCX => 'DocX',
					Docgen_Model_Mapper_TemplateClass::TYPE_PDF  => 'PDF'
				)
			));
		}
	
		$this->addElement('file', 'file', array(
			'label' => $this->getTranslator()->translate('Upload'),
			'class' => 'file',
			'required' => true,
			'validators' => array(
				'Extension' => new Zend_Validate_File_Extension(array('php'))
			)
		));

		$this->addelement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Docgen_Model_Data_Templateclass $templateClass) {
		$values = array();
		$values['name'] = $templateClass->name;

		return parent::populate($values);
	}
}
