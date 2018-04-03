<?php

/**
 * Notification content data helper controller.
 *
 * @package Notification\Data\Template\Helper
 */
class Notification_Data_Template_Helper_DataNotificationTemplate extends Zend_Controller_Action_Helper_Abstract implements Camac_Data_Helper_Interface {

	/**
	 * Adds a new row.
	 *
	 * @param Notification_Data_Template_Form $form
	 * @param int $id
	 * @param string $mode
	 * @return int The primary key
	 */
	public function add($form, $id, $mode) {

		$table = new Notification_Model_DbTable_Template();

		$templateId = $table->insert($form->getValues());

		return $templateId;

	}

	/**
	 * Updates the row.
	 *
	 * @param int $id
	 * @param Notification_Data_Template_Form $form
	 * @param string $previousLanguage = null
	 * @return void
	 */
	public function update($id, $form, $previousLanguage = null) {
		$table = new Notification_Model_DbTable_Template();
		$table->update($id, $form->getValues());
	}

	/**
	 * Deletes the row.
	 *
	 * @param int $id
	 * @return void
	 */
	public function delete($id) {

		$table = new Notification_Model_DbTable_Template();
		$table->deleteTemplate($id);

	}

	/**
	 * Changes the sort of the row. (Not implemented here)
	 *
	 * @param int $id
	 * @param int $targetId
	 * @param string $mode
	 * @return void
	 */
	public function move($id, $targetId, $mode) {
		// Not implemented
		return false;
	}

	/**
	 * Rows to display in the overview
	 *
	 * @return Notification_Data_Template_Data
	 */
	public function getRows() {
		$table = new Notification_Model_DbTable_Template();
		return $table->getList();
	}

	/**
	 * Retrieves the row.
	 *
	 * @param int $id
	 * @param string $language = null
	 * @param boolean $getTranslations = true
	 * @return Notification_Data_NotificationTemplate_Data
	 */
	public function getData($id, $language = null, $getTranslations = true) {

		$table = new Notification_Model_DbTable_Template();
		$obj = $table->getOne($id, $language);
		return $obj;
	}

	/**
	 * Retrieves the form.
	 *
	 * @return Notification_Data_Notificationcontent_Form
	 */
	public function getForm() {
		return new Notification_Data_Template_Form();

	}

	/**
	 * Delete translation (Not implemented here)
	 *
	 * @param int $id
	 * @param string $language
	 */
	public function deleteTranslation($id, $language) {
		return false;
	}

	/**
	 * Gets a list of languages that don't have yet a translation (plus the current language)
	 *
	 * @param int $searchedKey
	 * @return array('language' => 'language')
	 */
	public function getAvailableLanguageTranslations($searchedKey = null, $usePreviousTranslation = false) {
		$obj = $this->getData($searchedKey);

		$allLanguages = Zend_Registry::get('config')->frontend->languages->toArray();
		if (!is_object($obj)) {
			return array_combine($allLanguages, $allLanguages);
		}

		$translatedLanguages = json_decode(strtolower($obj->languages));

		$available = [$obj->translation => $obj->translation];

		foreach($allLanguages as $lang) {
			if (!in_array($lang, $translatedLanguages)) {
				// not translated, add to list
				$available[$lang] = $lang;
			}
		}

		return $available;
	}

}
