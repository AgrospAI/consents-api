"use client";
import { createContext } from "react";
import Auth from "@/utils/entities/Auth";

const AuthProvider = createContext<Auth | undefined>(undefined);

export default AuthProvider;
