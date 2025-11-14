"use client";

import { useState } from "react";
import { fetchAuthSession, signOut } from "aws-amplify/auth";
import { useRouter } from "next/navigation";

export default function ChatPage() {
  const router = useRouter();
  const [query, setQuery] = useState("");

  const handleLogout = async () => {
    await signOut();
    router.push("/");
  };

  const testSecureEndpoint = async () => {
    try {
      const session = await fetchAuthSession();
      const token = session.tokens?.idToken?.toString();

      const res = await fetch(
        "https://ideal-giggle-5g4r6v46vrw42vpr4-8000.app.github.dev/api/secure-hello",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ text: query }),
        }
      );

      const data = await res.json();
      alert(JSON.stringify(data));
    } catch (err) {
      alert("Error: " + err);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex">

      {/* Just keeping your UI intact */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 relative">
        <h2 className="text-2xl font-semibold mb-6">What can I help with?</h2>

        <div className="flex items-center bg-gray-800 rounded-full px-4 py-2 w-full max-w-xl">
          <input
            type="text"
            placeholder="Ask anything"
            className="bg-transparent flex-1 text-white placeholder-gray-400 outline-none"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={testSecureEndpoint} className="px-4">
            Test Secure API
          </button>
        </div>

        <button
          onClick={handleLogout}
          className="mt-6 text-xs bg-purple-600 px-4 py-2 rounded hover:bg-purple-700 transition"
        >
          Sign Out
        </button>
      </main>
    </div>
  );
}
