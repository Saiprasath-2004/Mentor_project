import clsx from "clsx";
import type {
    HTMLAttributes,
    ReactNode,
} from "react";

interface CardProps
    extends HTMLAttributes<HTMLDivElement> {
    children: ReactNode;
}

export default function Card({
    children,
    className,
    ...props
}: CardProps) {

    return (
        <div
            className={clsx(
                `
                w-full
                max-w-lg
                rounded-[32px]
                bg-white
                p-8
                shadow-[0_30px_80px_rgba(15,23,42,.10)]
                `,
                className
           )}
            {...props}
        >
            {children}
        </div>
    );
}