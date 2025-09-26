import csv
import random
from faker import Faker

fake = Faker()

# Expanded datasets
countries_cities = {
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
    "China": ["Shanghai", "Beijing", "Shenzhen", "Guangzhou", "Chengdu", "Hangzhou", "Wuhan", "Xi'an", "Tianjin", "Nanjing"],
    "India": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur"],
    "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig"],
    "Japan": ["Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kyoto", "Kawasaki", "Saitama"],
    "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Suwon", "Ulsan", "Changwon", "Seongnam"],
    "Vietnam": ["Ho Chi Minh City", "Hanoi", "Da Nang", "Haiphong", "Can Tho", "Bien Hoa", "Thu Dau Mot", "Nha Trang", "Vung Tau", "Hue"],
    "Taiwan": ["Taipei", "New Taipei", "Taichung", "Kaohsiung", "Taoyuan", "Tainan", "Hsinchu", "Keelung", "Chiayi", "Changhua"],
    "Mexico": ["Mexico City", "Ecatepec", "Guadalajara", "Puebla", "Juárez", "Tijuana", "León", "Zapopan", "Monterrey", "Nezahualcóyotl"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"],
    "UK": ["London", "Birmingham", "Glasgow", "Liverpool", "Bristol", "Manchester", "Sheffield", "Leeds", "Edinburgh", "Leicester"],
    "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"],
    "Italy": ["Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari", "Catania"],
    "Canada": ["Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Kitchener"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Canberra", "Newcastle", "Wollongong", "Hobart"]
}

industries = [
    "Semiconductors", "Electronics", "Automotive", "Aerospace", "Pharmaceuticals",
    "Medical Devices", "Food & Beverage", "Chemicals", "Construction", "Textiles",
    "Apparel", "Logistics", "Shipping", "Manufacturing", "Steel & Metals",
    "Plastics", "Rubber", "Wood & Paper", "Mining", "Oil & Gas",
    "Renewable Energy", "Telecom", "Software", "Hardware", "Furniture",
    "Jewelry", "Toys", "Sports Equipment", "Agriculture", "Fishing"
]

company_types = [
    "Corp", "Inc", "Ltd", "Co", "Group", "Enterprises", "Industries", 
    "Solutions", "Systems", "Technologies", "International", "Global",
    "Manufacturing", "Trading", "Supply", "Distributors", "Ventures"
]

words = [
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Omega", "Sigma", "Quantum", "Precision", "Advanced", "Premium", "Elite",
    "Superior", "Excel", "Prime", "First", "National", "United", "Federal",
    "Central", "Pacific", "Atlantic", "Continental", "Worldwide", "Universal",
    "Innovative", "Creative", "Dynamic", "Strategic", "Reliable", "Trusted",
    "Quality", "Standard", "Professional", "Technical", "Digital", "Smart",
    "Eco", "Green", "Sustainable", "Modern", "New", "Next", "Future", "Vision",
    "Star", "Sun", "Moon", "Earth", "Ocean", "Mountain", "River", "Valley",
    "Eagle", "Lion", "Tiger", "Dragon", "Phoenix", "Pegasus", "Orion", "Apollo"
]

def generate_supplier_data(num_rows=1000):
    suppliers = []
    used_ids = set()
    
    for i in range(num_rows):
        # Generate unique supplier ID
        supplier_id = f"S{str(i+1).zfill(3)}"
        while supplier_id in used_ids:
            i += 1
            supplier_id = f"S{str(i+1).zfill(3)}"
        used_ids.add(supplier_id)
        
        # Generate company name
        name_word1 = random.choice(words)
        name_word2 = random.choice(words)
        while name_word2 == name_word1:
            name_word2 = random.choice(words)
        company_type = random.choice(company_types)
        supplier_name = f"{name_word1} {name_word2} {company_type}"
        
        # Select country and city
        country = random.choice(list(countries_cities.keys()))
        city = random.choice(countries_cities[country])
        
        # Select industry
        industry_type = random.choice(industries)
        
        suppliers.append([supplier_id, supplier_name, country, city, industry_type])
    
    return suppliers

def save_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['supplier_id', 'supplier_name', 'country', 'city', 'industry_type'])
        writer.writerows(data)

# Generate 1000 rows
supplier_data = generate_supplier_data(1000)

# Save to CSV file
save_to_csv('suppliers.csv', supplier_data)

# Print first 20 rows as sample
print("First 20 rows of generated data:")
print("supplier_id,supplier_name,country,city,industry_type")
for i in range(20):
    print(','.join(supplier_data[i]))