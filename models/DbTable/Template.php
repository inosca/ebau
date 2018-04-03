<?php

class Notification_Model_DbTable_Template extends Zend_Db_Table_Abstract {

	protected $_name = 'NOTIFICATION_TEMPLATE';

	protected $_primary = 'id';

	private $translations;

	public function __construct() {
		parent::__construct();
		$this->translations = new Notification_Model_DbTable_TemplateT();
	}


	public function getList($lang=NULL) {
		if ($lang == null) {
			$lang = (new Zend_Session_Namespace('camac'))->translation;
		}
		$adp = $this->getAdapter();

		$query = $this->select()
			->setIntegrityCheck(false)
			->from('NOTIFICATION_TEMPLATE')
			->joinLeft(
				'NOTIFICATION_TEMPLATE_T',
				'"NOTIFICATION_TEMPLATE"."id" = "NOTIFICATION_TEMPLATE_T"."TEMPLATE_ID"'
			)
			->joinLeft(
				'NOTIFICATION_TEMPLATE_T AS TRANSLATIONS',
				'"NOTIFICATION_TEMPLATE"."id" = "TRANSLATIONS"."TEMPLATE_ID"',
				['languages' => new Zend_Db_Expr('ARRAY_TO_JSON(ARRAY_AGG("TRANSLATIONS"."LANGUAGE"))')]
			)
			->group([
				'NOTIFICATION_TEMPLATE.id',
				'NOTIFICATION_TEMPLATE_T.id',
			])
			->where($adp->quoteInto(
				'UPPER("NOTIFICATION_TEMPLATE_T"."LANGUAGE") = ?', strtoupper($lang)
			))
			->order('NOTIFICATION_TEMPLATE_T.PURPOSE')
			;
		return $query->query();
	}

	public function insert($data) {
		$templateId = parent::insert([ ]);

		foreach (Zend_Registry::get('config')->frontend->languages->toArray() as $lang) {
			$this->translations->insert([
				'TEMPLATE_ID' => $templateId,
				'LANGUAGE'    => $lang,
				'PURPOSE'     => $lang == $data['translation'] ? $data['PURPOSE'] : '',
				'SUBJECT'     => $lang == $data['translation'] ? $data['SUBJECT'] : '',
				'BODY'        => $lang == $data['translation'] ? $data['BODY']    : '',
			]);
		}
		return $templateId;
	}

	public function getOne($id, $lang=NULL) {
		if ($lang == null) {
			$lang = (new Zend_Session_Namespace('camac'))->translation;
		}
		$adp = $this->getAdapter();

		$query = $this->select()
			->setIntegrityCheck(false)
			->from('NOTIFICATION_TEMPLATE', ['TEMPLATE_ID' => 'id'])
			->joinLeft(
				'NOTIFICATION_TEMPLATE_T',
				$adp->quoteInto(
					'"NOTIFICATION_TEMPLATE"."id" = "NOTIFICATION_TEMPLATE_T"."TEMPLATE_ID" AND LOWER("LANGUAGE") = ?',
					strtolower($lang)
				),
				['PURPOSE' => 'PURPOSE', 'SUBJECT' => 'SUBJECT', 'BODY' => 'BODY', 'translation' => 'LANGUAGE']
			)
			->joinLeft(
				'NOTIFICATION_TEMPLATE_T AS TRANSLATIONS',
				'"NOTIFICATION_TEMPLATE"."id" = "TRANSLATIONS"."TEMPLATE_ID" AND "TRANSLATIONS"."SUBJECT" != \'\' AND "TRANSLATIONS".SUBJECT IS NOT NULL',
				['languages' => new Zend_Db_Expr('ARRAY_TO_JSON(ARRAY_AGG("TRANSLATIONS"."LANGUAGE"))')]
			)
			->group([
				'NOTIFICATION_TEMPLATE.id',
				'NOTIFICATION_TEMPLATE_T.id',
			])
			->where($adp->quoteInto(
				'NOTIFICATION_TEMPLATE.id = ?', $id
			));
		$res = $query->query()->fetchObject();

		// Workaround for when translation does not exist yet
		$res->translation = $lang;

		return $res;
	}

	public function deleteTemplate($id) {
		$adp = $this->getAdapter();
		$this->translations->delete($adp->quoteInto('"NOTIFICATION_TEMPLATE_T"."TEMPLATE_ID" = ?', $id));
		$this->delete($adp->quoteInto('"NOTIFICATION_TEMPLATE"."id" = ?', $id));
	}

	public function update($id, $data) {
		$translation = $data['translation'];

		$this->translations->update(
			[
				'PURPOSE'     => $data['PURPOSE'],
				'SUBJECT'     => $data['SUBJECT'],
				'BODY'        => $data['BODY'],
			],
			[
				$this->getAdapter()->quoteInto( 'TEMPLATE_ID = ?', $id),
				$this->getAdapter()->quoteInto( 'LANGUAGE    = ?', $translation),
			]
		);
	}
}
