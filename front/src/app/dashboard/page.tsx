"use client";

import { useEffect, useState } from "react";
import { fetchAuthSession, signOut } from "aws-amplify/auth";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const checkSession = async () => {
      try {
        const session = await fetchAuthSession();
        const idToken = session.tokens?.idToken;
        const claims = idToken?.payload;

        if (!idToken) {
          router.push("/login");
          return;
        }

        setUserEmail(typeof claims?.email === "string" ? claims.email : "Unknown User");
      } catch (err) {
        console.error("Session error:", err);
        router.push("/login");
      } finally {
        setLoading(false);
      }
    };
    checkSession();
  }, [router]);

  const handleLogout = async () => {
    await signOut();
    router.push("/login");
  };

  if (loading) {
    return (
      <div className="h-screen flex justify-center items-center bg-gray-900 text-white">
        <p>Loading your dashboard...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-96 text-center">
        <h1 className="text-3xl font-semibold mb-4">Welcome 👋</h1>
        <p className="text-lg mb-6">
          You’re logged in as <span className="font-bold">{userEmail}</span>
        </p>
        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 w-full py-2 rounded"
        >
          Sign Out
        </button>
      </div>
    </div>
  );
}