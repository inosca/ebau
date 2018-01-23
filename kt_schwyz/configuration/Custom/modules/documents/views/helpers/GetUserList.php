<?php

class Documents_View_Helper_GetUserList extends Zend_View_Helper_Abstract {

	public function getUserList() {
		$userMapper = new Camac_Model_DbTable_Account_User();

		$select = $userMapper->select()
			->setIntegrityCheck(false)
			->from(array('u' => 'USER'),
				array('*')
			)
			->join(array('ug' => 'USER_GROUP') , '"u"."USER_ID"   = "ug"."USER_ID" AND "ug"."DEFAULT_GROUP" = 1' , array())
			->join(array('g'  => 'GROUP')      , '"ug"."GROUP_ID" = "g"."GROUP_ID"'                              , array())
			->join(array('r'  => 'ROLE')       , '"g"."ROLE_ID"  = "r"."ROLE_ID"'                                , array('ROLE_NAME' => 'r.NAME'))
			->order('r.NAME')
			->order('USERNAME');

		$userData = $userMapper->fetchAll($select);

		$userList = array();

		foreach ($userData as $entry) {
			$roleName = $entry['ROLE_NAME'];

			if (!array_key_exists($roleName, $userList)) {
				$userList[$roleName] = array();
			}

			$userList[$roleName][] = $entry;
		}

		return $userList;
	}
}
