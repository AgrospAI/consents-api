import User from "@/lib/entities/User";

interface Auth {
  user?: User;
  setUser: (user: User) => void;
}

export default Auth;
