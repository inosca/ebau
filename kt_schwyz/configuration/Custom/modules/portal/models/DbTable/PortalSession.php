<?php

class Portal_Model_DbTable_PortalSession extends Zend_Db_Table_Abstract {

	/**
	 * The table name.
	 *
	 * @var string
	 */
	protected $_name = 'PORTAL_SESSION';

	/**
	 * The primary key column or columns.
	 * A compound key should be declared as an array.
	 * You may declare a single-column primary key
	 * as a string.
	 *
	 * @var mixed
	 */
	protected $_primary = 'PORTAL_SESSION_ID';

	protected $_sequence = false;
}
