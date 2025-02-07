import AuthContext from "@/context";
import { useContext } from "react";

export default function useUser() {
  const auth = useContext(AuthContext);

  if (!auth) {
    throw new Error("useUser must be used within a DashboardProvider");
  }

  return auth.user;
}
