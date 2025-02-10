import React from "react";
import { Alert, AlertDescription, AlertTitle } from "./ui/alert";
import { CircleAlert } from "lucide-react";

type Variant = "default" | "destructive";

interface Props {
  variant: Variant;
  message: string;
}

function AuthAlert({ variant, message }: Props) {
  return (
    <Alert variant={variant}>
      <AlertTitle className="flex flex-row font-bold gap-x-2 align-middle">
        <CircleAlert className="size-4" /> Authorization warning
      </AlertTitle>
      <AlertDescription>{message}</AlertDescription>
    </Alert>
  );
}

export default AuthAlert;
