"""
Report Generator
Generates comprehensive emission reports and identifies top 5 lowest-emission entities
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class ReportGenerator:
    """Generate emission reports and rankings"""
    
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]
        self.emissions_dir = self.base_dir / "data" / "emissions"
        self.reports_dir = self.base_dir / "data" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def load_aggregated_data(self) -> List[Dict]:
        """Load aggregated emission data"""
        file_path = self.emissions_dir / "aggregated_emissions.json"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Aggregated emissions file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return data
    
    def rank_entities(self, aggregated_data: List[Dict], ascending: bool = True) -> List[Dict]:
        """Rank entities by combined Materials and Transport emissions (excluding Energy)"""
        
        # Calculate combined metric for sorting
        for entity in aggregated_data:
            entity['ranking_emissions'] = (
                entity.get('materials_emissions_kg_co2e', 0) + 
                entity.get('transport_emissions_kg_co2e', 0)
            )
            
        sorted_data = sorted(
            aggregated_data,
            key=lambda x: x['ranking_emissions'],
            reverse=not ascending
        )
        
        # Add rank
        for idx, entity_data in enumerate(sorted_data, 1):
            entity_data['rank'] = idx
        
        return sorted_data
    
    def get_top_n_lowest(self, n: int = 5) -> List[Dict]:
        """Get top N entities with lowest combined (materials + transport) emissions"""
        aggregated_data = self.load_aggregated_data()
        ranked_data = self.rank_entities(aggregated_data, ascending=True)
        
        # Get top N
        top_n = ranked_data[:min(n, len(ranked_data))]
        
        return top_n
    
    def generate_detailed_report(self, top_entities: List[Dict]) -> str:
        """Generate detailed human-readable report"""
        
        report_lines = []
        report_lines.append("="*70)
        report_lines.append("CARBON FOOTPRINT REPORT")
        report_lines.append(f"Top 5 Entities with Lowest Emissions (Materials + Transport)")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("="*70)
        
        for entity_data in top_entities:
            rank = entity_data['rank']
            entity = entity_data['entity']
            # Using the combined metric we calculated
            combined_total = entity_data['ranking_emissions']
            materials = entity_data['materials_emissions_kg_co2e']
            transport = entity_data['transport_emissions_kg_co2e']
            
            report_lines.append(f"\n{'='*70}")
            report_lines.append(f"RANK #{rank}: {entity}")
            report_lines.append(f"{'='*70}")
            report_lines.append(f"Total Relevant Footprint: {combined_total:.2f} kg CO2e")
            report_lines.append(f"\nBreakdown by Category:")
            report_lines.append(f"  • Materials:  {materials:>10.2f} kg CO2e ({(materials/combined_total*100) if combined_total > 0 else 0:.1f}%)")
            report_lines.append(f"  • Transport:  {transport:>10.2f} kg CO2e ({(transport/combined_total*100) if combined_total > 0 else 0:.1f}%)")
            
            # Detailed breakdown
            breakdown = entity_data['breakdown']
            
            if breakdown['materials']:
                report_lines.append(f"\n  Materials Details:")
                for item in breakdown['materials']:
                    report_lines.append(f"    - {item['material']}: {item['weight_kg']} kg -> {item['emissions_kg_co2e']:.2f} kg CO2e")
            
            if breakdown['transport']:
                report_lines.append(f"\n  Transport Details:")
                for item in breakdown['transport']:
                    mode_info = f"via {item['mode']}"
                    if item['mode'] == 'intermodal':
                         mode_info += f" ({len(item.get('legs', []))} legs)"
                    
                    tonne_km = item.get('tonne_km', 0)
                    emissions = item.get('emissions_kg_co2e', 0)
                    
                    report_lines.append(f"    - {item['product']} {mode_info}: {tonne_km:.2f} t*km -> {emissions:.2f} kg CO2e")
        
        report_lines.append(f"\n{'='*70}")
        report_lines.append("END OF REPORT")
        report_lines.append("="*70)
        
        return "\n".join(report_lines)
    
    def save_reports(self):
        """Generate and save all reports"""
        
        print("\n" + "="*60)
        print("GENERATING REPORTS")
        print("="*60)
        
        # Get top 5 lowest emission entities (Materials + Transport)
        top_5_lowest = self.get_top_n_lowest(5)
        
        # Save JSON report
        json_report_path = self.reports_dir / "top_5_lowest_emissions.json"
        with open(json_report_path, 'w') as f:
            json.dump(top_5_lowest, f, indent=4)
        
        print(f"[OK] JSON report saved: {json_report_path}")
        
        # Generate and save detailed text report
        detailed_report = self.generate_detailed_report(top_5_lowest)
        text_report_path = self.reports_dir / "top_5_lowest_emissions_report.txt"
        with open(text_report_path, 'w') as f:
            f.write(detailed_report)
        
        print(f"[OK] Detailed report saved: {text_report_path}")
        
        # Print to console
        print("\n" + detailed_report)
        
        return top_5_lowest
    
    def generate_summary_stats(self):
        """Generate overall summary statistics (Materials + Transport optimized)"""
        aggregated_data = self.load_aggregated_data()
        
        total_entities = len(aggregated_data)
        
        total_materials = sum(e.get('materials_emissions_kg_co2e', 0) for e in aggregated_data)
        total_transport = sum(e.get('transport_emissions_kg_co2e', 0) for e in aggregated_data)
        
        # Total now reflects only Materials + Transport
        total_emissions = total_materials + total_transport
        
        avg_emissions = total_emissions / total_entities if total_entities > 0 else 0
        
        summary = {
            "total_entities": total_entities,
            "total_emissions_kg_co2e": round(total_emissions, 2),
            "average_emissions_kg_co2e": round(avg_emissions, 2),
            "category_totals": {
                "materials": round(total_materials, 2),
                "transport": round(total_transport, 2)
            }
        }
        
        summary_path = self.reports_dir / "summary_statistics.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=4)
        
        print(f"\n[STATS] Summary statistics saved: {summary_path}")
        
        return summary


def generate_reports():
    """Main function to generate all reports"""
    generator = ReportGenerator()
    top_5 = generator.save_reports()
    summary = generator.generate_summary_stats()
    return top_5, summary


if __name__ == "__main__":
    generate_reports()
