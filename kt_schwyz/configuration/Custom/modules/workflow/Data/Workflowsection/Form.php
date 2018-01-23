<?php

class Workflow_Data_Workflowsection_Form extends Camac_Form_Admin {

	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('text', 'name', array(
			'label'      => $this->getTranslator()->translate('Name') . ' *',
			'class'      => 'text',
			'required'   => 'true',
			'secure'     => true,
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 60)
			)
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();
	}

	public function populate(Workflow_Model_Data_WorkflowSection $section) {
		return parent::populate(array(
			'name' => $section->name,
			'sort' => $section->sort
		));
	}
}
