<?php

class Core_SimplelistController extends Camac_Controller_Action {
	private $koorColumns = array(
		'INSTANCE_ID'       => 'ID',
		'DOSSIER_NR'        => 'Dossier-Nr.',
		'KOOR'              => 'Koordinationsstelle',
		'KOOR_SHORT'        => 'Kurzname Koordinationsstelle',
		'FORM'              => 'Verfahren',
		'COMMUNITY'         => 'Gemeinde',
		'USER'              => 'Ersteller',
		'APPLICANT'         => 'Gesuchsteller',
		'INTENT'            => 'Vorhaben',
		'STREET'            => 'Strasse/Flurname',
		'STATE'             => 'Status',
		'STATE_DESCRIPTION' => 'Statusbeschreibung'
	);

	private $commColumns = array(
		'INSTANCE_ID'       => 'ID',
		'DOSSIER_NR'        => 'Dossier-Nr.',
		'FORM'              => 'Verfahren',
		'COMMUNITY'         => 'Gemeinde',
		'USER'              => 'Ersteller',
		'APPLICANT'         => 'Gesuchsteller',
		'INTENT'            => 'Vorhaben',
		'STREET'            => 'Strasse/Flurname',
		'STATE'             => 'Status',
		'STATE_DESCRIPTION' => 'Statusbeschreibung'
	);

	private $serviceColumns = array(
		'INSTANCE_ID' => 'ID',
		'DOSSIER_NR'  => 'Dossier-Nr.',
		'KOOR'        => 'Koordinationsstelle',
		'KOOR_SHORT'  => 'Kurzname Koordinationsstelle',
		'FORM'        => 'Verfahren',
		'DEADLINE'    => 'Frist',
		'COMMUNITY'   => 'Gemeinde',
		'APPLICANT'   => 'Gesuchsteller',
		'INTENT'      => 'Vorhaben',
		'STREET'      => 'Strasse/Flurname',
		'REASON'      => 'Grund',
		'CIRC_STATE'  => 'Status'
	);

	private $guestColumns = array(
		'DOSSIER_NR' => 'Dossier-Nr.',
		'COMMUNITY'  => 'Gemeinde',
		'APPLICANT'  => 'Gesuchsteller',
		'INTENT'     => 'Vorhaben',
		'STREET'     => 'Strasse/Flurname',
		'PARCEL_NR'  => 'Parzelle'
	);

	public function init() {
		$contextSwitch = $this->_helper->getHelper('contextSwitch');
		$contextSwitch->addContext('xls', array(
					'suffix' => 'xls',
					'headers' => array(
						'Content-type' => 'application/vnd.ms-excel',
						'Content-Disposition' => 'inline; filename=list.xls'
					)
				)
			)
			->addActionContext('index', 'xls')
			->initContext();

		$this->isGuest = Custom_UriUtils::isPublicPage($this->_request->getParam('resource-id'), null);
		$this->isComm = Custom_UriUtils::getCurrentRole() == Custom_UriConstants::ROLE_COMMUNITY;
		$this->isService = Custom_UriUtils::isService();
	}

	private function getColumns ($resource) {
		if ($this->isGuest) {
			return $this->guestColumns;
		}
		if ($this->isComm) {
			return $this->commColumns;
		}
		if ($this->isService && !self::isServiceAsKoor($resource)) {
			return $this->serviceColumns;
		}
		return $this->koorColumns;
	}

	public function indexAction() {
		$resourceId = (int) $this->getRequest()->getParam('resource-id');
		$orderColumnIndex = (int) $this->getRequest()->getParam('column', 1);
		$order = $this->getRequest()->getParam('order');
		$page = (int) $this->_getParam('page', 1);

		if (!in_array($order, array("ASC", "DESC"))) {
			$order = "ASC";
		}

		$mapper = new Core_Resource_Simplelist_Mapper();
		$resource = $mapper->getResource($resourceId);

		$query = Core_Model_ListModel::getQueryByRole($resource);
		if (!$query) {
			throw new Exception('Access denied');
		}

		$columns = $this->getColumns($resource);

		$headerColumns = array_values($columns);
		$columns = array_keys($columns);
		// Reset the column index if trying to edit the url with an arbitrary value greater than the number of columns
		if ($orderColumnIndex < 0 || $orderColumnIndex > count($columns)) {
			$orderColumnIndex = 0;
		}

		$orderColumn = $columns[$orderColumnIndex];

		$db = Zend_Controller_Front::getInstance()->getParam("bootstrap")->getResource("db");
		// Add the ORDER BY cluase
		$query .= ' ORDER BY "' . $orderColumn . '" ' . $order;
		$rows = $db->query($query)->fetchAll();

		$paginator = Zend_Paginator::factory($rows);
		$paginator->setItemCountPerPage(Zend_Registry::get('config')->paginator->list->itemsPerPage);
		// Display all the rows if the list is exported as xls
		if ($this->_helper->contextSwitch()->getCurrentContext() == 'xls') {
			$paginator->setItemCountPerPage(0);
		}
		$paginator->setCurrentPageNumber($page);

		$this->view->paginator = $paginator;
		$this->view->orderColumn = $headerColumns[$orderColumnIndex];
		$this->view->order = $order;
		$this->view->columns = $columns;
		$this->view->headerColumns = $headerColumns;
		$this->view->isGuest = $this->isGuest;
		$this->view->isService = $this->isService;

		$this->view->isCirculation = Core_Model_ListModel::isCirculation($resource->getName());

		// Hack: Render special "In Zirkulation" lists of services as normal lists
		if (self::isServiceAsKoor($resource)) {
			$this->view->isService = false;
		}
	}

	private function isServiceAsKoor($resource) {
		return Custom_UriUtils::getCurrentRole() == Custom_UriConstants::ROLE_SERVICE &&
			Core_Model_ListModel::isCirculation($resource->getName());
	}

}
