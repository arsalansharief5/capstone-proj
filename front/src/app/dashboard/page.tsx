"use client";

import { useState } from "react";
import { fetchAuthSession, signOut } from "aws-amplify/auth";
import { useRouter } from "next/navigation";

/* ---------------------------------------------
   Reusable Loader Overlay Component
---------------------------------------------- */
function LoaderOverlay({ message }: { message: string }) {
  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="flex flex-col items-center gap-4 p-8 bg-gray-900 rounded-2xl border border-gray-700 shadow-xl">
        <div className="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-lg text-gray-300 animate-pulse">{message}</p>
      </div>
    </div>
  );
}

/* ---------------------------------------------
   Main Component
---------------------------------------------- */
export default function ChatPage() {
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null);
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingAgent, setLoadingAgent] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const [result, setResult] = useState<string | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  /* -------------------- Sign Out -------------------- */
  const handleLogout = async () => {
    await signOut();
    router.push("/");
  };

  /* -------------------- Upload File -------------------- */
  const uploadVideo = async () => {
    if (!file) {
      alert("Please choose a file first.");
      return;
    }

    try {
      setLoadingUpload(true);
      setResult(null);

      const session = await fetchAuthSession();
      const token = session.tokens?.idToken?.toString();

      const res = await fetch(
        "https://capstone-django-777268942678.asia-south1.run.app/api/get-upload-url",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            file_name: file.name,
            content_type: file.type,
          }),
        }
      );

      const { upload_url, file_key } = await res.json();

      // Upload the actual file to S3
      await fetch(upload_url, {
        method: "PUT",
        headers: {
          "Content-Type": file.type,
        },
        body: file,
      });

      alert("Uploaded successfully!");
    } catch (err) {
      alert("Error: " + err);
    } finally {
      setLoadingUpload(false);
    }
  };

  /* -------------------- Fetch AI Agent Result -------------------- */
  const agentResult = async () => {
    try {
      setLoadingAgent(true);
      setResult(null);

      const session = await fetchAuthSession();
      const token = session.tokens?.idToken?.toString();

      const res = await fetch(
        "https://capstone-proj-777268942678.asia-south1.run.app/status",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await res.json();
      setResult(data.response);
    } catch (err) {
      console.log("Error fetching agent result:", err);
    } finally {
      setLoadingAgent(false);
    }
  };

  /* -------------------- Fetch Chat History -------------------- */
  const chatHistory = async () => {
    try {
      setLoadingHistory(true);

      const session = await fetchAuthSession();
      const token = session.tokens?.idToken?.toString();

      const res = await fetch(
        "https://capstone-django-777268942678.asia-south1.run.app/api/chat-history",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await res.json();
      setHistory(data);
      setShowHistory(true);
    } catch (err) {
      console.log(err);
    } finally {
      setLoadingHistory(false);
    }
  };

  /* -------------------- UI -------------------- */
  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center px-6 py-10">

      {/* Global Loaders */}
      {loadingUpload && <LoaderOverlay message="Uploading document…" />}
      {loadingAgent && <LoaderOverlay message="Analyzing with AI…" />}
      {loadingHistory && <LoaderOverlay message="Loading past analyses…" />}

      <main className="w-full max-w-3xl bg-gray-900 rounded-2xl p-10 shadow-xl border border-gray-800 relative">
        <h1 className="text-3xl font-bold mb-6 text-purple-400">
          Legal Document Analyzer ⚖️
        </h1>

        {/* File Upload */}
        <div className="space-y-4 mb-8">
          <input
            type="file"
            className="block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full 
            file:border-0 file:text-sm file:font-semibold file:bg-purple-600 file:text-white hover:file:bg-purple-700"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />

          <button
            onClick={uploadVideo}
            disabled={loadingUpload}
            className={`w-full py-2 rounded-lg bg-purple-600 hover:bg-purple-700 transition ${
              loadingUpload ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            {loadingUpload ? "Uploading..." : "Upload Document"}
          </button>
        </div>

        {/* Process Button */}
        <button
          onClick={agentResult}
          disabled={loadingAgent}
          className={`w-full py-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition mb-4 ${
            loadingAgent ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          {loadingAgent ? "Processing…" : "Get AI Analysis"}
        </button>

        {/* History Button */}
        <button
          onClick={chatHistory}
          disabled={loadingHistory}
          className={`w-full py-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition ${
            loadingHistory ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          {loadingHistory ? "Loading…" : "View Past Analyses"}
        </button>

        {/* AI Result */}
        {result && (
          <div className="mt-8 p-6 bg-gray-800 rounded-xl border border-gray-700 whitespace-pre-wrap">
            <h2 className="text-xl font-semibold mb-3 text-purple-300">
              AI Analysis Result
            </h2>
            {result}
          </div>
        )}

        {/* History Modal */}
        {showHistory && (
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-6 z-50">
            <div className="bg-gray-900 p-6 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto border border-gray-700">
              <h2 className="text-xl font-semibold text-purple-300 mb-4">
                Chat History
              </h2>

              {history.length === 0 ? (
                <p className="text-gray-400">No previous analyses found.</p>
              ) : (
                history.map((item, idx) => (
                  <div
                    key={idx}
                    className="mb-4 p-4 bg-gray-800 rounded-lg border border-gray-700"
                  >
                    <div className="text-xs text-gray-400 mb-2">
                      {item.timestamp}
                    </div>
                    <div className="font-bold text-purple-400 mb-1">
                      {item.file_key}
                    </div>
                    <div className="whitespace-pre-wrap">{item.response}</div>
                  </div>
                ))
              )}

              <button
                className="mt-4 w-full py-2 rounded-lg bg-red-600 hover:bg-red-700"
                onClick={() => setShowHistory(false)}
              >
                Close
              </button>
            </div>
          </div>
        )}

        {/* Sign Out */}
        <button
          onClick={handleLogout}
          className="mt-6 w-full text-xs bg-red-600 px-4 py-2 rounded hover:bg-red-700 transition"
        >
          Sign Out
        </button>
      </main>
    </div>
  );
}
