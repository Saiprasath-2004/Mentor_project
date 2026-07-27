    import { Outlet } from "react-router-dom";
    import { CheckCircle2 } from "lucide-react";
    import Logo from "../common/Logo";

    export default function AuthLayout() {

        return (

            <div
                className="
                min-h-screen
                bg-[#F7F8FC]
                grid
                grid-cols-1
                lg:grid-cols-[1.1fr_0.9fr]
                "
            >

                {/* Left */}

                <section
                    className="
                    relative
                    overflow-hidden

                    hidden
                    lg:flex
                    flex-col
                    justify-center

                    bg-gradient-to-br
                    from-indigo-700
                    via-violet-600
                    to-purple-500

                    px-16
                    py-12

                    text-white
                    "
                >
                    
                    <div
                        className="
                        absolute
                        -top-32
                        -left-32

                        h-80
                        w-80

                        rounded-full

                        bg-white/10

                        blur-3xl
                        "
                    />

                    <div
                        className="
                        absolute

                        bottom-0
                        right-0

                        h-96
                        w-96

                        rounded-full

                        bg-violet-400/20

                        blur-3xl
                        "
                    />
                    <div className="relative z-10">
                        <Logo />

                        <div className="mt-12 space-y-8">

                            <h2 className="text-5xl xl:text-6xl font-bold leading-tight">

                                Work smarter.

                                <br />

                                <span className="text-violet-200">

                                    Together.

                                </span>

                            </h2>

                            <p
                                className="
                                max-w-md
                                text-lg
                                leading-6
                                text-violet-100
                                "
                            >
                                Gen Pulse helps teams collaborate,
                                communicate in real time,
                                manage tasks,
                                and stay connected from anywhere.
                            </p>

                            <div className="mt-10 space-y-4">

                                {[
                                    "Real-time Direct Messaging",
                                    "Team Collaboration",
                                    "Task Management",
                                ].map((item) => (

                                    <div
                                        key={item}
                                        className="flex items-center gap-3"
                                    >

                                        <CheckCircle2
                                            size={20}
                                            className="text-violet-200"
                                        />

                                        <span className="text-violet-100">
                                            {item}
                                        </span>

                                    </div>

                                ))}

                            </div>

                        </div>
                    </div>

                </section>

                {/* Right */}

                <section
                    className="
                    flex
                    items-center
                    justify-center
                    px-8 py-12
                    "
                >

                    <Outlet />

                </section>
            </div>
        );
    }