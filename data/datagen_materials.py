import csv
import random
from faker import Faker

fake = Faker()

# Material categories and examples
material_categories = {
    "Electronics": [
        "Microchip", "Processor", "Circuit Board", "Capacitor", "Resistor", 
        "Transistor", "LED", "Sensor", "Memory Chip", "Integrated Circuit",
        "Semiconductor Wafer", "PCB", "Connector", "Oscillator", "Diode"
    ],
    "Chemicals": [
        "Active Pharmaceutical Ingredient", "Chemical Compound", "Polymer", 
        "Solvent", "Catalyst", "Reagent", "Additive", "Resin", "Adhesive",
        "Lubricant", "Coating", "Pigment", "Dye", "Surfactant", "Acid"
    ],
    "Metals": [
        "Steel Alloy", "Aluminum Sheet", "Copper Wire", "Titanium Rod", 
        "Brass Fitting", "Stainless Steel", "Bronze Casting", "Zinc Plate",
        "Magnesium Ingot", "Tungsten Carbide", "Nickel Coil", "Lead Plate"
    ],
    "Plastics": [
        "Polyethylene Pellet", "PVC Compound", "ABS Plastic", "Polycarbonate Sheet",
        "Nylon Fiber", "Polypropylene Resin", "Acrylic Panel", "PET Preform",
        "Polyurethane Foam", "Silicone Rubber", "TPE Compound", "EPS Bead"
    ],
    "Textiles": [
        "Cotton Fabric", "Polyester Yarn", "Nylon Mesh", "Wool Blend",
        "Silk Thread", "Linen Cloth", "Denim Fabric", "Felt Material",
        "Technical Textile", "Non-woven Fabric", "Kevlar Fiber", "Spandex"
    ],
    "Raw Materials": [
        "Crude Oil", "Natural Gas", "Iron Ore", "Bauxite", "Copper Concentrate",
        "Wood Pulp", "Silica Sand", "Limestone", "Gypsum", "Phosphate Rock",
        "Potash", "Sulfur", "Clay", "Graphite", "Lithium Carbonate"
    ],
    "Components": [
        "Precision Bearing", "Gear Assembly", "Hydraulic Cylinder", "Pump Housing",
        "Valve Body", "Motor Stator", "Compressor Rotor", "Heat Exchanger",
        "Filter Element", "Seal Kit", "Fastener Set", "Spring Assembly"
    ],
    "Packaging": [
        "Corrugated Box", "Plastic Container", "Glass Bottle", "Aluminum Can",
        "Label Stock", "Shrink Wrap", "Protective Foam", "Pallet",
        "Drum Container", "Flexible Pouch", "Clamshell Package", "Crate"
    ]
}

# Material prefixes and codes
prefixes = ["AX", "BX", "CX", "DX", "EX", "FX", "GX", "HX", "IX", "JX",
           "ALPHA", "BETA", "GAMMA", "DELTA", "OMEGA", "SIGMA", "ZETA",
           "TECH", "PRO", "ULTRA", "MEGA", "HYPER", "SUPER", "MAX",
           "ECO", "BIO", "NANO", "MICRO", "MACRO", "QUANTUM"]

suffixes = ["", "-A", "-B", "-C", "-PRO", "-PLUS", "-MAX", "-ULTRA", "-ECO", "-BIO"]

# Criticality levels with weights (High is less common but more critical)
criticality_levels = ["Low", "Medium", "High", "Critical"]
criticality_weights = [0.3, 0.4, 0.2, 0.1]  # Probability weights

# Generate supplier IDs (assuming we have suppliers from S001 to S1000)
supplier_ids = [f"S{str(i).zfill(3)}" for i in range(1, 1001)]

def generate_material_name(category, material_type):
    """Generate a realistic material name"""
    prefix = random.choice(prefixes)
    number = random.randint(1, 999)
    suffix = random.choice(suffixes)
    
    # Sometimes use technical numbering, sometimes use descriptive names
    if random.random() < 0.6:
        return f"{prefix}-{number}{suffix} {material_type}"
    else:
        descriptive_terms = [
            "High-Purity", "Precision", "Industrial-Grade", "Medical-Grade",
            "Food-Grade", "Military-Spec", "High-Temp", "Corrosion-Resistant",
            "UV-Stable", "Flame-Retardant", "Conductive", "Magnetic",
            "Optical", "Structural", "Thermal", "Electrical", "Mechanical"
        ]
        term = random.choice(descriptive_terms)
        return f"{term} {material_type}"

def generate_material_data(num_rows=1000):
    materials = []
    used_ids = set()
    
    for i in range(num_rows):
        # Generate unique material ID
        material_id = f"M{str(i+1).zfill(3)}"
        while material_id in used_ids:
            i += 1
            material_id = f"M{str(i+1).zfill(3)}"
        used_ids.add(material_id)
        
        # Select category and material type
        category = random.choice(list(material_categories.keys()))
        material_type = random.choice(material_categories[category])
        
        # Generate material name
        material_name = generate_material_name(category, material_type)
        
        # Select supplier (some suppliers provide multiple materials)
        supplied_by_id = random.choice(supplier_ids)
        
        # Assign criticality level with weighted probability
        criticality_level = random.choices(criticality_levels, weights=criticality_weights)[0]
        
        materials.append([material_id, material_name, supplied_by_id, criticality_level])
    
    return materials

def save_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['material_id', 'material_name', 'supplied_by_id', 'criticality_level'])
        writer.writerows(data)

# Generate 1000 rows
material_data = generate_material_data(1000)

# Save to CSV file
save_to_csv('materials.csv', material_data)

# Print first 20 rows as sample
print("First 20 rows of generated material data:")
print("material_id,material_name,supplied_by_id,criticality_level")
for i in range(20):
    print(','.join(material_data[i]))

# Print some statistics
print(f"\nGenerated {len(material_data)} material records")
print(f"Suppliers referenced: {len(set([row[2] for row in material_data]))}")
criticality_counts = {}
for row in material_data:
    level = row[3]
    criticality_counts[level] = criticality_counts.get(level, 0) + 1
print("Criticality level distribution:")
for level, count in criticality_counts.items():
    print(f"  {level}: {count} materials ({count/len(material_data)*100:.1f}%)")