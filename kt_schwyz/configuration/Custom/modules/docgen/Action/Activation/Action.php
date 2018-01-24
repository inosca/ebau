<?php
/**
 * Docgen_Action_Activation_Action class file.
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
 * Docgen_Action_Activation_Action class.
 * Action handler for handling activation actions within
 * the CAMAC frontend.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Activation_Action
	extends Camac_Action_Action
{
	/**
	 * Handles the flow of actions.
	 *
	 * @param boolean $success The status of the previous action.
	 *
	 * @return boolean $success TRUE if the action has been successfully executed,
	 *                          FALSE otherwise
	 */
	public function handleAction($success = true)
	{
		$currentSuccess = $success;
		$action = $this->getResourceAction();

		if ($action->isAlwaysExecutable() || $success) {
			$result = false;

			try {
				$actionMapper = new Docgen_Action_Activation_Mapper();
				$instanceAction = $actionMapper->getActivationAction(
					$action->getActionId()
				);

				$activationActionId = $instanceAction->getActivationactionId();

				$actionMapper = new Docgen_Model_Mapper_Activationaction();
				$activationAction = $actionMapper->getActivationAction(
					$activationActionId
				);

				$actionName = 'Docgen_Action_Activation_' . $activationAction->name;
				$performableAction = new $actionName();
				$result = $performableAction->handleAction($currentSuccess);

			}
			catch (\Exception $e) {

				Zend_Registry::get('log')->log(
					'There was an error '
					. 'performing the activation action '
					. $activationAction->name . ': '
					. $e->getMessage(),
					Zend_Log::ERR
				);
				$result = false;
			}

			$this->setMessage($result);
			$currentSuccess = $success && $result;
		}

		return parent::handleAction($currentSuccess);
	}
}
