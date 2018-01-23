<?php

class Documents_Lib_DocumentLib {

	/**
	 * Attachment mapper
	 *
	 * @var Documents_Model_Mapper_Attachment $attachmentMapper
	 */
	protected $attachmentMapper;

	/**
	 * Object for handling http file transfer
	 *
	 * @var Zend_File_Transfer_Adapter_Http $fileTransferHttp
	 */
	protected $fileTransferHttp;

	/**
	 * Class constructor
	 *
	 * @return void
	 */
	public function __construct() {
		$this->attachmentMapper = new Documents_Model_Mapper_Attachment();
		$this->fileTransferHttp = new Zend_File_Transfer_Adapter_Http();
	}

	/**
	 * Get uploaded / received files
	 *
	 * Returnes an array with file infos per file field:
	 * { 'fieldname' => { file infos } }
	 *
	 * @method getUploadedFiles
	 * @return array
	 */
	public function getUploadedFiles() {
		return $this->fileTransferHttp->getFileInfo();
	}

	/**
	 * Get file extension of a uploaded file
	 *
	 * @param string $sourceFieldname The upload field name
	 * @return string
	 */
	public function getFileExtension($sourceFieldname) {
		return strtolower(pathinfo(
			$this->fileTransferHttp->getFileName($sourceFieldname),
			PATHINFO_EXTENSION
		));
	}

	/**
	 * Get file name of a uploaded file (including extension)
	 *
	 * @param string $sourceFieldname The upload field name
	 * @return string
	 */
	public function getFileName($sourceFieldname) {
		return pathinfo(
			$this->fileTransferHttp->getFileName($sourceFieldname),
			PATHINFO_BASENAME
		);
	}


	/**
	 * Do the actual upload
	 *
	 * Save the file to the file system
	 * Add a new row to the database
	 *
	 * @param string $sourceFieldname The fieldname of the file input field
	 * @param int $instanceId The instance id
	 * @param int $userId The user id to save
	 * @param int $attachmentSectionId the id of the section to add the file to
	 * @param int $serviceId The service id
	 * @param string $targetFilename (optional) The destination filename
	 * @param bool $digitalSignature (optional) Flag if the file has a digital signature
	 * @return array Upload messages
	 */
	public function uploadFile(
		$sourceFieldname, $instanceId, $userId, $attachmentSectionId, $serviceId,
		$targetFilename = null, $digitalSignature = false, $isParcelPicture = false,
		$isConfidential = false
	) {
		if (!$this->fileTransferHttp->isUploaded($sourceFieldname) ||
			!$this->fileTransferHttp->isValid($sourceFieldname)
		) {
			throw new Exception('Upload failed');
		}

		if ($targetFilename === null) {
			$targetFilename = $this->fileTransferHttp->getFileName($sourceFieldname, false);
		}

		if (class_exists('Normalizer')) {
			$targetFilename = \Normalizer::normalize($targetFilename);
		}

		$path = sprintf(
			'%s/%s',
			$this->getUploadFolder($instanceId),
			$targetFilename
		);
		$sanitizedPath = self::getSanitizedPath($path);
		$this->fileTransferHttp->addFilter('Rename', $sanitizedPath);

		if ($this->fileTransferHttp->receive($sourceFieldname)) {
			$this->fileTransferHttp->setOptions(array('useByteString' => false));

			$size     = $this->fileTransferHttp->getFileSize($sourceFieldname);
			$mimeType = $this->fileTransferHttp->getMimeType($sourceFieldname);

			$attachment = new Documents_Model_Data_Attachment(
				null,
				$this->getSanitizedName($targetFilename),
				$instanceId,
				$sanitizedPath,
				$size,
				new DateTime('now'),
				$userId,
				md5(time() . $sanitizedPath . $size),
				$mimeType,
				$attachmentSectionId,
				$serviceId,
				$isParcelPicture,
				$digitalSignature,
				$isConfidential
			);

			$this->attachmentMapper->save($attachment);

			$extension = $this->getFileExtension($sourceFieldname);
			if (strtolower($extension) == 'pdf') {
				$this->createThumbnail($sanitizedPath, $attachment->identifier);
			}
		}

		$this->fileTransferHttp->removeFilter('Rename');

		return $this->fileTransferHttp->getMessages();
	}

	/**
	 * Delete an attachment file
	 *
	 * @param string $identifier The attachment identifier
	 * @return void
	 */
	public function deleteFile($identifier) {
		$attachment = $this->attachmentMapper->findByIdentifier($identifier);

		if (!unlink($attachment->path)) {
			Zend_Registry::get('log')->log(
				sprintf('Unable to delete attachment file "%s"', $attachment->path),
				Zend_Log::DEBUG
			);
			throw new Exception('Unable to delete attachment file');
		}

		$this->attachmentMapper->delete($attachment->attachmentID);

		$thumbnail = $this->thumbnailPath($identifier);
		if (file_exists($thumbnail) && !unlink($thumbnail)) {
			Zend_Registry::get('log')->log(
				sprintf('Unable to delete thumbnail "%s"', $thumbnail),
				Zend_Log::DEBUG
			);
			throw new Exception('Unable to delete thumbnail');
		}
	}

	/**
	 * Create a thumbnail from the given path
	 *
	 * @param string $path
	 * @param string $identifier
	 * @return void
	 */
	public function createThumbnail($path, $identifier) {
		$config    = Zend_Registry::get('config');
		$thumbPath = $this->thumbnailPath($identifier);
		$cmd       = sprintf($config->attachment->thumb_cmd, $path, $thumbPath);
		# TODO a bit of error handling might be nice here... man...
		exec($cmd);
	}

	/**
	 * Create if necessary and return the thumbnail path
	 *
	 * @param string $identifier
	 * @return string
	 */
	public function thumbnailPath($identifier) {
		$config    = Zend_Registry::get('config');
		$thumbLoc  = $config->attachment->thumb_path;
		$this->createFolderIfNotExist($thumbLoc);

		$thumbPath = sprintf("%s/%s.png", $thumbLoc, $identifier);

		return $thumbPath;
	}

	/**
	 * Create a folder if it doesn't exist, give permissions
	 *
	 * @param string $path
	 * @return void
	 */
	public function createFolderIfNotExist($path) {
		if (!is_dir($path)) {
			mkdir($path, 0777, true);
		}
	}

	/**
	 * Get filename from path, filtered by htmlspecialchars
	 *
	 * @param  string $path
	 * @return string
	 */
	public function getSanitizedName($path) {
		$pathInfo = pathinfo($path);

		if (!isset($pathInfo['filename']) || !isset($pathInfo['extension'])) {
			throw new Exception('Invalid filename or file extension');
		}

		return sprintf(
			"%s.%s",
			htmlspecialchars($pathInfo['filename']),
			$pathInfo['extension']
		);
	}

	/**
	 * Filter strange characters (just for storage) and add date
	 *
	 * @param  string $path
	 * @return string
	 */
	public function getSanitizedPath($path) {
		$pathInfo = pathinfo($path);

		if (!isset($pathInfo['filename']) || !isset($pathInfo['extension'])) {
			throw new Exception('Invalid filename or file extension');
		}

		$msecs = explode(' ', microtime());
		return sprintf(
			"%s/%s_%s%s.%s",
			$pathInfo['dirname'],
			mb_ereg_replace("([^\w\s\d\-_~,;\[\]\(\).])", '', $pathInfo['filename']),
			date('Y-m-d-His'),
			round($msecs[0] * 1000),
			$pathInfo['extension']
		);
	}

	/**
	 * Return the allowed file extensions
	 *
	 * @return array
	 */
	public function getAllowedExtensions() {
		$roleExtensionMapper    = new Documents_Model_Mapper_AttachmentExtensionRole();
		$serviceExtensionMapper = new Documents_Model_Mapper_AttachmentExtensionService();
		$extensionMapper        = new Documents_Model_Mapper_AttachmentExtension();

		$currentService = Zend_Auth::getInstance()->getIdentity()->CURRENT_SERVICE;
		$serviceExtensions = array();
		if ($currentService) {
			$serviceExtensions = $serviceExtensionMapper->getEntries(
				$currentService->getServiceId()
			);
		}
		$roleExtensions    = $roleExtensionMapper->getEntries(
			Zend_Auth::getInstance()->getIdentity()->CURRENT_ROLE->getRoleId()
		);

		$extensions = array();
		# WHERE ARE LIST COMPREHENSIONS
		foreach (array_merge($serviceExtensions, $roleExtensions) as $row) {
			$extensions[] = $extensionMapper->getEntry($row->attachmentExtensionID)->name;
		}

		return array_unique($extensions);
	}

	/**
	 * Return the upload folder for current instance
	 *
	 * @return string
	 */
	public function getUploadFolder($instanceId) {
		$uploadPath = Zend_Registry::get('config')->attachment->path .'/'. $instanceId;
		$this->createFolderIfNotExist($uploadPath);

		return $uploadPath;
	}
}
