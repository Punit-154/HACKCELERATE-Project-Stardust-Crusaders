import React, { useEffect, useState } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell
} from 'recharts';
import { ArrowRight, Loader2, AlertTriangle } from 'lucide-react';

const API_URL = "http://localhost:5000/api/rankings/all";

const RankingDashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(API_URL);
                if (!response.ok) throw new Error('Failed to fetch data');
                const result = await response.json();

                // Transform data for charts if needed
                // Assuming result structure: { materials: [...], transport: [...] }
                setData(result);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return (
        <div className="flex justify-center items-center h-96">
            <Loader2 className="animate-spin h-10 w-10 text-primary" />
        </div>
    );

    if (error) return (
        <div className="flex flex-col justify-center items-center h-96 text-destructive">
            <AlertTriangle className="h-10 w-10 mb-4" />
            <p>Error loading data. Please ensure the Python API server is running.</p>
        </div>
    );

    return (
        <section id="analysis" className="py-20 bg-background min-h-screen">
            <div className="container mx-auto px-6">
                <h2 className="text-4xl md:text-5xl font-serif text-center mb-16 text-foreground border-b-2 border-primary/20 pb-4 inline-block mx-auto">
                    Emission Analysis
                </h2>

                {/* Materials Section */}
                <div className="mb-24">
                    <h3 className="text-3xl font-sans font-bold mb-8 text-primary">Materials Ranking</h3>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

                        {/* Left: Text Ranking */}
                        <div className="space-y-4">
                            <div className="bg-card p-6 rounded-lg shadow-lg border border-border">
                                <table className="w-full text-left">
                                    <thead>
                                        <tr className="border-b border-border">
                                            <th className="py-2 font-serif text-muted-foreground">Rank</th>
                                            <th className="py-2 font-serif text-muted-foreground">Material</th>
                                            <th className="py-2 font-serif text-muted-foreground text-right">CO2e (kg)</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {data.materials.map((item, index) => (
                                            <tr key={index} className="hover:bg-muted/50 transition-colors">
                                                <td className="py-3 font-bold text-accent-foreground text-lg">#{item.rank}</td>
                                                <td className="py-3 font-medium">{item.material}</td>
                                                <td className="py-3 text-right font-mono">{Number(item.emissions).toFixed(2)}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                            <p className="text-muted-foreground italic text-sm mt-4">
                                * Top 5 materials by emission volume.
                            </p>
                        </div>

                        {/* Right: Bar Graph */}
                        <div className="h-[400px] w-full bg-card p-4 rounded-lg shadow-lg border border-border">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={data.materials} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="oklch(var(--border))" horizontal={false} />
                                    <XAxis type="number" hide />
                                    <YAxis type="category" dataKey="material" width={100} tick={{ fill: 'oklch(var(--foreground))' }} />
                                    <Tooltip
                                        cursor={{ fill: 'oklch(var(--muted)/0.2)' }}
                                        contentStyle={{ backgroundColor: 'oklch(var(--card))', borderColor: 'oklch(var(--border))', borderRadius: '8px' }}
                                    />
                                    <Bar dataKey="emissions" radius={[0, 4, 4, 0]}>
                                        {data.materials.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={index === 0 ? 'oklch(var(--destructive))' : 'oklch(var(--chart-1))'} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* Transport Section */}
                <div>
                    <h3 className="text-3xl font-sans font-bold mb-8 text-secondary-foreground">Transport Ranking</h3>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

                        {/* Left: Text Ranking */}
                        <div className="space-y-4">
                            <div className="bg-card p-6 rounded-lg shadow-lg border border-border">
                                <table className="w-full text-left">
                                    <thead>
                                        <tr className="border-b border-border">
                                            <th className="py-2 font-serif text-muted-foreground">Rank</th>
                                            <th className="py-2 font-serif text-muted-foreground">Mode</th>
                                            <th className="py-2 font-serif text-muted-foreground text-right">CO2e (kg)</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {data.transport.map((item, index) => (
                                            <tr key={index} className="hover:bg-muted/50 transition-colors">
                                                <td className="py-3 font-bold text-secondary-foreground text-lg">#{item.rank}</td>
                                                <td className="py-3 font-medium capitalize">{item.mode}</td>
                                                <td className="py-3 text-right font-mono">{Number(item.emissions).toFixed(2)}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* Right: Bar Graph */}
                        <div className="h-[400px] w-full bg-card p-4 rounded-lg shadow-lg border border-border">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={data.transport} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="oklch(var(--border))" horizontal={false} />
                                    <XAxis type="number" hide />
                                    <YAxis type="category" dataKey="mode" width={100} tick={{ fill: 'oklch(var(--foreground))', textTransform: 'capitalize' }} />
                                    <Tooltip
                                        cursor={{ fill: 'oklch(var(--muted)/0.2)' }}
                                        contentStyle={{ backgroundColor: 'oklch(var(--card))', borderColor: 'oklch(var(--border))', borderRadius: '8px' }}
                                    />
                                    <Bar dataKey="emissions" radius={[0, 4, 4, 0]}>
                                        {data.transport.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={index === 0 ? 'oklch(var(--destructive))' : 'oklch(var(--chart-2))'} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

            </div>
        </section>
    );
};

export default RankingDashboard;
