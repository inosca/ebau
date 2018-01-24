<?php
/**
 * Docgen_Model_Data_Activationaction
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\Data
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */

/**
 * Docgen_Model_Data_Activationaction
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\Data
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Model_Data_Activationaction
{

	/**
	 * ID of the activation action.
	 *
	 * @var integer
	 */
	public $actionId;
	/**
	* Name of the activation action.
	 *
	 * @var string
	 */
	public $name;

	/**
	 * Constructor.
	 *
	 * @param int    $actionId The ID of the activation action.
	 * @param string $name     The name of the activation action.
	 */
	public function __construct(
		$actionId,
		$name
	) {
		$this->actionId   = $actionId;
		$this->name = $name;
	}
}
