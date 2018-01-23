<?php


class Billing_Model_DbTable_Account extends Zend_Db_Table_Abstract {

	protected $_name = 'BILLING_ACCOUNT';

	protected $_primary = 'BILLING_ACCOUNT_ID';

	protected $_sequence = 'BILLING_ACCOUNT_SEQ';
}
