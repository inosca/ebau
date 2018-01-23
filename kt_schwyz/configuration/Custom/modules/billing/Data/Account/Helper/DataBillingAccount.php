<?php


class Billing_Data_Account_Helper_DataBillingAccount extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	protected $mapper;

	public function __construct() {
		$this->mapper = new Billing_Model_Mapper_Account();
		$this->stateMapper = new Billing_Model_Mapper_AccountState();
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function add($form, $id, $mode) {
		$account = new Billing_Model_Data_Account(
			NULL,
			$form->getValue('department'),
			$form->getValue('name'),
			$form->getValue('accountNumber'),
			$form->getValue('serviceGroupID'),
			true
		);
		$id = $this->mapper->insert($account);
		foreach ($form->getValue('states') as $stateId) {
			$accountState = new Billing_Model_Data_AccountState(
				null,
				$id,
				$stateId
			);
			$this->stateMapper->insert($accountState);
		}

	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function update($id, $form) {
		$account = new Billing_Model_Data_Account(
			$id,
			$form->getValue('department'),
			$form->getValue('name'),
			$form->getValue('accountNumber'),
			$form->getValue('serviceGroupID'),
			true
		);
		$this->mapper->update($account);

		$this->stateMapper->deleteAll($id);

		foreach ($form->getValue('states') as $stateId) {
			$accountState = new Billing_Model_Data_AccountState(
				null,
				$id,
				$stateId
			);
			$this->stateMapper->insert($accountState);
		}
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->stateMapper->deleteAll($id);
		$this->mapper->delete($id);
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function move($id, $targetid, $mode) {
	}

	public function getRows() {
		return $this->mapper->getAccounts();
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function getData($id) {
		return $this->mapper->getAccount($id);
	}

	public function getForm() {
		//include "../configuration/Custom/modules/Billing/Data/Account/Form.php";
		return new Billing_Data_Account_Form();
	}
}


