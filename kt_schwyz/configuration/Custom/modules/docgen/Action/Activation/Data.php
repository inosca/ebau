<?php
/**
 * Docgen_Action_Activation_Data class file.
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
 * Docgen_Action_Activation_Data class.
 * Data model for actions within
 * the CAMAC backend.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Activation_Data 
	extends Camac_Model_Data_Resource_Action
{
	protected $activationactionId;

	/**
	 * Constructor.
	 *
	 * @param int    $actionId           The identifier of the action.
	 * @param int    $availableActionId  The identifier of the available action.
	 * @param int    $buttonId           The identifier of the button.
	 * @param string $name               The name of the action.
	 * @param string $description        The description of the action.
	 * @param string $confirmMessage     The message which gets displayed 
	 *                                   upon successful execution.
	 * @param string $errorMessage       The message which gets displayed
	 *                                   upon an error.
	 * @param bool   $executeAlways      Whether the action shall be
	 *                                   executed in every case or not.
	 * @param bool   $sort               The execution order of the action.
	 * @param int    $activationActionId The identifier of the activation action.
	 *
	 * @return void
	 *
	 * @SuppressWarnings(ExcessiveParameterList)
	 */
	public function __construct(
		$actionId,
		$availableActionId,
		$buttonId,
		$name,
		$description,
		$confirmMessage,
		$errorMessage,
		$executeAlways,
		$sort,
		$activationActionId
	) {
		parent::__construct(
			$actionId,
			$availableActionId,
			$buttonId,
			$name,
			$description,
			$confirmMessage,
			$errorMessage,
			$executeAlways,
			$sort
		);

		$this->activationactionId = $activationActionId;
	}

	/**
	 * Getter for the identifier of the activation action.
	 *
	 * @return int Identifier of the activation action.
	 */
	public function getActivationactionId()
	{
		return $this->activationactionId;
	}
}
