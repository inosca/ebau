<?php

require_once(APPLICATION_PATH . '/../library/mpdf/mpdf.php');

abstract class Docgen_TemplateController_PdfController extends Docgen_TemplateController_TemplateControllerAbstract {

	protected $mpdf;

	/**
	 * Extract path
	 *
	 * @var           string $extractPath
	 */
	protected $extractPath;

	/**
	 * The view
	 *
	 * @var           Zend_View $view
	 */
	protected $view;


	public function __construct() {
		parent::__construct();
		$this->mpdf = new mPDF('c');
		$this->mpdf->useOnlyCoreFonts = true;
		$this->view = new Zend_View();

	}

	/**
	 * Render the PDF
	 */
	public function render($template) {
		// temporarily unzip the template

		$this->extract($template);

		$this->assignTags();

		$this->assignContentToPdf();

		$path = "blubber"; // this will be ignored
		return $this->mpdf->Output($path, 's');
	}

	/**
	 * Assign the tags to the pdf
	 */
	protected function assignTags() {
		$data = array_merge(
			$this->questionTags,
			$this->getIndividualTags()
		);

		foreach ($data as $key => $date) {
			$this->view->$key = $date;
		}

		$this->view->extractPath = $this->extractPath;
	}

	/**
	 * Extract the zip
	 */
	protected function extract($template) {
		$zip = new ZipArchive();
		$config = Zend_Registry::get('config');

		$this->extractPath = sprintf("%s/%s", $config->tempdir, uniqid());
		mkdir($this->extractPath);

		$res = $zip->open($template);
		if ($res) {
			$zip->extractTo($this->extractPath);

			$zip->close();
		}
		else {
			throw new Exception(sprintf("%s could not be extracted", $template));
		}
	}

	/**
	 * @SuppressWarnings(short)
	 *
	 * http://stackoverflow.com/questions/3349753/delete-directory-with-files-in-it
	 */
	public function __destruct() {
		$it = new RecursiveDirectoryIterator($this->extractPath, RecursiveDirectoryIterator::SKIP_DOTS);
		$files = new RecursiveIteratorIterator($it,
					 RecursiveIteratorIterator::CHILD_FIRST);
		foreach($files as $file) {
			if ($file->getFilename() === '.' || $file->getFilename() === '..') {
				continue;
			}
			if ($file->isDir()){
				rmdir($file->getRealPath());
			} else {
				unlink($file->getRealPath());
			}
		}
		rmdir($this->extractPath);
	}

	/**
	 * Assign the content to the PDF
	 *
	 * Mostly this will consist of
		$this->view->addScriptPath(sprintf("%s/content/", $this->extractPath));
		$this->mpdf->WriteHtml($this->view->render('main.phtml'), 2);

		WriteHtml has modes:
		0 - Parses a whole html document
		1 - Parses the html as styles and stylesheets only
		2 - Parses the html as output elements only
		3 - (For internal use only - parses the html code without writing to document)
		4 - (For internal use only - writes the html code to a buffer)

	 */
	abstract protected function assignContentToPdf();
}
