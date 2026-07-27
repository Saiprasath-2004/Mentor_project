import type { ButtonHTMLAttributes } from "react";

interface ButtonProps
    extends ButtonHTMLAttributes<HTMLButtonElement> {
    children: React.ReactNode;
}

export default function Button({

    children,
    className = "",
    ...props
}: ButtonProps) {
    return (
        <button
            className={`
        
            w-full
            rounded-2xl
            bg-gradient-to-r
            from-violet-600
            to-indigo-600
            py-3.5
            font-semibold
            tracking-wide
            text-white
            shadow-lg
            transition-all
            duration-200
            hover:from-violet-700
            hover:to-indigo-700
            hover:shadow-xl
            active:scale-[.98]
            disabled:opacity-60
            ${className}
            `}

            {...props}
        >
            {children}
        </button>
    );
}