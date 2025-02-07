"use client";
import { createContext } from "react";
import Auth from "@/lib/entities/Auth";

const AuthContext = createContext<Auth | undefined>(undefined);

export default AuthContext;
