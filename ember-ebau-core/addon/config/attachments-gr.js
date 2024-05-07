export default {
  allowedMimetypes: [
    "image/png",
    "image/jpeg",
    "image/gif",
    "application/pdf",
    "image/vnd.dwg",
    // for dwg files, just the mimetype is not enough to list the files
    // by default in file upload dialog, so allow extension as well
    ".dwg",
  ],
};
