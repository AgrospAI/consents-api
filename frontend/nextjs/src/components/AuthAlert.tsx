import React from "react";
import { Alert, AlertDescription, AlertTitle } from "./ui/alert";
import { CircleAlert } from "lucide-react";

function AuthAlert() {
  return (
    <Alert variant="destructive">
      <AlertTitle className="flex flex-row font-bold gap-x-2 align-middle">
        <CircleAlert className="size-4" /> Authorization warning
      </AlertTitle>
      <AlertDescription>
        Connect your wallet to access to your profile.
      </AlertDescription>
    </Alert>
  );
}

export default AuthAlert;
