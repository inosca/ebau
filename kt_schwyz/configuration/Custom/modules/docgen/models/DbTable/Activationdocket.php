<?php
/**
 * Docgen_Model_DbTable_Activationdocket class file.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\DbTable
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */

/**
 * Docgen_Model_DbTable_Activationdocket class.
 * Mapper between application and database for
 * activation dockets.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\DbTable
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Model_DbTable_Activationdocket extends Zend_Db_Table_Abstract
{
	// @codingStandardsIgnoreStart
	protected $_name = 'DOCGEN_ACTIVATION_DOCKET';
	protected $_primary = 'DOCGEN_ACTIVATION_DOCKET_ID';
	protected $_sequence = 'DOCGEN_ACTIVATION_DOCKET_SEQ';
	// @codingStandardsIgnoreEnd
}
