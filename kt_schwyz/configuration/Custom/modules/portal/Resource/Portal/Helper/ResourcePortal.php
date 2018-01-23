<?php

class Portal_Resource_Portal_Helper_ResourcePortal extends Zend_Controller_Action_Helper_Abstract implements Camac_Resource_Helper_Interface {

	/**
	 * Adds a new resource.
	 *
	 * @param int $resourceId
	 * @param Camac_Resource_Search_Form $form
	 * @return void
	 */
	public function add($resourceId, $form) {

	}

	/**
	 * Updates the resource.
	 *
	 * @param int $resourceId
	 * @param Camac_Resource_Search_Form $form
	 * @return void
	 */
	public function update($resourceId, $form) {

	}

	/**
	 * Retrieves the instance of the resource.
	 *
	 * @param int $resourceId
	 * @return Camac_Resource_Search_Data
	 */
	public function getResource($resourceId) {
		$resourceMapper = new Admin_Model_Mapper_Resource_Resource();
		return $resourceMapper->getResource($resourceId);
	}

	/**
	 * Retrieves the form.
	 *
	 * @return Camac_Resource_Search_Form
	 */
	public function getForm() {
		return new Portal_Resource_Portal_Form();
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
	 * @return string
	 */
	public function getTabs() {
		return NULL;
	}

	/**
	 *  Retrieves the url of the file with the context menu fo the additioanl tabs.
	 *
	 * @return string
	 */
	public function getContextMenu() {
		return NULL;
	}

	/**
	 * Deletes the resource.
	 *
	 * @param int $resourceId
	 * @return void
	 */
	public function delete($resourceId) {
	}
}
