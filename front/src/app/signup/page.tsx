"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signUp, confirmSignUp } from "aws-amplify/auth";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [step, setStep] = useState<"signup" | "confirm">("signup");
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSignup = async () => {
    try {
      setLoading(true);
      await signUp({
        username: email,
        password,
        options: { userAttributes: { email } },
      });
      setStep("confirm");
    } catch (err: any) {
      alert(err.message || "Error signing up");
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = async () => {
    try {
      setLoading(true);
      await confirmSignUp({ username: email, confirmationCode: code });
      alert("✅ Signup confirmed! Redirecting to login...");
      setTimeout(() => router.push("/login"), 1500);
    } catch (err: any) {
      alert(err.message || "Error confirming signup");
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
      <div className="absolute top-1/2 left-10 transform -translate-y-1/2 flex gap-6 items-start">
        {/* Trigger Button */}
        {!showForm && (
          <button
            onClick={() => setShowForm(true)}
            className="px-8 py-3 rounded-xl font-semibold text-white bg-gradient-to-r from-[#0a0f2c] via-[#102a5c] to-[#1a3b7c] 
                       shadow-lg border border-white/10 backdrop-blur-md transition-all duration-300 
                       hover:scale-105 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(26,59,124,0.6)] hover:brightness-110"
          >
            Sign Up
          </button>
        )}

        {/* Pop-Up Signup Form */}
        <div
          className={`transition-all duration-500 ease-out ${
            showForm ? "opacity-100 scale-100" : "opacity-0 scale-95 pointer-events-none"
          } w-full max-w-md`}
        >
          <div className="bg-gray-800/70 backdrop-blur-md p-8 rounded-xl shadow-2xl border border-gray-700 text-white transition-transform duration-300 hover:scale-105 hover:shadow-[0_0_25px_rgba(255,255,255,0.3)]">
            <h2 className="text-3xl font-bold text-center mb-6 tracking-wide">Create Account</h2>

            {step === "signup" && (
              <>
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
                  onClick={handleSignup}
                  disabled={loading}
                  className={`w-full py-2 rounded-xl font-semibold text-white bg-gradient-to-r from-[#0a0f2c] via-[#102a5c] to-[#1a3b7c] 
                              shadow-lg border border-white/10 backdrop-blur-md transition-all duration-300 
                              ${loading ? "cursor-not-allowed opacity-60" : "hover:scale-105 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(26,59,124,0.6)] hover:brightness-110"}`}
                >
                  {loading ? "Signing Up..." : "Sign Up"}
                </button>
              </>
            )}

            {step === "confirm" && (
              <>
                <p className="text-sm mb-4 text-center">
                  Enter the verification code sent to your email.
                </p>
                <input
                  type="text"
                  placeholder="Verification Code"
                  className="w-full px-4 py-2 mb-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition"
                  onChange={(e) => setCode(e.target.value)}
                  value={code}
                />
                <button
                  onClick={handleConfirm}
                  disabled={loading}
                  className={`w-full py-2 rounded-xl font-semibold text-white bg-gradient-to-r from-green-900 via-green-700 to-green-600 
                              shadow-lg border border-white/10 backdrop-blur-md transition-all duration-300 
                              ${loading ? "cursor-not-allowed opacity-60" : "hover:scale-105 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(0,255,0,0.4)] hover:brightness-110"}`}
                >
                  {loading ? "Verifying..." : "Confirm Account"}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}