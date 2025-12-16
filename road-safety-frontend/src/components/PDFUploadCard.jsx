export default function PDFUploadCard({ onFileSelect }) {
  return (
    <div className="card">
      <h2>Upload PDF</h2>
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => onFileSelect(e.target.files[0])}
      />
    </div>
  );
}
