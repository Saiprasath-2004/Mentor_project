import type { ReactNode } from "react";

interface AuthCardProps {
    children: ReactNode;
}

export default function AuthCard({
    children
}: AuthCardProps){
    return(
        <div
            className="
            w-full
            max-w-md
            rounded-2xl
            border
            border-slate-800
            bg-slate-900
            p-10
            shadow-2xl
            "
            >
            {children}
        </div>
    )
}