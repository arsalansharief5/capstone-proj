"use client";

import { Amplify } from "aws-amplify";

Amplify.configure(
  {
    Auth: {
      Cognito: {
        userPoolId: process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID!,
        userPoolClientId:
          process.env.NEXT_PUBLIC_COGNITO_USER_POOL_CLIENT_ID!,
        signUpVerificationMethod: "code",

        loginWith: {
          email: true,
          phone: false,
          username: false,
        },
      },
    },
  },
  { ssr: true }
);

export default function ConfigureAmplifyClientSide() {
  return null;
}
