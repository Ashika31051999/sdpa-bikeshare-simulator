import copy
from rules import completed_trips, breakages

class BikeShare:
    FARE, DAILY_COST, VAN_COST, REPAIR_COST = 200, 2400, 500, 200
    BREAK_RATE, VAN_CAPACITY, MAX_MOVES, DEPOT = 10, 10, 3, "A"

    def __init__(self, stations=None):
        self._day = 1
        self._cash = 10000
        self._workshop = 0
        self._history = []
        
        if stations is None:
            # Rule C1: Independent instances via fresh generation
            from station import Station
            self._stations = {
                "A": Station("A", "Temple Meads", 20, 12),
                "B": Station("B", "Harbourside", 15, 8),
                "C": Station("C", "Clifton", 12, 6)
            }
        else:
            self._stations = {k: v.copy() for k, v in stations.items()}

    def get_day(self): return self._day
    def get_cash(self): return self._cash
    def get_workshop(self): return self._workshop
    
    # Rule C2: Return clean copies preventing external mutability shifts
    def get_bikes(self): return {k: s.bikes for k, s in self._stations.items()}
    def get_history(self): return copy.deepcopy(self._history)

    def step(self, decision, trips):
        if not isinstance(decision, dict) or "moves" not in decision or "repairs" not in decision:
            raise ValueError("Invalid decision format.")
        moves, repairs = decision["moves"], decision["repairs"]
        if not isinstance(moves, list) or len(moves) > self.MAX_MOVES or not isinstance(repairs, int) or repairs < 0:
            raise ValueError("Violated base execution constraints parameters.")

        # Rule C3: Transaction Sandbox Environment Clones (Atomic Reversion)
        sandbox_stations = {k: v.copy() for k, v in self._stations.items()}
        sandbox_workshop = self._workshop

        # Process Van Moves
        for move in moves:
            if len(move) != 3: raise ValueError("Invalid move format.")
            o, d, c = move
            if o not in sandbox_stations or d not in sandbox_stations or c <= 0 or c > self.VAN_CAPACITY:
                raise ValueError("Invalid station index or capacity threshold overflows.")
            if sandbox_stations[o].bikes < c or sandbox_stations[d].free_docks() < c:
                raise ValueError("Insufficient assets to execute moving transitions.")
            sandbox_stations[o].bikes -= c
            sandbox_stations[d].bikes += c

        # Process Workshop Repairs
        if repairs > 0:
            if sandbox_workshop < repairs or sandbox_stations[self.DEPOT].free_docks() < repairs:
                raise ValueError("Invalid context layout adjustments for repairs execution.")
            sandbox_workshop -= repairs
            sandbox_stations[self.DEPOT].bikes += repairs

        # Process Customer Commutes
        t_comp, t_lost, t_brok = 0, 0, 0
        for o, d, req in trips:
            done = completed_trips(req, sandbox_stations[o].bikes, sandbox_stations[d].free_docks())
            sandbox_stations[o].bikes -= done
            sandbox_stations[d].bikes += done
            
            brok = breakages(done, self.BREAK_RATE)
            sandbox_stations[d].bikes -= brok
            sandbox_workshop += brok
            
            t_comp += done
            t_lost += (req - done)
            t_brok += brok

        # Financial Balancing
        rev = t_comp * self.FARE
        v_cost = len(moves) * self.VAN_COST
        r_cost = repairs * self.REPAIR_COST
        closing = self._cash + rev - v_cost - r_cost - self.DAILY_COST

        # Commit State changes only if everything succeeds
        self._stations = sandbox_stations
        self._workshop = sandbox_workshop
        
        record = {
            "day": self._day, "opening_cash": self._cash, "closing_cash": closing,
            "revenue": rev, "van_cost": v_cost, "repair_cost": r_cost, "daily_cost": self.DAILY_COST,
            "completed": t_comp, "lost": t_lost, "broken": t_brok,
            "stations_bikes": self.get_bikes(), "workshop_bikes": self._workshop
        }
        self._cash = closing
        self._history.append(record)
        self._day += 1
        return copy.deepcopy(record)
