export default function Logo() {
    return (
        <div className="flex items-center gap-4">

            <div
                className="
                flex
                h-14
                w-14
                items-center
                justify-center
                rounded-2xl
                bg-white/15
                backdrop-blur-md
                border
                border-white/20
                shadow-xl
                "
            >
                <span className="text-2xl font-bold text-white">
                    GP
                </span>
            </div>

            <div>

                <h1 className="text-3xl font-bold text-white">
                    Gen Pulse
                </h1>

                <p className="text-sm text-violet-100">
                    Connect. Collaborate. Deliver.
                </p>

            </div>

        </div>
    );
}