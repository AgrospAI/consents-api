import AuthProvider from "@/context/AuthProvider";
import { useContext } from "react";

export default function useUser() {
  const auth = useContext(AuthProvider);

  if (!auth) {
    throw new Error("useUser must be used within a DashboardProvider");
  }

  return auth.user;
}
