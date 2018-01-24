<?php

class Billing_InstanceResource_Billing_Helper_InstanceResourceBilling extends Zend_Controller_Action_Helper_Abstract implements Camac_InstanceResource_Helper_Interface {

	public function add($instanceResourceId, $form) {

	}

	public function update($instanceResourceId, $form) {
	}


	public function getResource($instanceResourceId, $language = null) {

		$instanceResourceMapper = new Admin_Model_Mapper_Resource_InstanceResource();

		return $instanceResourceMapper->getInstanceResource($instanceResourceId);


	}

	public function getForm() {
		return new Billing_InstanceResource_Billing_Form();
	}

	/**
	 * Injects variables to the view.
	 * These variables are used to display data in the additional tabs added by te resource.
	 *
	 * @param int $resourceId
	 * @param Zend_View $view
	 * @return void
	 */
	public function injectVariables($resourceId, $view) {

	}

	/**
	 * Retrieves the url of the file with the additional tabs to display.
	 *
	 * @return null
	 */
	public function getTabs() {

		return NULL;

	}

	/**
	 * Retrieves the url of the file with the context menu fo the additioanl tabs.
	 *
	 * @return null
	 */
	public function getContextMenu() {

		return NULL;

	}

	/**
	 * Check if a given instance resource is referenced by records of other tables.
	 *
	 * @param int $instanceResourceId
	 * @return boolean Returns true if there are records referencing the instance resource, false otherwise.
	 */
	public function isReferenced($instanceResourceId) {
		return false;
	}

	/**
	 * Deletes the instance resource.
	 *
	 * @param int $instanceResourceId
	 * @return void
	 */
	public function delete($instanceResourceId) {
		// No table, do nothing
	}
}
