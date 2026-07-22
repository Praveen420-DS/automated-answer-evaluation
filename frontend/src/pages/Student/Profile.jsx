import { useEffect, useRef, useState } from "react";
import { Camera, Eye, EyeOff, GraduationCap, Landmark, LockKeyhole, Mail, Phone, Save, UserRound } from "lucide-react";
import toast from "react-hot-toast";
import api from "../../services/api";
import "./profile.css";

const API_ORIGIN = (import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api").replace(/\/api$/, "");

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [passwords, setPasswords] = useState({ currentPassword: "", newPassword: "" });
  const [showPassword, setShowPassword] = useState({ current: false, next: false });
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileInput = useRef(null);
  useEffect(() => { loadProfile(); }, []);

  async function loadProfile() {
    try { const response = await api.get("/student/profile"); setProfile(response.data.data); }
    catch { toast.error("Unable to load profile."); }
  }
  function updateProfile(event) { const { name, value } = event.target; setProfile((current) => ({ ...current, [name]: value })); }
  function updatePassword(event) { const { name, value } = event.target; setPasswords((current) => ({ ...current, [name]: value })); }
  function photoUrl(photo) { return photo ? `${API_ORIGIN}${photo}` : ""; }

  async function uploadPhoto(event) {
    const image = event.target.files?.[0];
    if (!image) return;
    if (!image.type.startsWith("image/")) { toast.error("Please choose an image file."); return; }
    if (image.size > 5 * 1024 * 1024) { toast.error("Choose an image smaller than 5 MB."); return; }
    try {
      setUploading(true);
      const formData = new FormData(); formData.append("photo", image);
      const response = await api.post("/student/profile/photo", formData, { headers: { "Content-Type": "multipart/form-data" } });
      setProfile((current) => ({ ...current, photo: response.data.photo }));
      toast.success("Profile photo saved.");
    } catch (error) { toast.error(error.response?.data?.message || "Unable to upload the photo."); }
    finally { setUploading(false); event.target.value = ""; }
  }
  async function saveProfile(event) {
    event.preventDefault();
    if (passwords.newPassword && !passwords.currentPassword) { toast.error("Enter your current password before choosing a new one."); return; }
    try {
      setSaving(true);
      const response = await api.put("/student/profile", { name: profile.name, mobile: profile.mobile, ...passwords });
      setProfile(response.data.data); setPasswords({ currentPassword: "", newPassword: "" }); toast.success(response.data.message || "Profile updated.");
    } catch (error) { toast.error(error.response?.data?.message || "Unable to save your changes."); }
    finally { setSaving(false); }
  }
  if (!profile) return <div className="profile-loading">Loading profile…</div>;
  const initials = profile.name?.trim()?.[0]?.toUpperCase() || "S";
  return <main className="profile-page"><section className="profile-card"><div className="profile-cover"><div className="profile-avatar">{profile.photo ? <img src={photoUrl(profile.photo)} alt="Profile" /> : initials}<button type="button" aria-label="Upload profile photo" onClick={() => fileInput.current?.click()} disabled={uploading}><Camera /></button><input ref={fileInput} type="file" accept="image/png,image/jpeg,image/webp" onChange={uploadPhoto} hidden /></div><h1>{profile.name || "Student"}</h1><span>{profile.role || "Student"}</span></div><form onSubmit={saveProfile}><div className="profile-fields"><Field label="Name" icon={UserRound}><input name="name" value={profile.name || ""} onChange={updateProfile} required /></Field><Field label="Email" icon={Mail}><input value={profile.email || ""} readOnly /></Field><Field label="Mobile" icon={Phone}><input name="mobile" value={profile.mobile || ""} onChange={updateProfile} placeholder="Add your mobile number" /></Field><Field label="Department" icon={GraduationCap}><input value={profile.department || "Not assigned"} readOnly /></Field><Field label="Year" icon={Landmark}><input value={profile.year || "Not assigned"} readOnly /></Field><PasswordField label="Current Password" name="currentPassword" value={passwords.currentPassword} show={showPassword.current} onChange={updatePassword} onToggle={() => setShowPassword((state) => ({ ...state, current: !state.current }))} placeholder="Required to set a new password" /><PasswordField label="New Password" name="newPassword" value={passwords.newPassword} show={showPassword.next} onChange={updatePassword} onToggle={() => setShowPassword((state) => ({ ...state, next: !state.next }))} placeholder="Leave empty if unchanged" /></div><div className="profile-save"><button disabled={saving}>{saving ? "Saving…" : <><Save /> Save Changes</>}</button></div></form></section></main>;
}

function Field({ label, icon: Icon, children }) { return <label className="profile-field"><span>{label}</span><div><Icon />{children}</div></label>; }
function PasswordField({ label, name, value, show, onChange, onToggle, placeholder }) { return <label className="profile-field"><span>{label}</span><div><LockKeyhole /><input type={show ? "text" : "password"} name={name} value={value} onChange={onChange} placeholder={placeholder} /><button type="button" onClick={onToggle} aria-label={`Show ${label}`}>{show ? <EyeOff /> : <Eye />}</button></div></label>; }
