<?php

/**
 * Document upload form. This form is not used for rendering, but just for validation.
 *
 * @author Christian Zosel <christian.zosel@adfinis-sygroup.ch>
 */
class Documents_Data_UploadForm extends Camac_Form_Application {

	/**
	 * The instance ID
	 *
	 * @property int $instanceID
	 */
	private $instanceID;

	/**
	 * DocumentLib object
	 *
	 * @property Documents_Lib_DocumentLib $documentLib
	 */
	private $documentLib;

	/**
	 * Constructor.
	 *
	 * @return void
	 */
	public function __construct($instanceID) {
		$this->instanceID  = $instanceID;
		$this->documentLib = new Documents_Lib_DocumentLib();

		$this->addPrefixPath('Camac_Form_Element', 'Camac/Form/Element', 'element');

		$this->addButtons();

		parent::__construct();
	}

	/**
	 * Inizializes the form elements.
	 *
	 * @return void
	 */
	public function initForm() {
		$mapper = new Documents_Model_Mapper_AttachmentSection();

		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());
		$this->setAttrib('enctype', 'multipart/form-data');
		$this->setMethod('post');

		$this->addElement('CamacHidden', 'upload_target', array(
			'validators' => array(
				array('inArray', false, array('haystack' => array_map(function($section) {
					return $section->attachmentSectionID;
				}, $mapper->getEntries())))
			),
			'required' => true,
			'errorMessages' => array('Bitte füllen Sie das Feld "Hochladen nach" aus.')
		));

		// validation should be more thorough here - but getting the user list is implemented as a view helper :(
		$this->addElement('CamacHidden', 'upload_as', array(
			'secure' => true
		));

		$upload = new Zend_Form_Element_File('file', array(
			'secure' => true
		));
		$extensions = $this->documentLib->getAllowedExtensions();

		$upload->setMultiFile(5)
			->addValidator('Extension', false, $extensions)
			->addValidator('Size', false, Zend_Registry::get('config')->attachment->upload_max_filesize)
			->addValidator('MimeType', false, Custom_UriUtils::getMimeTypes($extensions))
			->setDestination($this->documentLib->getUploadFolder($this->instanceID));

		$this->addElement($upload);
	}

	public function initPortalForm() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());
		$this->setAttrib('enctype', 'multipart/form-data');
		$this->setMethod('post');

		$extensions = $this->documentLib->getAllowedExtensions();

		$upload = new Zend_Form_Element_File('file', array(
			'secure' => true
		));
		$upload->addValidator('Extension', false, $extensions)
			->addValidator('Size', false, Zend_Registry::get('config')->attachment->upload_max_filesize)
			->addValidator('MimeType', false, Custom_UriUtils::getMimeTypes($extensions));

		$this->addElement($upload);
	}

	public function initSubmitForm() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());
		$this->setAttrib('enctype', 'multipart/form-data');
		$this->setMethod('post');

		$extensions = $this->documentLib->getAllowedExtensions();
		$upload = new Zend_Form_Element_File('file', array(
			'secure' => true,
			'required' => true
		));
		$upload->addValidator('Extension', false, $extensions)
			->addValidator('Size', false, Zend_Registry::get('config')->attachment->upload_max_filesize)
			->addValidator('MimeType', false, Custom_UriUtils::getMimeTypes($extensions));

		$this->addElement($upload);

		$this->addElement('submit', 'Upload', array(
			'label' => 'Hochladen',
			'class' => 'button upload'
		));
	}
}
