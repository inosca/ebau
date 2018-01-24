<?php

/**
 * Document upload form. This form is not used for rendering, but just for validation.
 *
 */
class Documents_Data_SubmitUploadForm extends Camac_Form_Application {

	/**
	 * Save the instance ID of current form
	 *
	 * @var int
	 */
	private $instanceId;

	/**
	 * Constructor.
	 *
	 * @return void
	 */
	public function __construct($instanceId) {
		$this->instanceId = $instanceId;
		$this->addPrefixPath('Camac_Form_Element', 'Camac/Form/Element', 'element');

		$this->addButtons();

		// Add the elements to the form
		$this->addFormElements();

		parent::__construct();
	}

	/**
	 * Add the form elements
	 *
	 * @return void
	 */
	public function addFormElements() {
		$this->setAction(Zend_Controller_Front::getInstance()->getRequest()->getRequestUri());
		$this->setAttrib('enctype', 'multipart/form-data');
		$this->setMethod('post');

		$upload = $this->makeUploadElement();
		$this->addElement($upload);

		$this->addElement('submit', 'Upload', array(
			'label' => 'Hochladen',
			'class' => 'button upload'
		));
	}

	/**
	 * Create the upload element
	 *
	 * @return Zend_Form_Element_File
	 */
	protected function makeUploadElement() {
		$documentsLib = new Documents_Lib_DocumentLib();

		$upload = new Zend_Form_Element_File('file', array(
			'secure' => true
		));
		$extensions = array('PDF');
		$mimeTypeMap = array(
			'PDF' => 'application/pdf',
		);
		$upload->addValidator('Extension', false, $extensions)
				->addValidator('Size',     false, Zend_Registry::get('config')->attachment->upload_max_filesize)
				->addValidator('MimeType', false, array_map(function($extension) use ($mimeTypeMap) {
					return array_key_exists($extension, $mimeTypeMap) ? $mimeTypeMap[$extension]: null;
				}, $extensions))
				->setDestination($documentsLib->getUploadFolder($this->instanceId));

		return $upload;
	}
}
