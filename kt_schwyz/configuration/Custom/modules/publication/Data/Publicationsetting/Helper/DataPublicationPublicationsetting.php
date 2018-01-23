<?php

class Publication_Data_Publicationsetting_Helper_DataPublicationPublicationsetting extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {


	protected $mapper;

	public function __construct() {
		$this->mapper = new Publication_Model_Mapper_PublicationSetting();
	}

	/**
	 * @SuppressWarnings(unused)
	 * @SuppressWarnings(short)
	 */
	public function add($form, $id, $mode) {
		$publicationSetting = new Publication_Model_Data_PublicationSetting(
			null,
			$form->getValue('key'),
			$form->getValue('value')
		);
		$this->mapper->save($publicationSetting);
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function update($id, $form) {
		$publicationSetting        = $this->mapper->getEntry($id);
		$publicationSetting->key   = $form->getValue('key');
		$publicationSetting->value = $form->getValue('value');

		$this->mapper->update($publicationSetting);
	}


	/**
	 * @SuppressWarnings(short)
	 */
	public function delete($id) {
		$this->mapper->delete($id);
	}

	/**
	 *  @SuppressWarnings(short)
	 */
	public function move($id, $targetId, $mode) {
		//not needed..
	}

	public function getRows() {
		return $this->mapper->getEntries();
	}

	/**
	 * @SuppressWarnings(short)
	 */
	public function getData($id) {
		return $this->mapper->getEntry($id);
	}

	public function getForm() {
		return new Publication_Data_Publicationsetting_Form();
	}
}
