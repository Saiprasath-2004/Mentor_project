import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Authlayout from "../components/layout/AuthLayout";
import MainLayout from "../components/layout/MainLayout";

import LoginPage from "../features/auth/pages/LoginPage";
import RegisterPage from "../features/auth/pages/RegisterPage";

import ChatPage from "../features/chat/pages/ChatPage";


export default function AppRouter() {
    return(
        <BrowserRouter> 
            <Routes>
                <Route element={<Authlayout/>}>
                    <Route path="login" element={<LoginPage />}/>
                    <Route path="register" element={<RegisterPage />}/>
                </Route>
                <Route element={<MainLayout />}>
                    <Route path="/chat" element={<ChatPage />} />
                </Route>

                <Route path="*" element={<Navigate to="/login" replace />}/>
            </Routes>
            
        </BrowserRouter>
    )
}