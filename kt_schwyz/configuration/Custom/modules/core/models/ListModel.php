<?php

class Core_Model_ListModel {

	/**
	 * Map user roles to form groups
	 *
	 * The form groups  are used by getGetQueryByRole to determine if the role
	 * is allowed to access the list.
	 *
	 * @var array
	 */
	private static $formGroupByRole = array(
		Custom_UriConstants::ROLE_BG           => array(Custom_UriConstants::FORM_GROUP_BAUKOORDINATION),
		Custom_UriConstants::ROLE_SERVICE         => array(Custom_UriConstants::FORM_GROUP_ALL),
		Custom_UriConstants::ROLE_SUBSERVICE      => array(Custom_UriConstants::FORM_GROUP_ALL),
		Custom_UriConstants::ROLE_COMM_SERVICE    => array(Custom_UriConstants::FORM_GROUP_ALL),
		Custom_UriConstants::ROLE_COMMUNITY       => array(Custom_UriConstants::FORM_GROUP_ALL),
		Custom_UriConstants::ROLE_BUILD_COMMITTEE => array(Custom_UriConstants::FORM_GROUP_ALL),
		Custom_UriConstants::ROLE_BD              => array(Custom_UriConstants::FORM_GROUP_BD),
		Custom_UriConstants::ROLE_NP              => array(Custom_UriConstants::FORM_GROUP_NP),
		Custom_UriConstants::ROLE_AFU             => array(Custom_UriConstants::FORM_GROUP_AFU),
		Custom_UriConstants::ROLE_ALA             => array(Custom_UriConstants::FORM_GROUP_ALA),
		Custom_UriConstants::ROLE_AFE             => array(Custom_UriConstants::FORM_GROUP_AFE),
		Custom_UriConstants::ROLE_AFJ             => array(Custom_UriConstants::FORM_GROUP_AFJ),
		Custom_UriConstants::ROLE_READONLY_ORG    => array(Custom_UriConstants::FORM_GROUP_READONLY_ORG),
		Custom_UriConstants::ROLE_COMMISSIONER    => array(Custom_UriConstants::FORM_GROUP_ALL)
	);

	/**
	 * get a list query based on the users role and the current resource
	 *
	 * This is used in lieu of having this same old SQL statment stored in
	 * the database the camac way.
	 *
	 * @param object  $resource resource instance from mapper
	 *
	 * @return string
	 */
	public static function getQueryByRole($resource) {
		$config = Zend_Registry::get('config');
		$isOracle = in_array($config->resources->db->adapter, array('Oracle', 'Pdo_Oci'));

		$roleId = Custom_UriUtils::getCurrentRole();
		$resourceName = $resource->getName();

		$isGuest = true;
		$formGroups = array(Custom_UriConstants::FORM_GROUP_BAUKOORDINATION); // default form group for guests
		if (array_key_exists($roleId, self::$formGroupByRole)) {
			$formGroups = self::$formGroupByRole[$roleId];
			$isGuest = false;
		}

		if (!$resource || !$resource->instanceStates) {
			return;
		}

		$isBilling  = $resourceName === "Gebühren";
		$isSanction = $resourceName === "Auflagen";
		$isPermitIssued = $resourceName === "Pendenzenliste Baubewilligung erteilt";

		/**
		 * This is implemented as a plain SQL query because I didn't get LISTAGG to work
		 * with Zend_Db_Table - see failed attempt below
		 */
		$columns = array(
			'"INSTANCE"."INSTANCE_ID"            AS "INSTANCE_ID"',
			'"ANSWER_DOK_NR"."ANSWER"            AS "DOSSIER_NR"',
			'"FORM"."NAME"                       AS "FORM"',
			'"LOCATION"."NAME"                   AS "COMMUNITY"',
			'"USER"."USERNAME"                   AS "USER"',
			'"ANSWER_STREET_BG"."ANSWER"         AS "STREET"',
			'"INSTANCE_STATE"."NAME"             AS "STATE"',
			'"APPLICANT_VIEW"."APPLICANT"',
			'"GET_INST_STATE_DESCRIPTION"("INSTANCE_STATE"."NAME") AS "STATE_DESCRIPTION"',
			'CASE
				WHEN "ANSWER_STREET_BG"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_BG"."ANSWER"
				WHEN "ANSWER_STREET_NP"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_NP"."ANSWER"
				WHEN "ANSWER_STREET_247"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_247"."ANSWER"
				END AS "STREET"',
		);
		if ($isOracle) {
			$columns[] = 'SUBSTR("FORM"."DESCRIPTION", Instr("FORM"."DESCRIPTION", \';\', -1, 1) +1)    AS "KOOR"';
			$columns[] = 'SUBSTR("FORM"."DESCRIPTION", 1, Instr("FORM"."DESCRIPTION", \';\', -1, 1) -1) AS "KOOR_SHORT"';
			$columns[] = '(SELECT LISTAGG("NAME", \', \') WITHIN GROUP (ORDER BY "NAME")
				FROM INTENTIONS WHERE "INSTANCE_ID" = "INSTANCE"."INSTANCE_ID") AS "INTENT"';
		} else {
			$columns[] = 'SUBSTR("FORM"."DESCRIPTION", position(\';\' in "FORM"."DESCRIPTION") +1)    AS "KOOR"';
			// TODO fix this for PG 'SUBSTR("FORM"."DESCRIPTION", 1, Instr("FORM"."DESCRIPTION", \';\', -1, 1) -1) AS "KOOR_SHORT"',
			$columns[] = '(SELECT
				string_agg("NAME", \', \' order by "NAME")
				FROM "INTENTIONS" WHERE "INSTANCE_ID" = "INSTANCE"."INSTANCE_ID") AS "INTENT"';
		}

		$joins = '
			LEFT JOIN "APPLICANT_VIEW" ON (
				"INSTANCE"."INSTANCE_ID" = "APPLICANT_VIEW"."INSTANCE_ID"
			)

			JOIN "INSTANCE_LOCATION" ON (
				"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"
			)

			JOIN "LOCATION" ON (
				"INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"
			)

			JOIN "FORM" ON (
				"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"
			)

			JOIN "USER" ON (
				"INSTANCE"."USER_ID" = "USER"."USER_ID"
			)

			JOIN "GROUP" ON (
				"INSTANCE"."GROUP_ID" = "GROUP"."GROUP_ID"
			)

			JOIN "ANSWER_DOK_NR" ON (
				"INSTANCE"."INSTANCE_ID" = "ANSWER_DOK_NR"."INSTANCE_ID"
			)

			LEFT JOIN "ANSWER_STREET_BG" ON (
				"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_BG"."INSTANCE_ID"
			)

			LEFT JOIN "ANSWER_STREET_NP" ON (
				"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_NP"."INSTANCE_ID"
			)

			LEFT JOIN "ANSWER_STREET_247" ON (
				"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_247"."INSTANCE_ID"
			)

			JOIN "FORM_GROUP_FORM" ON (
				"FORM_GROUP_FORM"."FORM_ID" = "INSTANCE"."FORM_ID"
			)

			JOIN "INSTANCE_STATE" ON (
				"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"
			)';

		$guestJoins = '';
		if ($isGuest) {
			$guestJoins = '
			LEFT JOIN "ANSWER" "ANSWER_PARCEL" ON (
				"INSTANCE"."INSTANCE_ID" = "ANSWER_PARCEL"."INSTANCE_ID" AND
				"QUESTION_ID" = 91
			)
			';
			if ($isOracle) {
				$guestJoins .= 'JOIN "WORKFLOW_ENTRY" PUBLIKATION ON (
					"INSTANCE"."INSTANCE_ID" = PUBLIKATION."INSTANCE_ID" AND
					PUBLIKATION."WORKFLOW_ITEM_ID" = 15 AND
					TRUNC(PUBLIKATION."WORKFLOW_DATE") <= sysdate
				)
				JOIN "WORKFLOW_ENTRY" EINSPRACHEFRIST ON (
					"INSTANCE"."INSTANCE_ID" = EINSPRACHEFRIST."INSTANCE_ID" AND
					EINSPRACHEFRIST."WORKFLOW_ITEM_ID" = 65 AND
					TRUNC(EINSPRACHEFRIST."WORKFLOW_DATE") >= sysdate
				)';
			} else {
				$guestJoins .= 'JOIN "WORKFLOW_ENTRY" PUBLIKATION ON (
					"INSTANCE"."INSTANCE_ID" = PUBLIKATION."INSTANCE_ID" AND
					PUBLIKATION."WORKFLOW_ITEM_ID" = 15 AND
					PUBLIKATION."WORKFLOW_DATE" <= current_date
				)
				JOIN "WORKFLOW_ENTRY" EINSPRACHEFRIST ON (
					"INSTANCE"."INSTANCE_ID" = EINSPRACHEFRIST."INSTANCE_ID" AND
					EINSPRACHEFRIST."WORKFLOW_ITEM_ID" = 65 AND
					EINSPRACHEFRIST."WORKFLOW_DATE" >= current_date
				)';
			}
			$columns[] = '"ANSWER_PARCEL"."ANSWER" AS "PARCEL_NR"';
		}

		$sanctionJoins = $isSanction ? '
			JOIN "SANCTION" ON (
				"SANCTION"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
			)' : '';

		$baseWhere = '
			WHERE
				"INSTANCE"."INSTANCE_STATE_ID" IN (%states)
			AND
			"FORM_GROUP_FORM"."FORM_GROUP_ID" IN (%formGroups)';

		if (
			$roleId == Custom_UriConstants::ROLE_COMMUNITY ||
			$roleId == Custom_UriConstants::ROLE_BUILD_COMMITTEE ||
			$roleId == Custom_UriConstants::ROLE_READONLY_ORG
		) {
			// community: only show own location
			$joins .= '
				JOIN "GROUP_LOCATION" ON (
					"GROUP_LOCATION"."GROUP_ID" = %groupId
				)';

			$baseWhere .= '
				AND "GROUP_LOCATION"."LOCATION_ID" = "INSTANCE_LOCATION"."LOCATION_ID"';

			// Add "Versand Baubewilligung" entries to the query
			if ($isPermitIssued) {
				$joins .= '
					JOIN "WORKFLOW_ENTRY" "PERMIT_ISSUED" ON (
						"PERMIT_ISSUED"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID" AND
						"PERMIT_ISSUED"."WORKFLOW_ITEM_ID" = 72
					)';
			}
			else {
				$joins .= '
					LEFT JOIN "WORKFLOW_ENTRY" "PERMIT_ISSUED" ON (
						"PERMIT_ISSUED"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID" AND
						"PERMIT_ISSUED"."WORKFLOW_ITEM_ID" = 72
					)';
				$baseWhere .= '
					AND "PERMIT_ISSUED"."INSTANCE_ID" IS NULL';
			}
		}
		else if (Custom_UriUtils::isService($roleId)) {
			// Hack: Services see 3 lists of dossiers of specific KOORs (e.g. "In Zirkularion (BG)")
			// Instead of extending the admin ui and complicating things a lot, we'll just implement
			// the override here.
			if (
				$roleId == Custom_UriConstants::ROLE_SERVICE &&
				self::isCirculation($resourceName)
			) {
				if (strpos($resourceName, 'BG') !== false) {
					$formGroups = array(Custom_UriConstants::FORM_GROUP_BAUKOORDINATION);
				}
				else if (strpos($resourceName, 'BD') !== false) {
					$formGroups = array(Custom_UriConstants::FORM_GROUP_BD);
				}
				else if (strpos($resourceName, 'NP') !== false) {
					$formGroups = array(Custom_UriConstants::FORM_GROUP_NP);
				}
			}
			else {
				// service: check activation
				$columns[] = 'TO_CHAR("ACTIVATION"."DEADLINE_DATE", \'DD.MM.YYYY\') AS "DEADLINE"';
				$columns[] = '"ACTIVATION"."REASON" AS "REASON"';
				$columns[] = '"CIRCULATION_STATE"."NAME" AS "CIRC_STATE"';
				$joins .= '
					JOIN "CIRCULATION" ON (
						"CIRCULATION"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
					)
					JOIN "ACTIVATION" ON (
						"ACTIVATION"."CIRCULATION_ID" = "CIRCULATION"."CIRCULATION_ID"
						AND
						"ACTIVATION"."SERVICE_ID" = %serviceId
					)
					LEFT JOIN "CIRCULATION_STATE" ON (
						"ACTIVATION"."CIRCULATION_STATE_ID" = "CIRCULATION_STATE"."CIRCULATION_STATE_ID"
					)';
				$baseWhere .= '
					AND ("ACTIVATION"."CIRCULATION_STATE_ID" = 1
						OR
						"ACTIVATION"."CIRCULATION_STATE_ID" = 41)';
			}
		}
		else if (Custom_UriConstants::ROLE_COMMISSIONER == $roleId) {
			$joins .= '
				JOIN "COMMISSION_ASSIGNMENT" ON (
					"INSTANCE"."INSTANCE_ID" = "COMMISSION_ASSIGNMENT"."INSTANCE_ID"
					AND
						"COMMISSION_ASSIGNMENT"."GROUP_ID" = %groupId
				)
			';
		}

		$billingWhere = $isBilling ? '
			AND
				"INSTANCE"."INSTANCE_ID" IN (
					SELECT
						"INSTANCE_ID" FROM "BILLING_ENTRY"
					WHERE
						"BILLING_ENTRY"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
					AND
						"BILLING_ENTRY"."INVOICED" = 0
					AND
						"BILLING_ENTRY"."TYPE" = 1
			)' : '';

		$sanctionWhere = $isSanction ? '
			AND
				"SANCTION"."IS_FINISHED" = 0' : '';

		// be careful here - no build-in SQL injection safety!
		$data = array(
			'%states'    => $resource->instanceStates,
			'%formGroups' => implode($formGroups, ', '),
			'%groupId'   => Custom_UriUtils::getCurrentGroup(),
			'%serviceId' => Custom_UriUtils::getCurrentService()
		);

		$where = $baseWhere . $billingWhere . $sanctionWhere;
		$query = 'SELECT ' . implode($columns, ', ') . ' FROM "INSTANCE" '.$joins . $guestJoins . $sanctionJoins;
		return str_replace(array_keys($data), array_values($data), $query.$where);
	}

	public static function isCirculation($resourceName) {
		return strpos($resourceName, 'Zirkulation') !== false;
	}
}

/**
 * Didn't get LISTAGG to work with Zend_Db ...
 */

/*
$table = new Camac_Model_DbTable_Instance();
$select = $table->select();
$select
	->setIntegrityCheck(false)
	->from($table, array(
		'INSTANCE.INSTANCE_ID',
		'INTENT' => new Zend_Db_Expr('(SELECT LISTAGG("NAME", ", ") WITHIN GROUP (ORDER BY "NAME" FROM INTENTIONS WHERE "INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"))')
	))
	->where('INSTANCE_STATE_ID = ?', 22) // EXT
	->join('ANSWER_DOK_NR', 'INSTANCE.INSTANCE_ID = ANSWER_DOK_NR.INSTANCE_ID', array('DOSSIER_NR' => 'ANSWER_DOK_NR.ANSWER'))
	->join('FORM', 'INSTANCE.FORM_ID = FORM.FORM_ID', array('FORM' => 'FORM.NAME'))
	->join('INSTANCE_LOCATION', 'INSTANCE.INSTANCE_ID = INSTANCE_LOCATION.INSTANCE_ID', array('LOCATION_ID'))
	->join('LOCATION', 'INSTANCE_LOCATION.LOCATION_ID = LOCATION.LOCATION_ID', array('COMMUNITY' => 'LOCATION.NAME'))
	->join('USER', 'INSTANCE.USER_ID = "USER".USER_ID', array('USER' => 'USER.USERNAME'))
	->join('INTENTIONS', 'INSTANCE.INSTANCE_ID = INTENTIONS.INSTANCE_ID', array('INTENT' => 'INTENTIONS.NAME'))
	;
 */
