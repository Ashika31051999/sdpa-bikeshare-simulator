import sys
from rules import load_days, parse_int, pence_to_pounds
from bikeshare import BikeShare

def safe_input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting program cleanly. Goodbye!")
        sys.exit(0)

def run():
    # 1. Load the trips dataset cleanly
    try:
        trips_data = load_days("data/trips.json")
    except Exception as e:
        print(f"Error loading initial file parameters: {e}")
        sys.exit(1)

    print("==========================================================")
    print("  Welcome to the Bike-Share Simulation Console Framework  ")
    print("==========================================================")

    # 2. Collect simulation duration scope bounds safely
    while True:
        days_raw = safe_input("Enter days to simulate (1-14, Press Enter for default 7): ")
        if not days_raw.strip():
            days_count = 7
            break
        try:
            days_count = parse_int(days_raw, 1, 14)
            break
        except ValueError:
            print("[Invalid] Please enter a whole number between 1 and 14.")

    sim = BikeShare()
    total_completed = 0
    total_lost = 0
    bankrupt = False
    
    # 3. Process the simulation daily turn loop sequences
    for _ in range(days_count):
        day_idx = sim.get_day() - 1
        today_trips = trips_data[day_idx] if day_idx < len(trips_data) else []

        print(f"\n--- Day {sim.get_day()} | Bank Balance: {pence_to_pounds(sim.get_cash())} ---")
        print("Station Status:")
        for k, v in sim.get_bikes().items():
            print(f"  Station {k}: {v} bikes currently docked")
        print(f"Workshop Inventory: {sim.get_workshop()} broken bikes in repair queue")

        # Inner loop to handle inputs safely until a valid day action set is entered
        while True:
            try:
                print("\n[Input Actions for Today]")
                rep_raw = safe_input("  Enter number of bikes to repair: ")
                repairs = parse_int("0" if not rep_raw.strip() else rep_raw, 0)
                
                m_raw = safe_input("  Enter number of van moves (0-3): ")
                m_count = parse_int("0" if not m_raw.strip() else m_raw, 0, 3)
                
                moves = []
                for i in range(m_count):
                    while True:
                        m_str = safe_input(f"    Enter move #{i+1} (Format: Origin Destination Count, e.g. 'B A 3'): ")
                        parts = m_str.strip().split()
                        if len(parts) != 3:
                            print("    [Error] Format must be exactly three values split by spaces.")
                            continue
                        try:
                            origin = parts[0].upper()
                            destination = parts[1].upper()
                            count = parse_int(parts[2], 1, 10)
                            moves.append((origin, destination, count))
                            break
                        except ValueError as e:
                            print(f"    [Error] Invalid move values: {e}")
                
                # Execute day step operations atomically
                res = sim.step({"moves": moves, "repairs": repairs}, today_trips)
                break
            except ValueError as e:
                print(f"\n[Decision Rejected] {e}")
                print("Your plan violated system constraints. Let's try setting up today's plan again.")

        # Print detailed evening tracking summary report data models
        print("\n>>> End of Day Financial & Commuter Report <<<")
        print(f"  Revenue Earned : {pence_to_pounds(res['revenue'])}")
        print(f"  Van Costs      : {pence_to_pounds(res['van_cost'])}")
        print(f"  Repair Costs   : {pence_to_pounds(res['repair_cost'])}")
        print(f"  Fixed Day Cost : {pence_to_pounds(res['daily_cost'])}")
        print(f"  Closing Balance: {pence_to_pounds(res['closing_cash'])}")
        print(f"  Trips Finished : {res['completed']} | Trips Lost: {res['lost']} | Bikes Broken: {res['broken']}")
        
        total_completed += res['completed']
        total_lost += res['lost']

        if res['closing_cash'] < 0:
            print("\n!!! BANKRUPTCY NOTICE: Accounts dropped below zero credit balance !!!")
            bankrupt = True
            break

    # 4. Final Cumulative Multi-Day Simulation Reports summary print blocks
    print("\n==================== SIMULATION OVER ====================")
    print(f"Total Completed Commutes: {total_completed}")
    print(f"Total Dropped Commutes  : {total_lost}")
    print(f"Final Bank Holdings     : {pence_to_pounds(sim.get_cash())}")
    if bankrupt:
        print("Simulation Outcome      : TERMINATED (Bankrupt)")
    else:
        print("Simulation Outcome      : SUCCESS (Target Run Finished)")
    print("=========================================================")

if __name__ == "__main__":
    run()
