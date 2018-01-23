<?php

class Docgen_Action_Docx_Form extends Admin_Form_Resource_Action {
	public function init() {
		parent::init();

		$templateclassMapper = new Docgen_Model_Mapper_Templateclass();
		$items = $templateclassMapper->getTemplateClasses(Docgen_Model_Mapper_Templateclass::TYPE_DOCX);

		$templateclassItems = array();
		foreach ($items as $item) {
			$templateclassItems[$item->docgenTemplateclassId] = $item->name;
		}

		$this->addElement('select', 'docx_template_class_id', array(
			'label' => $this->getTranslator()->translate('Docx document class file'),
			'class' => 'select',
			'multiOptions' => $templateclassItems,
		));

		$templateMapper = new Docgen_Model_Mapper_Template();
		$items = $templateMapper->getTemplates(Docgen_Model_Mapper_Template::TYPE_DOCX);

		$templateItems = array();
		foreach ($items as $item) {
			$templateItems[$item->docgenTemplateId] = $item->name;
		}

		$this->addElement('select', 'docx_template_id', array(
			'label'        => $this->getTranslator()->translate('Docx document template file'),
			'class'        => 'select',
			'multiOptions' => $templateItems,
		));
	}

	public function populate(Camac_Model_Data_Resource_Action $action) {
		$values = array();
		$values['docx_template_class_id'] = $action->getTemplateclassId();
		$values['docx_template_id'] = $action->getTemplateId();

		return parent::populate($values, $action);
	}
}
