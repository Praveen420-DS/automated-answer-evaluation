import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  Users,
  Brain,
  FileText,
  Download
} from "lucide-react";

import {
  Bar,
  Doughnut,
  Line
} from "react-chartjs-2";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
);

export default function Analytics() {

  const [data, setData] = useState(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/analytics",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setData(res.data);

    } catch {

      toast.error("Unable to load analytics");

    }

  };

  if (!data)
    return (
      <div className="min-h-screen flex justify-center items-center">
        Loading...
      </div>
    );

  return (

    <div className="min-h-screen bg-gray-100">

      {/* Header */}

      <div className="bg-white shadow px-8 py-6 flex justify-between">

        <div>

          <h1 className="text-4xl font-bold">

            System Analytics

          </h1>

          <p className="text-gray-500 mt-2">

            Complete AI Evaluation Statistics

          </p>

        </div>

        <button
          className="bg-indigo-600 text-white px-6 py-3 rounded-xl flex gap-2 items-center"
        >

          <Download size={18}/>

          Export Report

        </button>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        {/* KPI Cards */}

        <div className="grid md:grid-cols-4 gap-6">

          <Card
            icon={<Users className="text-blue-600"/>}
            title="Students"
            value={data.students}
          />

          <Card
            icon={<FileText className="text-green-600"/>}
            title="Exams"
            value={data.exams}
          />

          <Card
            icon={<Brain className="text-purple-600"/>}
            title="AI Evaluations"
            value={data.aiEvaluations}
          />

          <Card
            icon={<Brain className="text-orange-600"/>}
            title="OCR Accuracy"
            value={`${data.ocrAccuracy}%`}
          />

        </div>

        {/* Charts */}

        <div className="grid lg:grid-cols-2 gap-8 mt-10">

          <div className="bg-white rounded-2xl shadow p-6">

            <h2 className="text-xl font-bold mb-5">

              Department Performance

            </h2>

            <Bar
              data={{
                labels:data.departments,
                datasets:[
                  {
                    label:"Average Marks",
                    data:data.departmentMarks,
                    backgroundColor:"#4F46E5"
                  }
                ]
              }}
            />

          </div>

          <div className="bg-white rounded-2xl shadow p-6">

            <h2 className="text-xl font-bold mb-5">

              Pass / Fail

            </h2>

            <Doughnut
              data={{
                labels:["Pass","Fail"],
                datasets:[
                  {
                    data:[
                      data.pass,
                      data.fail
                    ],
                    backgroundColor:[
                      "#22C55E",
                      "#EF4444"
                    ]
                  }
                ]
              }}
            />

          </div>

        </div>

        {/* Monthly Trend */}

        <div className="bg-white rounded-2xl shadow mt-10 p-6">

          <h2 className="text-xl font-bold mb-6">

            Monthly AI Evaluations

          </h2>

          <Line
            data={{
              labels:data.months,
              datasets:[
                {
                  label:"Evaluations",
                  data:data.evaluationTrend,
                  borderColor:"#4F46E5",
                  fill:false
                }
              ]
            }}
          />

        </div>

        {/* AI Metrics */}

        <div className="grid md:grid-cols-3 gap-6 mt-10">

          <Metric
            title="Average AI Similarity"
            value={`${data.averageSimilarity}%`}
          />

          <Metric
            title="Average OCR Time"
            value={`${data.averageOCRTime} sec`}
          />

          <Metric
            title="Average Evaluation Time"
            value={`${data.averageEvaluationTime} sec`}
          />

        </div>

      </div>

    </div>

  );

}

function Card({icon,title,value}){

  return(

    <div className="bg-white rounded-2xl shadow p-6">

      {icon}

      <p className="text-gray-500 mt-4">

        {title}

      </p>

      <h2 className="text-3xl font-bold">

        {value}

      </h2>

    </div>

  );

}

function Metric({title,value}){

  return(

    <div className="bg-white rounded-2xl shadow p-6">

      <h3 className="text-gray-500">

        {title}

      </h3>

      <p className="text-3xl font-bold mt-4">

        {value}

      </p>

    </div>

  );

}