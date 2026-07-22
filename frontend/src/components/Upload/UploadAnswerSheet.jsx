export default function UploadAnswerSheet({ onChange }) { return <input type="file" accept=".pdf,image/*" multiple onChange={onChange} />; }
