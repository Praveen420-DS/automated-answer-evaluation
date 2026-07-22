<motion.div
    initial={{ opacity: 0, x: 100 }}
    animate={{ opacity: 1, x: 0 }}
    transition={{ duration: 1 }}
    className="relative flex items-center justify-center"
>

    {/* Background Glow */}

    <div className="absolute w-[650px] h-[650px] rounded-full bg-gradient-to-r from-purple-300/30 via-blue-300/20 to-indigo-300/30 blur-[140px]"></div>

    {/* Floating Robot */}

    <motion.img
        animate={{
            y: [-12, 12, -12],
        }}
        transition={{
            repeat: Infinity,
            duration: 5,
        }}
        src="/robot.png"
        alt="robot"
        className="relative z-20 w-[360px]"
    />

    {/* Answer Sheet */}

    <motion.img
        animate={{
            rotate: [-6, -2, -6],
            y: [-8, 8, -8],
        }}
        transition={{
            repeat: Infinity,
            duration: 4,
        }}
        src="/answersheet.png"
        className="absolute bottom-10 left-2 w-[260px] z-10"
    />

    {/* Scanner */}

    <motion.img
        animate={{
            y: [-10, 10, -10],
        }}
        transition={{
            repeat: Infinity,
            duration: 3,
        }}
        src="/scanner.png"
        className="absolute top-0 left-28 w-[220px]"
    />

    {/* OCR CARD */}

    <motion.div
        whileHover={{ scale: 1.05 }}
        className="absolute left-0 top-24
        bg-white/90 backdrop-blur-xl
        rounded-3xl
        shadow-2xl
        p-5
        w-56"
    >

        <h2 className="font-bold text-lg">

            OCR Processing

        </h2>

        <div className="mt-3 h-2 rounded-full bg-gray-200">

            <div className="w-4/5 h-full rounded-full bg-indigo-500"></div>

        </div>

        <p className="mt-3 text-gray-500">

            Handwriting Detected

        </p>

    </motion.div>

    {/* AI CARD */}

    <motion.div

        whileHover={{ scale: 1.05 }}

        className="absolute left-8 bottom-52
        bg-white
        rounded-3xl
        shadow-2xl
        p-5
        w-56"

    >

        <h2 className="font-bold text-lg">

            AI Evaluation

        </h2>

        <p className="text-5xl mt-4 font-black text-indigo-600">

            96%

        </p>

        <p className="text-gray-500">

            Confidence

        </p>

    </motion.div>

    {/* SCORE CARD */}

    <motion.div

        whileHover={{ scale: 1.05 }}

        className="absolute right-0 top-40
        bg-white
        rounded-3xl
        shadow-2xl
        p-5
        w-56"

    >

        <h2 className="font-bold">

            Score

        </h2>

        <div className="mt-6 flex justify-center">

            <div className="relative">

                <svg
                    width="120"
                    height="120"
                >

                    <circle
                        cx="60"
                        cy="60"
                        r="48"
                        stroke="#E5E7EB"
                        strokeWidth="10"
                        fill="none"
                    />

                    <circle
                        cx="60"
                        cy="60"
                        r="48"
                        stroke="#6366F1"
                        strokeWidth="10"
                        fill="none"
                        strokeDasharray="300"
                        strokeDashoffset="30"
                        strokeLinecap="round"
                    />

                </svg>

                <div className="absolute inset-0 flex items-center justify-center">

                    <span className="text-3xl font-bold">

                        92%

                    </span>

                </div>

            </div>

        </div>

    </motion.div>

    {/* Analytics */}

    <motion.div

        whileHover={{ scale: 1.05 }}

        className="absolute right-12 bottom-8
        bg-white
        rounded-3xl
        shadow-xl
        p-5
        w-52"

    >

        <h2 className="font-bold">

            Analytics

        </h2>

        <img

            src="/chart.png"

            className="mt-4"

        />

    </motion.div>

</motion.div>