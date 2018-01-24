<?php

/**
 * Sanction form. This form is not used for rendering, but just for validation.
 *
 * @author Christian Zosel <christian.zosel@adfinis-sygroup.ch>
 */
class Sanction_Data_Sanction extends Camac_Form_Application {

	/**
	 * Constructor.
	 *
	 * @return void
	 */
	public function __construct() {

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

		$this->addElement('CamacText', 'text', array(
			'secure' => true,
			'required' => true,
			'errorMessages' => array('Bitte geben Sie im Feld "Art der Auflage" einen Text ein.')
		));
		$this->addElement('CamacText', 'startDate', array(
			'validators' => array(
				array('Date', true, array('locale' => 'de'))
			),
			'required' => true,
			'secure' => true,
			'errorMessages' => array('Bitte geben Sie im Feld "Verfügung / Stellungnahme vom" ein Datum ein.')
		));
		$this->addElement('CamacText', 'deadlineDate', array(
			'validators' => array(
				array('Date', true, array('locale' => 'de'))
			),
			'secure' => true,
			'errorMessages' => array('Bitte geben Sie im Feld "Frist" ein Datum ein.')
		));
		$this->addElement('CamacText', 'endDate', array(
			'validators' => array(
				array('Date', true, array('locale' => 'de'))
			),
			'secure' => true,
			'errorMessages' => array('Bitte geben Sie im Feld "Abnahme Datum" ein Datum ein.')
		));
		$this->addElement('CamacText', 'notice', array(
			'secure' => true
		));
		$this->addElement('CamacCheckbox', 'isFinished', array(
			'secure' => true
		));

		$this->addElement('CamacHidden', 'sanctionID', array(
			'validators' => array('digits')
		));
	}

}
