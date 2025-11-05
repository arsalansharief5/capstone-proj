"use client";

import { useState } from "react";
import { useRouter } from "next/navigation"; // 👈 for navigation
import { signUp, confirmSignUp } from "aws-amplify/auth";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [step, setStep] = useState<"signup" | "confirm">("signup");
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
      // 👇 Redirect to login page after 2 seconds
      setTimeout(() => router.push("/login"), 1500);
    } catch (err: any) {
      alert(err.message || "Error confirming signup");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl mb-6 text-center font-semibold">Sign Up</h2>

        {step === "signup" && (
          <>
            <input
              type="email"
              placeholder="Email"
              className="w-full p-2 mb-3 bg-gray-700 rounded"
              onChange={(e) => setEmail(e.target.value)}
              value={email}
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full p-2 mb-3 bg-gray-700 rounded"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
            />
            <button
              onClick={handleSignup}
              disabled={loading}
              className={`${
                loading ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"
              } w-full py-2 rounded mt-2`}
            >
              {loading ? "Signing Up..." : "Sign Up"}
            </button>
          </>
        )}

        {step === "confirm" && (
          <>
            <p className="text-sm mb-3">
              Enter the verification code sent to your email.
            </p>
            <input
              type="text"
              placeholder="Verification Code"
              className="w-full p-2 mb-3 bg-gray-700 rounded"
              onChange={(e) => setCode(e.target.value)}
              value={code}
            />
            <button
              onClick={handleConfirm}
              disabled={loading}
              className={`${
                loading ? "bg-green-400" : "bg-green-600 hover:bg-green-700"
              } w-full py-2 rounded mt-2`}
            >
              {loading ? "Verifying..." : "Confirm Account"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
