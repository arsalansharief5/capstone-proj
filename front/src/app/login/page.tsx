"use client";

import { useState } from "react";
import { signIn, fetchAuthSession } from "aws-amplify/auth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [showLogin, setShowLogin] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    try {
      setLoading(true);
      await signIn({ username: email, password });
      const session = await fetchAuthSession();
      const token = session.tokens?.idToken?.toString();

      if (token) localStorage.setItem("cognito_token", token);

      alert("✅ Login successful!");
      router.push("/dashboard");
    } catch (err: any) {
      alert(err.message || "Error logging in");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center text-white px-4 relative"
      style={{ backgroundImage: "url('/background-image.jpg')" }}
    >
      {/* Left-aligned container */}
      <div className="absolute top-1/2 left-10 transform -translate-y-1/2 flex flex-row gap-6 items-start">
        {/* Dark Gradient Login Button with Reversed Direction */}
        {!showLogin && (
                <button
        onClick={() => setShowLogin(true)}
        className="px-8 py-3 rounded-xl font-semibold text-white bg-gradient-to-r from-[#0a0f2c] via-[#102a5c] to-[#1a3b7c] 
                    shadow-lg border border-white/10 backdrop-blur-md transition-all duration-300 
                    hover:scale-105 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(26,59,124,0.6)] hover:brightness-110"
        >
        Login
        </button>
        )}

        {/* Animated Login Form */}
        <div
          className={`transition-all duration-500 ease-out ${
            showLogin ? "opacity-100 scale-100" : "opacity-0 scale-95 pointer-events-none"
          } w-full max-w-md`}
        >
          <div className="bg-gray-800/70 backdrop-blur-md p-8 rounded-xl shadow-2xl border border-gray-700 text-white transition-transform duration-300 hover:scale-105 hover:shadow-[0_0_25px_rgba(255,255,255,0.3)]">
            <h2 className="text-3xl font-bold text-center mb-6 tracking-wide">Login</h2>

            <input
              type="email"
              placeholder="Email"
              className="w-full px-4 py-2 mb-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              onChange={(e) => setEmail(e.target.value)}
              value={email}
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full px-4 py-2 mb-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
            />

            <button
              onClick={handleLogin}
              disabled={loading}
              className={`w-full py-2 rounded-lg font-semibold transition ${
                loading
                  ? "bg-blue-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}