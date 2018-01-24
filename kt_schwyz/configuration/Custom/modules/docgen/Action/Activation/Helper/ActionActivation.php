<?php
/**
 * Docgen_Action_Activation_Helper_ActionActivation class file.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation\Helper
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */

/**
 * Docgen_Action_Activation_Helper_ActionActivation class.
 * Action mapper for handling activation actions from within
 * the CAMAC backend.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation\Helper
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Activation_Helper_ActionActivation
	extends Zend_Controller_Action_Helper_Abstract
	implements Camac_Action_Helper_Interface
{
	protected $mapper;

	/**
	 * Constructor.
	 */
	public function __construct()
	{
		$this->mapper = new Docgen_Action_Activation_Mapper();
	}

	/**
	 * Adds a new action.
	 *
	 * @param int                          $actionId The identifier of the action.
	 * @param Camac_Action_Activation_Form $form     The backend form.
	 *
	 * @return void
	 */
	public function add($actionId, $form)
	{
		$activationAction = new Docgen_Action_Activation_Data(
			$actionId,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			null,
			$form->getValue('activation_action_id')
		);

		$this->mapper->save($activationAction);
	}

	/**
	 * Updates the action.
	 *
	 * @param int                          $actionId The identifier of the action.
	 * @param Camac_Action_Activation_Form $form     The backend form.
	 *
	 * @return void
	 */
	public function update($actionId, $form)
	{
		$activationAction = new Docgen_Action_Activation_Data(
			$actionId,
			null, null, null, null, null, null, null, null,
			$form->getValue('activation_action_id')
		);

		$this->mapper->update($activationAction);
	}

	/**
	 * Retrieves the instance of the action.
	 *
	 * @param int  $actionId    The identifier of the action.
	 * @param bool $interpreted Wether the action shall be interpreted or not.
	 *
	 * @return Docgen_Model_Data_Activationaction
	 *
	 * @SuppressWarnings(UnusedFormalParameter)
	 */
	public function getAction($actionId, $interpreted = false)
	{
		return $this->mapper->getActivationAction($actionId);
	}

	/**
	 * Retrieves the form.
	 *
	 * @return Camac_Action_Activation_Form
	 */
	public function getForm()
	{
		return new Docgen_Action_Activation_Form();
	}

	/**
	 * Injects variables to the view.
	 * These variables are used to display data in the additional
	 * tabs added by te resource.
	 *
	 * @param int       $actionId The identifier of the action.
	 * @param Zend_View $view     The (backend) view where the variables
	 *                            shall be injected into.
	 *
	 * @return void
	 *
	 * @SuppressWarnings(UnusedFormalParameter)
	 */
	public function injectVariables($actionId, $view)
	{
	}

	/**
	 * Retrieves the url of the file with the additional tabs to display.
	 *
	 * @return string
	 */
	public function getTabs()
	{
		return null;
	}

	/**
	 *  Retrieves the url of the file with the context menu fo the additioanl tabs.
	 *
	 * @return string
	 */
	public function getContextMenu()
	{
		return null;
	}

	/**
	 * Retrieves the instance of the concrete handler action
	 *
	 * @param int $actionId The identifier of the action.
	 *
	 * @return Camac_Action_Activation_Action
	 */
	public function getHandlerAction($actionId)
	{
		$resourceAction = $this->getAction($actionId, true);
		return new Docgen_Action_Activation_Action($resourceAction);

	}

	/**
	 * Deletes the action.
	 *
	 * @param int $actionId The identifier of the action.
	 *
	 * @return void
	 *
	 * @SuppressWarnings(UnusedFormalParameter)
	 */
	public function delete($actionId)
	{
		$this->mapper->delete($actionId);
	}
}
