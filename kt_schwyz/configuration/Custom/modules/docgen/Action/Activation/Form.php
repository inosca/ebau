<?php
/**
 * Docgen_Action_Activation_Form class file.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */

/**
 * Docgen_Action_Activation_Form class.
 * Mapper for populating and displaying form
 * for activation actions within the CAMAC backend.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Activation_Form
	extends Admin_Form_Resource_Action
{

	/**
	 * Inizializes the form.
	 *
	 * @return void
	 */
	public function init()
	{
		parent::init();

		$actionMapper = new Docgen_Model_Mapper_Activationaction();
		$items = $actionMapper->getActivationActions();

		$actionItems = array();
		foreach ($items as $item) {
			$actionItems[$item->actionId] = $item->name;
		}

		$this->addElement(
			'select',
			'activation_action_id',
			array(
				'label' => $this->getTranslator()->translate('Activation action'),
				'class' => 'select',
				'multiOptions' => $actionItems,
			)
		);
	}

	/**
	 * Populates the form.
	 *
	 * @param Camac_Model_Data_Resource_Action $action Action containing the data.
	 *
	 * @return Zend_Form
	 */
	public function populate(Camac_Model_Data_Resource_Action $action)
	{
		$values = array();
		$values['activation_action_id'] = $action->getActivationactionId();

		return parent::populate($values, $action);
	}

}
