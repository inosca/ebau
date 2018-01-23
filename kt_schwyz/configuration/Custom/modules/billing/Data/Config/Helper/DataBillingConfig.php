<?php


class Billing_Data_Config_Helper_DataBillingConfig extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Billing_Model_Mapper_Config();
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function add($form, $id, $mode) {
		$config = new Billing_Model_Data_Config(
			NULL,
			$form->getValue('name'),
			$form->getValue('value')
		);
		$this->mapper->insert($config);
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function update($id, $form) {
		$config = new Billing_Model_Data_Config(
			$id,
			$form->getValue('name'),
			$form->getValue('value')
		);
		$this->mapper->update($config);
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->mapper->delete($id);
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function move($id, $targetid, $mode) {
	}

	public function getRows() {
		return $this->mapper->getConfigs();
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function getData($id) {
		return $this->mapper->getConfig($id);
	}

	public function getForm() {
		return new Billing_Data_Config_Form();
	}
}


