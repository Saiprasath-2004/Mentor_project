import { useState } from "react";
import { register } from "../services/auth.service";
import { useNavigate } from "react-router-dom";



import Card from "../../../components/ui/Card";
import Input from "../../../components/ui/Input";
import Button from "../../../components/ui/Button";


export default function RegisterPage() {
    const [username, setUsername] = useState("");

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const navigate = useNavigate();

    const handleRegister = async () => {

        try {

            await register({
                username,
                email,
                password,
            });

            navigate("/login");

        } catch (error) {
            console.error(error);
            alert("Registration failed");
        }

    };

    return (
        <Card className="max-w-md">

            <div className="space-y-6">

                <div className="space-y-2">

                    <h1 className="text-4xl font-bold text-slate-900">
                        Create Account
                    </h1>

                    <p className="text-slate-500">
                        Join Gen Pulse today.
                    </p>

                </div>

                <Input
                    label="Username"
                    placeholder="Enter username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />

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
                    placeholder="Create password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                <Button
                    type="button"
                    onClick={handleRegister}
                >
                    Create Account 
                </Button>

                <p className="text-center text-sm text-slate-500">

                    Already have an account?{" "}

                    <span
                        className="
                        cursor-pointer
                        font-semibold
                        text-violet-600
                        hover:text-violet-700
                        "
                        onClick={() => navigate("/login")}
                    >
                        Sign In
                    </span>

                </p>

            </div>

        </Card>
    );
};