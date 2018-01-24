<?php


class Documents_Model_Data_Attachment  {

	/**
	 * ATtachment ID
	 *
	 * @var           int $attachmentID
	 */
	public $attachmentID;

	/**
	 * Document name
	 *
	 * @var           string $name
	 */
	public $name;

	/**
	 * Instance ID
	 *
	 * @var           int $instanceID
	 */
	public $instanceID;


	/**
	 * Document path
	 *
	 * @var           string $path
	 */
	public $path;


	/**
	 * The size
	 *
	 * @var           int $size
	 */
	public $size;

	/**
	 * Date
	 * todo
	 *
	 * @var           date $date
	 */
	public $date;

	/**
	 * User ID
	 *
	 * @var           int $puserID
	 */
	public $userID;

	/**
	 * The identifyer hash
	 *
	 * @var           string $identifier
	 */
	public $identifier;

	/**
	 * Mime attachmentSectionID
	 *
	 * @var           string $mimeattachmentSectionID
	 */
	public $mimeattachmentSectionID;

	/**
	 * The attachmentSectionID
	 *
	 * The attachmentSectionID that denotes who is the originator of the file
	 *
	 * @var           int $attachmentSectionID
	 */
	public $attachmentSectionID;

	/**
	 * The Service ID
	 *
	 * @var int serviceID
	 */
	public $serviceID;

	/**
	 * Whether it's a parcel picture
	 *
	 * @var bool isParcelPicture
	 */
	public $isParcelPicture;

	/**
	 * Has the attachment a digital signature
	 *
	 * @var bool $digitalSignature
	 */
	public $digitalSignature;


	/**
	 * Is the attachment confidential?
	 *
	 * @var bool $digitalSignature
	 */
	public $isConfidential;

	/**
	 * @SuppressWarnings("Excessive")
	 */
	public function __construct(
		$attachmentID,
		$name,
		$instanceID,
		$path,
		$size,
		$date,
		$userID,
		$identifier,
		$mimeType,
		$attachmentSectionID,
		$serviceID,
		$isParcelPicture = false,
		$digitalSignature = false,
		$isConfidential = false
	) {
		$this->attachmentID        = $attachmentID;
		$this->name                = $name;
		$this->instanceID          = $instanceID;
		$this->path                = $path;
		$this->size                = $size;
		$this->date                = $date;
		$this->userID              = $userID;
		$this->identifier          = $identifier;
		$this->mimeType            = $mimeType;
		$this->attachmentSectionID = $attachmentSectionID;
		$this->serviceID           = $serviceID;
		$this->isParcelPicture     = $isParcelPicture;
		$this->digitalSignature    = $digitalSignature;
		$this->isConfidential      = $isConfidential;
	}

	public function getUserName() {
		$userMapper = new Camac_Model_DbTable_Account_User();

		$user = $userMapper->find($this->userID);

		return $user[0]->USERNAME;
	}

	public function getService() {
		$serviceMapper = new Application_Model_Mapper_Account_Service();

		if ($this->serviceID) {
			$service = $serviceMapper->getService($this->serviceID);

			return $service->getName();
		}
	}
}
