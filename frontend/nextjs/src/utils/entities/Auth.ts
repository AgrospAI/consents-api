import User from "@/utils/entities/User";

interface Auth {
  user?: User;
  setUser: (user: User) => void;
}

export default Auth;
