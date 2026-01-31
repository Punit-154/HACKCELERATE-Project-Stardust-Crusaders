import React from 'react';
import { Menu, X } from 'lucide-react';

const Navbar = () => {
    const [isOpen, setIsOpen] = React.useState(false);

    const navLinks = [
        { name: 'Home', href: '#home' },
        { name: 'Analysis', href: '#analysis' },
        { name: 'About Us', href: '#about' },
    ];

    return (
        <nav className="fixed top-0 w-full z-50">
            <div className="bg-primary pt-4 pb-2 relative">
                <div className="container mx-auto px-6 flex justify-between items-center text-primary-foreground">
                    {/* Logo or Text */}
                    <div className="text-2xl font-bold font-serif italic tracking-wider">
                        CL
                    </div>

                    {/* Desktop Menu */}
                    <div className="hidden md:flex space-x-8">
                        {navLinks.map((link) => (
                            <a
                                key={link.name}
                                href={link.href}
                                className="hover:text-amber-200 transition-colors duration-300 font-medium text-lg font-sans"
                            >
                                {link.name}
                            </a>
                        ))}
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="md:hidden">
                        <button onClick={() => setIsOpen(!isOpen)} className="focus:outline-none">
                            {isOpen ? <X size={28} /> : <Menu size={28} />}
                        </button>
                    </div>
                </div>

                {/* Mobile Menu Dropdown */}
                {isOpen && (
                    <div className="md:hidden absolute top-full left-0 w-full bg-primary shadow-lg py-4">
                        <div className="flex flex-col items-center space-y-4">
                            {navLinks.map((link) => (
                                <a
                                    key={link.name}
                                    href={link.href}
                                    className="text-primary-foreground text-lg font-medium"
                                    onClick={() => setIsOpen(false)}
                                >
                                    {link.name}
                                </a>
                            ))}
                        </div>
                    </div>
                )}
            </div>
            {/* Wavy Bottom using CSS clip-path or SVG. Using SVG for smoother wave */}
            <div className="w-full overflow-hidden leading-[0]">
                <svg
                    className="relative block w-[calc(110%+1.3px)] h-[50px] rotate-180"
                    data-name="Layer 1"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 1200 120"
                    preserveAspectRatio="none"
                >
                    <path
                        d="M985.66,92.83C906.67,72,823.78,31,743.84,14.19c-82.26-17.34-168.06-16.33-250.45.39-57.84,11.73-114,31.07-172,41.86A600.21,600.21,0,0,1,0,27.35V120H1200V95.8C1132.19,118.92,1055.71,111.31,985.66,92.83Z"
                        className="fill-primary"
                    ></path>
                </svg>
            </div>
        </nav>
    );
};

export default Navbar;
