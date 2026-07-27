import { useState } from "react";
import { useNavigate } from "react-router-dom";



import Card from "../../../components/ui/Card";
import Input from "../../../components/ui/Input";
import Button from "../../../components/ui/Button";

import { login } from "../services/auth.service"


export default function LoginPage() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const navigate = useNavigate()

    const handleLogin = async () => {

        try {
            const response = await login({
                email,
                password,
            });

            localStorage.setItem(
                "access_token",
                response.access_token
            );

            navigate("/chat");
        } catch (error) {
            console.error(error);
            alert("Invalid credentials");
        }
    };


    return (
            <Card className="max-w-md">

                <div className="space-y-6">

                    <div className="space-y-2">

                        <h1 className="text-4xl font-bold text-slate-900">
                            Welcome Back 👋
                        </h1>

                        <p className="text-slate-500">
                            Sign in to continue to Gen Pulse
                        </p>

                    </div>

                    <Input
                        label="Email"
                        type="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <Input
                        label="Password"
                        type="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <Button
                        type="button"
                        onClick={handleLogin}
                    >
                        Sign In 
                    </Button>

                    <p className="text-center text-sm text-slate-500">

                        Don't have an account?{" "}

                        <span
                            className="
                            cursor-pointer
                            font-semibold
                            text-violet-600
                            hover:text-violet-700
                            "
                            onClick={() => navigate("/register")}
                        >
                            Create Account
                        </span>

                    </p>

                </div>

            </Card>
    );
};