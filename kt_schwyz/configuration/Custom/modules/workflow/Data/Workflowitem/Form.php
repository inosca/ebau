<?php

class Workflow_Data_WorkflowItem_Form extends Camac_Form_Admin {


	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());

		$this->addElement('text', 'name', array(
			'label' => $this->getTranslator()->translate('Name') . ' *',
			'class' => 'text',
			'required' => 'true',
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 255)
			)
		));

		$this->addElement('checkbox', 'automatical', array(
			'label' => $this->getTranslator()->translate('Automatical'),
			'class' => 'checkbox',
			'required' => 'true'
		));

		$this->addElement('checkbox', 'different_color', array(
			'label' => $this->getTranslator()->translate('Different color'),
			'class' => 'checkbox',
			'required' => 'true'
		));

		$this->addelement('multiCheckbox', 'roles', array(
			'label' => $this->getTranslator()->translate('Roles'),
			'class' => 'multicheckbox',
			'multiOptions' => $this->getRoles()
		));

		$this->addElement('select', 'workflowSectionID', array(
			'label' => $this->getTranslator()->translate('Workflow Section'),
			'class' => 'text',
			'required' => true,
			'multiOptions' => $this->getWorkflowSections()
		));

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));

		$this->initDisplayGroup();

	}

	public function populate(Workflow_Model_Data_WorkflowItem $workflow) {
		$values = array();
		$values['name'] = $workflow->name;
		$values['position'] = $workflow->position;
		$values['automatical'] = $workflow->automatical;
		$values['workflowSectionID'] = $workflow->workflowSectionID;

		$roleMapper = new Workflow_Model_Mapper_WorkflowRole();
		$roles = $roleMapper->getWorkflowItemRoles($workflow->workflowItemID);

		foreach ($roles as $role) {
			$values['roles'][] = $role->roleID;
		}

		return parent::populate($values);
	}

	public function getRoles() {
		$dbTable = new Camac_Model_DbTable_Account_Role();
		$rows = $dbTable->fetchAll($dbTable->select());

		$result = array();
		foreach ($rows as $row) {
			$result[$row->ROLE_ID] = $row->NAME;
		}

		return $result;
	}

	private function getWorkflowSections() {
		$mapper = new Workflow_Model_Mapper_WorkflowSection();
		$sections = $mapper->getAll();
		$result = array();
		foreach ($sections as $section) {
			$result[$section->workflowSectionID] = $section->name;
		}

		return $result;
	}
}
