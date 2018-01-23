<?php

class Core_Resource_Simplelist_Helper_ResourceSimplelist extends Zend_Controller_Action_Helper_Abstract implements Camac_Resource_Helper_Interface {

	public function add($resourceId, $form) {
		$listResourceMapper = new Core_Resource_Simplelist_Mapper();
		$listResource = new Core_Resource_Simplelist_Data($resourceId, null, null, null, null, null, null, null, $form->getValue('instanceStates'));

		$listResourceMapper->save($listResource);
	}

	public function update($resourceId, $form) {
		$listResourceMapper = new Core_Resource_Simplelist_Mapper();
		$listResource = new Core_Resource_Simplelist_Data($resourceId, null, null, null, null, null, null, null, $form->getValue('instanceStates'));

		$listResourceMapper->update($listResource);
	}

	/**
	 * Retrieves the instance of the resource.
	 *
	 * @param int $resourceId
	 * @return Camac_Resource_Search_Data
	 */
	public function getResource($resourceId, $language = null) {
		$listResourceMapper = new Core_Resource_Simplelist_Mapper();
		return $listResourceMapper->getResource($resourceId);
	}

	public function getForm() {
		return new Core_Resource_Simplelist_Form();
	}

	/**
	 * Injects variables to the view.
	 * These variables are used to display data in the additional tabs added by the resource.
	 *
	 * @param int $resourceId
	 * @param Zend_View $view
	 * @return void
	 */
	public function injectVariables($resourceId, $view) {}

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
		$listResourceMapper = new Core_Resource_Simplelist_Mapper();
		$listResourceMapper->delete($resourceId);
	}
}
