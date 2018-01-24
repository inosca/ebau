<?php


class Billing_Data_Account_Form extends Camac_Form_Admin {
	public function init() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());
		$accountId = Zend_Controller_Front::getInstance()->getRequest()->getParam('id');

		$this->addElement('text', 'department', array(
			'label' => $this->getTranslator()->translate('Department'),
			'class' => 'text',
			'required' => true,
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 255)
			)
		));

		$this->addElement('select', 'serviceGroupID', array(
			'label' => $this->getTranslator()->translate('Service Group'),
			'class' => 'text',
			'required' => true,
			'multiOptions' => $this->getServiceGroups()
		));

		$this->addElement('text', 'name', array(
			'label' => $this->getTranslator()->translate('Name'),
			'class' => 'text',
			'required' => true,
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 255)
			)
		));

		$this->addElement('text', 'accountNumber', array(
			'label' => $this->getTranslator()->translate('Account number'),
			'class' => 'text',
			'required' => true,
			'filters' => array(
				'StringTrim' => new Zend_Filter_StringTrim(),
				'StripTags' => new Zend_Filter_StripTags()
			),
			'validators' => array(
				'StringLength' => new Zend_Validate_StringLength(0, 255)
			)
		));
		
		// Retrieve all the states
		$instanceStateMapper = new Admin_Model_Mapper_Resource_InstanceState();
		$states = $instanceStateMapper->getInstanceStates();

		// Retrieve selected states
		$accountStateMapper = new Billing_Model_Mapper_AccountState();
		
		if ($accountId) {
			$selected = array_map(function($state) {
				return $state->instanceStateId;
			}, $accountStateMapper->getStates($accountId));
		} else {
			$selected = array();
		}

		$options = array();
		foreach ($states as $state) {
			$options[$state->getInstanceStateId()] = $state->getName();
		}
		$states = new Zend_Form_Element_MultiCheckbox('states', array(
			'label' => 'States',
			'multiOptions' => $options,
			'value' => $selected
		));
		$this->addElement($states);

		$this->addElement('submit', 'save', array(
			'label' => $this->getTranslator()->translate('Save'),
			'class' => 'button save'
		));


		$this->initDisplayGroup();
	}

	/**
	 * @SuppressWarnings(unused)
	 */
	public function populate(Billing_Model_Data_Account $account) {
		$values = array();
		$values['department']     = $account->department;
		$values['accountNumber']  = $account->accountNumber;
		$values['name']           = $account->name;
		$values['serviceGroupID'] = $account->serviceGroupID;
		return parent::populate($values);
	}
	
	private function getServiceGroups() {
		$mapper = new Admin_Model_Mapper_Account_ServiceGroup();
		$groups = $mapper->getServiceGroups();
		$result = array();
		foreach ($groups as $group) {
			$result[$group->getServiceGroupId()] = $group->getName();
		}

		return $result;
	}
}


