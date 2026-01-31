import React from 'react';
import { ArrowDown } from 'lucide-react';
import { motion } from 'framer-motion';
import CompanySearch from './CompanySearch';

const Hero = () => {
    return (
        <section id="home" className="h-screen w-full flex flex-col justify-center items-center relative bg-background overflow-hidden">

            {/* Background Decorative Elements */}
            <div className="absolute inset-0 z-0 opacity-10">
                <div className="absolute top-20 left-10 w-64 h-64 bg-primary rounded-full blur-[100px]"></div>
                <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent rounded-full blur-[120px]"></div>
            </div>

            <div className="z-10 text-center px-4">
                <motion.h1
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="text-8xl md:text-[10rem] font-heading text-primary drop-shadow-md"
                >
                    Carba Lens
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5, duration: 1 }}
                    className="mt-6 text-xl md:text-2xl font-serif text-muted-foreground italic max-w-2xl mx-auto"
                >
                    Visualizing the footprint of industry
                </motion.p>

                {/* Company Search Bar */}
                <CompanySearch />
            </div>

            {/* Down Arrow */}
            <motion.div
                className="absolute bottom-12 z-10 cursor-pointer"
                animate={{ y: [0, 10, 0] }}
                transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
                whileHover={{ scale: 1.1 }}
            >
                <a href="#analysis" className="bg-white/80 p-3 rounded-full shadow-lg border border-border backdrop-blur-sm block">
                    <ArrowDown className="text-primary w-8 h-8" />
                </a>
            </motion.div>

        </section>
    );
};

export default Hero;
