import type { InputHTMLAttributes } from "react";

interface InputProps
    extends InputHTMLAttributes<HTMLInputElement> {
    label: string;
}

export default function Input({

    label,
    className = "",
    ...props
}: InputProps) {

    return (
        <div className="space-y-2">
            <label
                className="
                text-sm
                font-medium
                text-gray-700
                "
            >
                {label}
            </label>

            <input
                className={`
                w-full
                rounded-xl
                border
                border-slate-200
                bg-white
                px-4
                py-4
                outline-none
                transition-all
                duration-200
                hover:border-violet-300
                focus:border-[#6D5EF5]
                focus:ring-4
                focus:ring-violet-200
                ${className}
                `}

                {...props}
            />
        </div>
    );
}