


import pandas as pd
import os

# File to store the collected data
DATA_FILE = "instagram_research_data.csv"

def get_input(prompt, data_type=str, allow_empty=False):
    """Get and validate user input"""
    while True:
        value = input(prompt)
        if value == "" and allow_empty:
            return None
        try:
            if data_type == bool:
                if value.lower() in ['y', 'yes', 'true', 't', '1']:
                    return True
                elif value.lower() in ['n', 'no', 'false', 'f', '0']:
                    return False
                else:
                    print("Please enter Yes/No, True/False, Y/N, or 1/0")
                    continue
            return data_type(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {data_type.__name__}")

def collect_business_data():
    """Collect data about a single business"""
    print("\n=== New Instagram Business Data Entry ===")
    
    business_data = {
        'Business_Name': get_input("Business Name: "),
        'Industry': get_input("Industry (Clothing/Food/Beauty/Other): "),
        'Followers': get_input("Number of Followers: ", int),
        'Posts_Count': get_input("Number of Posts: ", int),
        'Avg_Likes': get_input("Average Likes per Post: ", float),
        'Avg_Comments': get_input("Average Comments per Post: ", float),
        'Response_Time_Hours': get_input("Response Time (hours): ", float),
        'DM_Centric': get_input("DM-Centric Business? (y/n): ", bool),
        'Notes': get_input("Additional Notes: ")
    }
    
    return business_data

def load_existing_data():
    """Load existing data from CSV if it exists"""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            'Business_Name', 'Industry', 'Followers', 'Posts_Count', 
            'Avg_Likes', 'Avg_Comments', 'Response_Time_Hours', 
            'DM_Centric', 'Notes'
        ])

def analyze_research(df):
    """Analyze the collected data"""
    if df.empty:
        return "No data to analyze yet."
    
    try:
        industry_stats = df.groupby('Industry').agg({
            'Followers': 'mean',
            'Response_Time_Hours': 'mean',
            'DM_Centric': lambda x: sum(x)/len(x) * 100  # % of businesses using DMs
        })
        return industry_stats
    except Exception as e:
        return f"Error analyzing data: {str(e)}"

def main():
    print("Instagram Business Research Data Collection")
    print("==========================================")
    
    # Load existing data
    df = load_existing_data()
    if not df.empty:
        print(f"Loaded {len(df)} existing business entries")
    
    while True:
        print("\nOptions:")
        print("1. Add new business data")
        print("2. View all collected data")
        print("3. Analyze data")
        print("4. Save and exit")
        
        choice = get_input("Enter your choice (1-4): ")
        
        if choice == "1":
            # Add new business
            new_data = collect_business_data()
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            print("Business data added successfully!")
            # Save after each addition
            df.to_csv(DATA_FILE, index=False)
            print(f"Data saved to {DATA_FILE}")
            
        elif choice == "2":
            # View all data
            if df.empty:
                print("No data collected yet.")
            else:
                print("\nCollected Data:")
                print(df)
                
        elif choice == "3":
            # Analyze data
            if df.empty:
                print("No data to analyze yet.")
            else:
                results = analyze_research(df)
                print("\nAnalysis Results:")
                print(results)
                
        elif choice == "4":
            # Save and exit
            if not df.empty:
                df.to_csv(DATA_FILE, index=False)
                print(f"Data saved to {DATA_FILE}")
            print("Exiting program. Thank you!")
            break
            
        else:
            print("Invalid choice. Please enter a number from 1-4.")

if __name__ == "__main__":
    main()

### How to Use This Script:
