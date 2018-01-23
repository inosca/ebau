<?php

/**
 * Billing form. This form is not used for rendering, but just for validation.
 *
 * @author Christian Zosel <christian.zosel@adfinis-sygroup.ch>
 */
class Billing_Data_Billing extends Camac_Form_Application {

	private $serviceGroupID;

	/**
	 * Constructor.
	 *
	 * @return void
	 */
	public function __construct($serviceGroupID) {

		$this->serviceGroupID = $serviceGroupID;
		$this->addPrefixPath('Camac_Form_Element', 'Camac/Form/Element', 'element');

		$this->addButtons();

		// Add the elements to the form
		$this->addFormElements();

		parent::__construct();

	}

	/**
	 * Inizializes the form elements.
	 *
	 * @return void
	 */
	private function addFormElements() {

		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());
		$this->setMethod('post');

		$floatValidator = new Zend_Validate_Float(array('locale' => 'de_CH'));

		$this->addElement('CamacText', 'amount', array(
			'validators' => array($floatValidator),
			'errorMessages' => array('Bitte geben Sie im Feld "Pauschalgebühr" eine Zahl ein.')
		));
		$this->addElement('CamacText', 'hours', array(
			'validators' => array($floatValidator),
			'errorMessages' => array('Bitte geben Sie im Feld "Aufwand" eine Zahl ein.')
		));
		$this->addElement('CamacText', 'other_dept', array(
			'secure' => true
		));
		$this->addElement('CamacText', 'other_name', array(
			'secure' => true
		));
		$this->addElement('CamacText', 'other_account', array(
			'secure' => true
		));

		$this->addElement('CamacText', 'reason', array(
			'secure' => true
		));

		$this->addElement('select', 'basic', array(
			'multiOptions' => array(
				'1' => 'halbe Grundgebühr',
				'2' => 'ganze Grundgebühr',
				'4' => 'doppelte Grundgebühr'
			)
		));

		$accountMapper = new Billing_Model_Mapper_Account();
		$accounts = array_map(function($account) {
			return $account->billingAccountID;
		}, $accountMapper->getAccounts(true, $this->serviceGroupID));
		// add "Andere" entry
		array_push($accounts, -1);

		// this form is rendered with a custom template, so we can also use a hidden element
		$this->addElement('CamacHidden', 'account', array(
			'validators' => array(
				array('inArray', false, array('haystack' => $accounts))
			)
		));

	}

}
