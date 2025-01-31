import random
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import calendar  

# Initialize game state
state = {
    "countryName": "",
    "year": 2025,
    "month": 1,
    "popularity": 50,
    "gdp": 15000000,
    "growth": 0.02,
    "medianIncome": 1,
    "meanIncome": 1,
    "lowIncome": 0.5,
    "mediumIncome": 1,
    "highIncome": 1.5,
    "disposableIncome": 1,
    "gdpPerCapita": 1000,
    "interestRate": 0.01,
    "inflation": 0.01,
    "population": 15000,
    "lowIncomePopulation": 50,
    "mediumIncomePopulation": 50,
    "highIncomePopulation": 50,
    "numberOfCompanies": 10,
    "crime": 1,
    "taxBurden": 0,
    "lowIncomeTax": 0,
    "mediumIncomeTax": 0,
    "highIncomeTax": 0,
    "companyTax": 0,
    "salesTax": 0,
    "totalRevenue": 0,
    "healthSpending": 0,
    "educationSpending": 0,
    "policeSpending": 0,
    "defenceSpending": 0,
    "pensionSpending": 0,
    "subsidies": 0,
    "totalSpending": 0,
    "deficit": 0,
    "debt": 0,
    "stockIndex": 100,
    "businessConfidence": 0.8,
    "baseGrowth": 0.02,
    "previous_population": 150,
    "history": [],
}

state['sectors'] = {
    "automobile": {"gdpContribution": state['gdp'] * 0.1, "growth": 0.03, "subsidy": 0},
    "internet": {"gdpContribution": state['gdp'] * 0.02, "growth": 0.08, "subsidy": 0},
    "software": {"gdpContribution": state['gdp'] * 0.14, "growth": 0.07, "subsidy": 0},
    "oil": {"gdpContribution": state['gdp'] * 0.15, "growth": 0.02, "subsidy": 0},
    "farming": {"gdpContribution": state['gdp'] * 0.1, "growth": 0.01, "subsidy": 0},
    "evcar": {"gdpContribution": state['gdp'] * 0.05, "growth": 0.07, "subsidy": 0},
    "banking": {"gdpContribution": state['gdp'] * 0.15, "growth": 0.02, "subsidy": 0},
    "tourism": {"gdpContribution": state['gdp'] * 0.2, "growth": 0.03, "subsidy": 0},
    "construction": {"gdpContribution": state['gdp'] * 0.08, "growth": 0.05, "subsidy": 0},
    "space": {"gdpContribution": state['gdp'] * 0.01, "growth": 0.12, "subsidy": 0},
}

events = {
    "pandemic": {
        "description": "There has been a global pandemic!",
        "effects": {
            "gdpMultiplier": 0.95,
            "populationGrowth": -0.04,
            "stockImpact": -0.1
        }
    },
    "stock_crash": {
        "description": "The stock market crashed!",
        "effects": {
            "gdpMultiplier": 0.98,
            "businessConfidence": -0.05,
            "stockImpact": -0.3
        }
    },
    "economic_boom": {
        "description": "The economy is booming!",
        "effects": {
            "gdpMultiplier": 1.05,
            "baseGrowth": 0.03,
            "stockImpact": 0.03,
            "businessConfidence": 0.04
        }
    },
    "foreign_investment": {
        "description": "Companies are starting to invest in your country!",
        "effects": {
            "gdpMultiplier": 1.06,
            "baseGrowth": 0.04,
            "stockImpact": 0.08,
            "businessConfidence": 0.04
        }
    },
    "global_recession": {
        "description": "There has been a global recession!",
        "effects": {
            "gdpMultiplier": 0.93,
            "baseGrowth": -0.02,
            "stockImpact": -0.1,
            "businessConfidence:": -0.09
        }
    }
}

def trigger_event():
    event_name = random.choice(list(events.keys()))
    event = events[event_name]
    print(f"\nEvent: {event_name.replace('_', ' ').capitalize()} - {event['description']}")

    effects = event['effects']
    state['gdp'] *= effects.get("gdpMultiplier", 1) 
    state['baseGrowth'] = max(0.02, state['baseGrowth'] + effects.get("baseGrowth", 0))  # Reset to 2% minimum
    state['businessConfidence'] += effects.get("businessConfidence", 0)
    state['stockIndex'] *= (1 + effects.get("stockImpact", 0))
    state['population'] = int(state['population'] * (1 + effects.get("populationGrowth", 0)))

def save_game():
    filename = "autosave.json"
    with open(filename, "w") as file:
        json.dump(state, file)

def list_save_files():
    save_files = [f for f in os.listdir() if f.endswith(".json")]
    save_files.sort(key=os.path.getmtime, reverse=True)
    return save_files[:10]

def load_game():
    save_files = list_save_files()
    if not save_files:
        print("No save files found.")
        return

    print("Available save files:")
    for i, file in enumerate(save_files):
        print(f"{i + 1}: {file}")

    try:
        choice = int(input("Select a file to load (number): ")) - 1
        if 0 <= choice < len(save_files):
            filename = save_files[choice]
            global state
            with open(filename, "r") as file:
                state = json.load(file)
            if 'month' not in state:
                state['month'] = 1

            print(f"Game loaded from {filename}.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")


def display_stats():
    deficit_percent = (state['deficit'] / state['gdp']) * 100 if state['gdp'] > 0 else 0
    print(f"Year: {state['year']}")
    print(f"GDP: ${state['gdp']:.2f}, GDP Per Capita: ${state['gdpPerCapita']:.2f}")
    print(f"Population: {state['population']:.2f} (Low: {state['lowIncomePopulation']:.2f}, Medium: {state['mediumIncomePopulation']:.2f}, High: {state['highIncomePopulation']:.2f})")
    print(f"Pensioners: {state.get('pensioners', 0)}")
    print(f"Unemployment Rate: {state.get('unemploymentRate', 0) * 100:.2f}%")
    print(f"Crime: {state['crime']:.2f}/1000, Inflation: {state['inflation'] * 100:.2f}%")
    print(f"Disposable Income: ${state['disposableIncome']:.2f}")
    print(f"Popularity: {state['popularity']:.2f}%")
    debt_percent = (state['debt'] / state['gdp']) * 100 if state['gdp'] > 0 else 0
    print(f"Debt: ${state['debt']:.2f} ({debt_percent:.2f}% of GDP), Deficit: {deficit_percent:.2f}% of GDP")

    print(f"Stock Index: {state['stockIndex']:.2f}")

    # Dynamically list available stats for graphing
    available_stats = list(state['history'][0].keys()) if state['history'] else []
    print(f"Available stats for graphing: {', '.join(available_stats)} (type 'none' to exit)")
    option = input("Enter a stat to view its graph: ").strip()

    if option in available_stats:
        values = [entry[option] for entry in state['history']]
        ylabel = option.capitalize().replace("_", " ")
        title = f"{ylabel} Over Time"

        # Convert dates into fractional years (e.g., 2024.08 for August 2024)
        month_mapping = {
            "January": 0,
            "February": 1,
            "March": 2,
            "April": 3,
            "May": 4,
            "June": 5,
            "July": 6,
            "August": 7,
            "September": 8,
            "October": 9,
            "November": 10,
            "December": 11,
        }
        dates = [
            int(entry['date'].split(" ")[1]) + month_mapping[entry['date'].split(" ")[0].strip(",")] / 12.0
            for entry in state['history']
        ]

        # Plot the data
        plt.plot(dates, values, marker='o', markersize=1)

        # Set the x-axis to show only years as labels
        start_year = int(state['history'][0]['date'].split(" ")[1])
        end_year = int(state['history'][-1]['date'].split(" ")[1])
        ticks = range(start_year, end_year + 1)

        ax = plt.gca()
        ax.set_xticks(ticks)  # Set ticks for each year
        ax.set_xticklabels([str(year) for year in ticks])  # Display years as labels

        # Add labels and title
        plt.title(title)
        plt.xlabel("Year")
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.show()

    elif option != "none":
        print(f"Invalid stat. Available stats are: {', '.join(available_stats)}")


def manage_taxes():
    # Calculate total tax revenue as a percentage of GDP
    taxRevenue = (
        (state['lowIncomeTax'] * state['lowIncome'] * state['lowIncomePopulation']) +
        (state['mediumIncomeTax'] * state['mediumIncome'] * state['mediumIncomePopulation']) +
        (state['highIncomeTax'] * state['highIncome'] * state['highIncomePopulation']) +
        (state['companyTax'] * state['gdp'] * 0.2) +  # Assume 20% of GDP is taxable corporate income
        (state['salesTax'] * state['gdp'] * 0.5)      # Assume 50% of GDP is subject to sales tax
    )
    state['taxBurden'] = (taxRevenue / state['gdp'])  # Tax burden 

    print("Welcome to the tax department! Your current tax burden is {:.2f}%".format(state['taxBurden'] * 100))
    print("SELECT: income, company, sales")
    tax = input("> ")
    try:
        if tax == "income":
            print("What income tax bracket would you like to change?")
            print("SELECT: low, medium, high")
            incometax = input("> ")
            if incometax == "low":
                state['lowIncomeTax'] = float(input("Set low income tax (current: {:.2f}%): > ".format(state['lowIncomeTax'] * 100))) / 100
            elif incometax == "medium":
                state['mediumIncomeTax'] = float(input("Set medium income tax (current: {:.2f}%): > ".format(state['mediumIncomeTax'] * 100))) / 100
            elif incometax == "high":
                state['highIncomeTax'] = float(input("Set high income tax (current: {:.2f}%): > ".format(state['highIncomeTax'] * 100))) / 100
        elif tax == "company":
            state['companyTax'] = float(input("Set company tax (current: {:.2f}%): > ".format(state['companyTax'] * 100))) / 100
        elif tax == "sales":
            state['salesTax'] = float(input("Set sales tax (current: {:.2f}%): > ".format(state['salesTax'] * 100))) / 100
    except Exception as e:
        print("Error: "+str(e))

def manage_spending():
    try:
        print("Welcome to the spending department! Current spending is {:.2f}% of GDP.".format(state['totalSpending'] / state['gdp'] * 100))
        print("SELECT: health, education, police, defence, pension, subsidies")
        spending = input("> ")
        if spending == "health":
            state['healthSpending'] = float(input("Set health spending (current: {:.2f}%): > ".format(state['healthSpending'] * 100))) / 100
        elif spending == "education":
            state['educationSpending'] = float(input("Set education spending (current: {:.2f}%): > ".format(state['educationSpending'] * 100))) / 100
        elif spending == "police":
            state['policeSpending'] = float(input("Set police spending (current: {:.2f}%): > ".format(state['policeSpending'] * 100))) / 100
        elif spending == "defence":
            state['defenceSpending'] = float(input("Set defence spending (current: {:.2f}%): > ".format(state['defenceSpending'] * 100))) / 100
        elif spending == "pension":
            state['pensionSpending'] = float(input("Set pension spending (current: {:.2f}%): > ".format(state['pensionSpending'] * 100))) / 100
        elif spending == "subsidies":
            print("Available sectors to subsidise: ")
            for sector in state['sectors']:
                print(f"- {sector} (Current GDP: ${state['sectors'][sector]['gdpContribution']:,})")
            
            sector_choice = input("Enter the sector to subsidise: > ").strip().lower()

            if sector_choice in state['sectors']:
                current_gdp = state['sectors'][sector_choice]['gdpContribution']
                subsidy = float(input(f"Enter subsidy amount in dollars for {sector_choice} (Current GDP: ${current_gdp:.2f}): > "))
                diminishing_factor = 1 / (1 + subsidy / (current_gdp + 1))  # Diminishes more smoothly
                gdp_boost = subsidy * 0.1 * diminishing_factor
                state['sectors'][sector_choice]['gdpContribution'] += gdp_boost  # Add only the calculated GDP boost
                subsidy_total = sum(sector['subsidy'] for sector in state['sectors'].values())
                state['totalSpending'] += subsidy_total  # Add total subsidies to spending
                gdp_boost = subsidy * 0.1 * max(0, 1 - (subsidy / (state['sectors'][sector_choice]['gdpContribution'] + 1)))  # Calculate boost
                print(f"Subsidy of ${subsidy:.2f} applied to {sector_choice}, boosting its GDP contribution by approximately ${gdp_boost:.2f}.")
  
            else:
                print("Invalid sector. No subsidies applied.")
                
    except Exception as e:
        print("Error: "+str(e))
    
def adjust_finance():
    try:
        print(f"Current interest rate: {state['interestRate'] * 100:.2f}%")
        interest_payment = state['debt'] * state['interestRate']
        print(f"Annual interest payment on debt: ${interest_payment:.2f}")
        new_rate = float(input("Set a new interest rate (as a percentage, e.g., 2.5): > ")) / 100
        state['interestRate'] = max(-1, new_rate)  # Ensure interest rate doesn't go below -1
        print(f"Interest rate updated to {state['interestRate'] * 100:.2f}%.")
    except Exception as e:
        print("Error: "+str(e))

def next_month():
    state['previous_population'] = state['population']

    if 'month' not in state:
        state['month'] = 1  # Initialize the month field if not present

    state['month'] += 1
    if state['month'] > 12:
        state['month'] = 1
        state['year'] += 1

    # Trigger an event (10% chance)
    if random.random() < 0.05:
        trigger_event()

    # Calculate derived stats
    state['pensioners'] = int(state['population'] * 0.15)
    workforce = state['population'] - state['pensioners']
    unemployment_rate = 0.1 + (0.2 - state['educationSpending']) * 0.05 - state['numberOfCompanies'] * 0.001
    state['unemploymentRate'] = max(0, min(1, unemployment_rate))

    # Revenue calculation
    state['totalRevenue'] = (
        (state['lowIncomeTax'] * state['lowIncome'] * state['lowIncomePopulation']) +
        (state['mediumIncomeTax'] * state['mediumIncome'] * state['mediumIncomePopulation']) +
        (state['highIncomeTax'] * state['highIncome'] * state['highIncomePopulation']) +
        (state['companyTax'] * state['gdp'] * 0.2) +
        (state['salesTax'] * state['gdp'] * 0.5)
    )

    # Spending calculation
    state['totalSpending'] = (
        state['healthSpending'] * state['gdp'] +
        state['educationSpending'] * state['gdp'] +
        state['policeSpending'] * state['gdp'] +
        state['defenceSpending'] * state['gdp'] +
        state['pensionSpending'] * state['pensioners'] +
        state['subsidies'] * state['gdp']
    )

    # Deficit and debt adjustments
    monthly_deficit = (state['totalSpending'] - state['totalRevenue']) / 12

    state['deficit'] = monthly_deficit
    
    if state['deficit'] > 0:
        state['debt'] += state['deficit']
        
    state['debt'] += monthly_deficit

     # GDP growth calculations
    investment = state['companyTax'] * -0.1 + state['educationSpending'] * 0.2
    trade_balance = state['salesTax'] * -0.05

    # Gradually reset base growth toward the default value (0.02)
    default_base_growth = 0.02
    reset_rate = 0.1
    state['baseGrowth'] += (default_base_growth - state['baseGrowth']) * reset_rate

    # Add boom-bust cycles
    base_growth = state['baseGrowth'] + (0.01 * random.uniform(-0.5, 0.5))

    # Adjust investment and trade balance to scale realistically
    investment = max(-0.01, min(0.05, state['companyTax'] * -0.05 + state['educationSpending'] * 0.1))
    trade_balance = max(-0.02, min(0.02, state['salesTax'] * -0.03))

    interest_penalty = state['interestRate'] * 0.15
    growth = base_growth + investment + trade_balance - state['unemploymentRate'] * 0.05 - state['inflation'] * 0.03 - interest_penalty
    growth = max(-0.2, min(0.2, growth))  # Cap growth between -2% and 20%
    state['growth'] = growth

    # Adjust sector growth rates dynamically
    sector_gdp = sum(data['gdpContribution'] for data in state['sectors'].values())

    for sector, data in state['sectors'].items():
        # Distribute growth proportionally
        sector_share = data['gdpContribution'] / sector_gdp if sector_gdp > 0 else 0
        sector_growth = state['growth'] * sector_share

        # Add variability and subsidy effects
        variability = random.uniform(-0.02, 0.02)
        subsidy_effect = (data['subsidy'] * 0.1) * (1 - min(1, data['subsidy'] / (data['gdpContribution'] + 1)))
        adjusted_growth = sector_growth + variability + subsidy_effect

        # Update sector GDP contribution
        data['gdpContribution'] += data['gdpContribution'] * adjusted_growth
        data['gdpContribution'] = int(max(0, data['gdpContribution']))  # Prevent negative contributions

    # Recalculate total GDP and ensure total growth matches
    sector_gdp = sum(data['gdpContribution'] for data in state['sectors'].values())
    state['gdp'] = int(max(1, sector_gdp))


    # Update stock index with stronger ties to GDP growth and a boom/bust cycle
    volatility = random.uniform(-0.03, 0.03)  # Slightly increased range for volatility
    growth_impact = state['growth'] * 0.3  # Stock index tied more strongly to GDP growth
    boom_bust = random.uniform(-0.02, 0.02) if state['growth'] > 0 else random.uniform(-0.05, 0.05)  # Amplify busts during negative growth

    state['stockIndex'] *= (1 + growth_impact + boom_bust + volatility)
    state['stockIndex'] = max(0, state['stockIndex'])  # Ensure stock index doesn't drop below 0



    inflation_adjustment = state['interestRate'] * -0.1  + state['subsidies'] * 0.02
    monthly_inflation = inflation_adjustment / 12
    state['inflation'] += monthly_inflation
    state['inflation'] = max(-0.03, state['inflation'])  # Min -3% inflation


    # Update population
    population_growth = 0.01 + state['healthSpending'] * 0.02 - state['pensioners'] / state['population'] * 0.01
    monthly_population_growth = population_growth / 12
    state['population'] = state['population'] * (1 + monthly_population_growth)

    # Update income distribution
    state['lowIncomePopulation'] = int(state['population'] * 0.3 - (state['educationSpending'] * 0.05 * state['population']))
    state['mediumIncomePopulation'] = int(state['population'] * 0.5 + (state['educationSpending'] * 0.03 * state['population']))
    state['highIncomePopulation'] = state['population'] - (state['lowIncomePopulation'] + state['mediumIncomePopulation'])

    # Update income
    state['lowIncome'] = 0.5 * state['gdpPerCapita']
    state['mediumIncome'] = 1 * state['gdpPerCapita']
    state['highIncome'] = 1.5 * state['gdpPerCapita']
    
    # GDP per Capita
    gdp_per_capita_growth = (state['gdp'] / state['population']) - state['gdpPerCapita']
    state['gdpPerCapita'] = state['gdp'] / state['population']

    # Disposable Income (Tied to GDP per capita)
    state['disposableIncome'] = max(0, state['gdpPerCapita'] * 0.7 - (state['lowIncomeTax'] + state['mediumIncomeTax'] + state['highIncomeTax']) * state['gdpPerCapita'])

    # Deduct interest payments from revenue
    interest_payment = state['debt'] * state['interestRate']
    state['totalSpending'] += interest_payment


     # Adjust popularity based on economic performance
    if state['growth'] > 0.03:  # High growth increases popularity
        state['popularity'] += random.uniform(0, 2)
    elif state['growth'] < 0.01:  # Low growth decreases popularity
        state['popularity'] -= random.uniform(0, 2)

    if state['unemploymentRate'] > 0.1:  # High unemployment reduces popularity
        state['popularity'] -= random.uniform(1, 3)

    state['popularity'] = max(0, min(100, state['popularity']))  # Ensure popularity stays within bounds

    # Adjust the number of companies based on growth
    if state['growth'] > 0.03:
        state['numberOfCompanies'] += random.randint(1, 3)
    elif state['growth'] < 0.01:
        state['numberOfCompanies'] -= random.randint(1, 2)

    # Ensure the number of companies doesn't drop below a minimum
    state['numberOfCompanies'] = max(5, state['numberOfCompanies'])

    # Adjust unemployment based on growth and company count
    workforce = state['population'] - state['pensioners']
    employment_effect = max(0, (state['growth'] - 0.02) * 0.2)
    state['unemploymentRate'] += random.uniform(-0.01, 0.01) - employment_effect - (state['numberOfCompanies'] * 0.0002)
    state['unemploymentRate'] = max(0, min(1, state['unemploymentRate']))  # Ensure bounds
    
    
     #Adjust crime rate
    crime_increase = 0.05 * (state['lowIncomePopulation'] / state['population'])  # Higher crime with more low-income population
    crime_decrease = 0.03 * state['policeSpending']  # Police spending reduces crime
    state['crime'] += crime_increase - crime_decrease
    state['crime'] = max(0, min(1000, state['crime']))  # Clamp crime between 0 and 1000
    
    state['debtToGDP'] = (state['debt'] / state['gdp']) * 100
    

    # History
    state['history'].append({
    "date": f"{calendar.month_name[state['month']]}, {state['year']}",  
    "gdp": state['gdp'],
    "population": state['population'],
    "gdpPerCapita": state['gdpPerCapita'],
    "growth": state['growth'],
    "stockIndex": state['stockIndex'],
    "crime": state['crime'],
    "debt": state['debt'],
    "inflation": state['inflation'],
    "interestRate": state['interestRate'],
    "unemploymentRate": state['unemploymentRate'],
    "popularity": state['popularity'],
    "disposableIncome": state['disposableIncome'],
    "numberOfCompanies": state['numberOfCompanies'],
    "debtToGDP": state['debtToGDP'],


    })
    for entry in state['history']:
        if 'date' not in entry:
            entry['date'] = f"{calendar.month_name[1]}, {state['year']}" 

    for sector, data in state['sectors'].items():
        entry[f"{sector}_gdp"] = data['gdpContribution'],


    save_game()
    


# Main loop
while True:
    if not state['countryName']:
        state['countryName'] = input("Choose a country name: > ")
        print(f"Setting up your country, {state['countryName']}...")

    print(f"\nDate: {calendar.month_name[state['month']]}, {state['year']} | GDP: ${state['gdp']:,} | Population: {int(state['population'])} | Stock Index: {state['stockIndex']:.2f} | Monthly Deficit: {state['deficit'] / state['gdp'] * 100:.2f}% of GDP | Inflation: {state['inflation']*100:.2f}%")
    print("What would you like to do?")
    print("SELECT: taxes, spending, finance, stats, next, save, load, quit")
    try:
        todo = input("> ").lower()
    except Exception as e:
        print("Error: "+str(e))
    if todo == "taxes":
        manage_taxes()
    elif todo == "spending":
        manage_spending()
    elif todo == "stats":
        display_stats()
    elif todo == "finance":
        adjust_finance()
    elif todo == "next":
        next_month()
    elif todo == "save":
        save_game()
    elif todo == "load":
        load_game()
    elif todo == "quit":
        print("Exiting the game.")
        break
    else:
        print("Invalid option. Try again.")       

