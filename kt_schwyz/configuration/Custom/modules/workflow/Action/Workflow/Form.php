<?php


/**
 * Action workflow form.
 *
 * @package Workflow\Action\Workflow
 */
class Workflow_Action_Workflow_Form extends Admin_Form_Resource_Action {

	/**
	 * Inizializes the form.
	 *
	 * @return void
	 */
	public function init() {

		parent::init();


		$workflowItemMapper = new Workflow_Model_Mapper_WorkflowItem();
		$items = $workflowItemMapper->getAll();

		$workflowItems = array();
		foreach ($items as $item) {
			$workflowItems[$item->workflowItemID] = $item->name;
		}

		$this->addElement('select', 'workflow_id', array(
			'label' => $this->getTranslator()->translate('Workflow item'),
			'class' => 'select',
			'multiOptions' => $workflowItems,
		));

		$this->addElement('radio', 'multi_value', array(
			'label' => $this->getTranslator()->translate('Multiple workflow values'),
			'class' => 'radio',
			'required' => true,
			'multiOptions' => array(
				Workflow_Action_Workflow_Data::MULTI_VALUE_RANGE   => $this->getTranslator()->translate('Range'),
				Workflow_Action_Workflow_Data::MULTI_VALUE_APPEND  => $this->getTranslator()->translate('Append'),
				Workflow_Action_Workflow_Data::MULTI_VALUE_REPLACE => $this->getTranslator()->translate('Replace'),
				Workflow_Action_Workflow_Data::MULTI_VALUE_IGNORE  => $this->getTranslator()->translate('Ignore')
			)
		));
	}

	/**
	 * Populates the form.
	 *
	 * @param Camac_Action_Checkquery_Data $resource
	 * @return Zend_Form
	 */
	public function populate(Camac_Model_Data_Resource_Action $action) {

		$values = array();

		$values['workflow_id'] = $action->getWorkflowItemID();
		$values['multi_value'] = $action->getMultiValue();

		return parent::populate($values, $action);

	}

}
