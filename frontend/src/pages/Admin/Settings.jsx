import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  Building2,
  Mail,
  Shield,
  Save,
  Database,
  Wrench,
} from "lucide-react";

export default function Settings() {

  const [settings, setSettings] = useState({
    instituteName: "",
    instituteCode: "",
    email: "",
    smtpHost: "",
    smtpPort: "",
    jwtExpiry: 24,
    maintenanceMode: false,
    allowRegistration: true,
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/settings",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setSettings(res.data);

    } catch {
      toast.error("Unable to load settings");
    }
  };

  const handleChange = (e) => {

    setSettings({
      ...settings,
      [e.target.name]:
        e.target.type === "checkbox"
          ? e.target.checked
          : e.target.value,
    });

  };

  const saveSettings = async () => {

    try {

      const token = localStorage.getItem("token");

      await axios.put(
        "http://127.0.0.1:5000/api/admin/settings",
        settings,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      toast.success("Settings Saved");

    } catch {

      toast.error("Unable to Save");

    }

  };

  return (

    <div className="min-h-screen bg-gray-100">

      <div className="bg-white shadow px-8 py-6">

        <h1 className="text-4xl font-bold">

          System Settings

        </h1>

        <p className="text-gray-500 mt-2">

          Configure EvalAI platform

        </p>

      </div>

      <div className="max-w-5xl mx-auto py-10 space-y-8">

        {/* Institute */}

        <div className="bg-white rounded-2xl shadow p-8">

          <h2 className="text-2xl font-bold flex items-center gap-2">

            <Building2/>

            Institute

          </h2>

          <div className="grid md:grid-cols-2 gap-6 mt-6">

            <input
              name="instituteName"
              value={settings.instituteName}
              onChange={handleChange}
              placeholder="Institute Name"
              className="border rounded-xl p-3"
            />

            <input
              name="instituteCode"
              value={settings.instituteCode}
              onChange={handleChange}
              placeholder="Institute Code"
              className="border rounded-xl p-3"
            />

          </div>

        </div>

        {/* SMTP */}

        <div className="bg-white rounded-2xl shadow p-8">

          <h2 className="text-2xl font-bold flex items-center gap-2">

            <Mail/>

            Email Settings

          </h2>

          <div className="grid md:grid-cols-2 gap-6 mt-6">

            <input
              name="email"
              value={settings.email}
              onChange={handleChange}
              placeholder="Sender Email"
              className="border rounded-xl p-3"
            />

            <input
              name="smtpHost"
              value={settings.smtpHost}
              onChange={handleChange}
              placeholder="SMTP Host"
              className="border rounded-xl p-3"
            />

            <input
              name="smtpPort"
              value={settings.smtpPort}
              onChange={handleChange}
              placeholder="SMTP Port"
              className="border rounded-xl p-3"
            />

          </div>

        </div>

        {/* Security */}

        <div className="bg-white rounded-2xl shadow p-8">

          <h2 className="text-2xl font-bold flex items-center gap-2">

            <Shield/>

            Security

          </h2>

          <div className="mt-6">

            <label>JWT Expiry (Hours)</label>

            <input
              type="number"
              name="jwtExpiry"
              value={settings.jwtExpiry}
              onChange={handleChange}
              className="border rounded-xl p-3 w-full mt-2"
            />

          </div>

          <div className="flex justify-between mt-6">

            <span>Allow New Registration</span>

            <input
              type="checkbox"
              name="allowRegistration"
              checked={settings.allowRegistration}
              onChange={handleChange}
            />

          </div>

        </div>

        {/* Maintenance */}

        <div className="bg-white rounded-2xl shadow p-8">

          <h2 className="text-2xl font-bold flex items-center gap-2">

            <Wrench/>

            Maintenance

          </h2>

          <div className="flex justify-between mt-6">

            <span>Enable Maintenance Mode</span>

            <input
              type="checkbox"
              name="maintenanceMode"
              checked={settings.maintenanceMode}
              onChange={handleChange}
            />

          </div>

        </div>

        {/* Backup */}

        <div className="bg-white rounded-2xl shadow p-8">

          <h2 className="text-2xl font-bold flex items-center gap-2">

            <Database/>

            Backup & Restore

          </h2>

          <div className="flex gap-4 mt-6">

            <button className="bg-green-600 text-white px-6 py-3 rounded-xl">

              Backup Database

            </button>

            <button className="bg-orange-600 text-white px-6 py-3 rounded-xl">

              Restore Database

            </button>

          </div>

        </div>

        <button
          onClick={saveSettings}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-xl flex items-center gap-2"
        >

          <Save size={18}/>

          Save Settings

        </button>

      </div>

    </div>

  );

}