import React from 'react';
import { Leaf, Globe, TrendingUp } from 'lucide-react';

const AboutUs = () => {
    const features = [
        {
            icon: <Leaf className="w-8 h-8 text-primary" />,
            title: "Environmental Impact",
            description: "Tracking carbon footprints to encourage sustainable material choices."
        },
        {
            icon: <Globe className="w-8 h-8 text-accent" />,
            title: "Global Supply Chain",
            description: "Analyzing transport emissions across air, sea, and land networks."
        },
        {
            icon: <TrendingUp className="w-8 h-8 text-chart-2" />,
            title: "Data-Driven Insights",
            description: "Providing actionable rankings to optimize industrial processes."
        }
    ];

    return (
        <section id="about" className="py-20 bg-muted/30">
            <div className="container mx-auto px-6">
                <div className="max-w-4xl mx-auto text-center">
                    <h2 className="text-4xl font-serif text-foreground mb-8">About Carba Lens</h2>
                    <p className="text-xl text-muted-foreground leading-relaxed mb-16">
                        We are dedicated to illuminating the invisible environmental costs of modern industry.
                        Through precise calculation and transparent visualization, Carba Lens empowers organizations to make conscious decisions for a greener future.
                    </p>

                    <div className="grid md:grid-cols-3 gap-8">
                        {features.map((feature, idx) => (
                            <div key={idx} className="bg-card p-6 rounded-lg shadow-sm border border-border flex flex-col items-center">
                                <div className="mb-4 p-3 bg-muted rounded-full">
                                    {feature.icon}
                                </div>
                                <h3 className="text-lg font-bold mb-2 font-sans">{feature.title}</h3>
                                <p className="text-muted-foreground text-sm">
                                    {feature.description}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="mt-20 pt-8 border-t border-border text-center text-muted-foreground font-mono text-sm">
                    &copy; {new Date().getFullYear()} Carba Lens. All rights reserved.
                </div>
            </div>
        </section>
    );
};

export default AboutUs;
