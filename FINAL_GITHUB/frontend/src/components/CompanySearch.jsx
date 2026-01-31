import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { motion } from 'framer-motion';

const CompanySearch = () => {
    const [companyName, setCompanyName] = useState('');

    // Placeholder URL - you can update this later
    const baseUrl = 'http://localhost:7071/api/ScrapeScope3?company_name=';

    const handleSearch = (e) => {
        e.preventDefault();
        if (companyName.trim()) {
            // Format company name for URL (replace spaces with hyphens, lowercase)
            const formattedName = companyName.trim().toLowerCase().replace(/\s+/g, '-');
            const fullUrl = `${baseUrl}${formattedName}`;

            // Open the URL in a new tab
            window.open(fullUrl, '_blank');
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.8 }}
            className="w-full max-w-2xl mx-auto px-4 mt-12"
        >
            <form onSubmit={handleSearch} className="relative group">
                {/* Search Input Container */}
                <div className="relative">
                    <input
                        type="text"
                        placeholder="Search for a company..."
                        value={companyName}
                        onChange={(e) => setCompanyName(e.target.value)}
                        className="w-full px-6 py-4 pr-14 rounded-full border-2 border-border bg-card/50 backdrop-blur-sm text-foreground placeholder:text-muted-foreground text-lg focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all duration-300 shadow-lg hover:shadow-xl"
                    />

                    {/* Search Button */}
                    <button
                        type="submit"
                        className="absolute right-2 top-1/2 -translate-y-1/2 bg-primary hover:bg-primary/90 text-primary-foreground p-3 rounded-full transition-all duration-300 shadow-md hover:shadow-lg hover:scale-105 active:scale-95"
                        aria-label="Search"
                    >
                        <Search className="w-5 h-5" />
                    </button>
                </div>

                {/* Subtle hint text */}
                <p className="text-sm text-muted-foreground text-center mt-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    Enter a company name to view their carbon footprint
                </p>
            </form>
        </motion.div>
    );
};

export default CompanySearch;
