import unittest
from bikeshare import BikeShare
from station import Station
from rules import parse_int, breakages

class StudentValidationTests(unittest.TestCase):

    # --- Task 3 Object Constraints Verification ---

    def test_c1_default_stations_isolation(self):
        """Verify that two default BikeShare objects are fully independent (C1)."""
        sim1 = BikeShare()
        sim2 = BikeShare()
        
        # Move bikes in sim1 only
        sim1.step({"moves": [("B", "A", 2)], "repairs": 0}, [])
        
        # Confirm sim2 remains untouched in its original state
        self.assertNotEqual(sim1.get_bikes(), sim2.get_bikes())

    def test_c2_historical_records_and_state_isolation(self):
        """Verify that modifying returned maps or history logs cannot corrupt internal state (C2)."""
        sim = BikeShare()
        
        # Attempt an external mutation on the returned bikes dictionary
        bikes_view = sim.get_bikes()
        bikes_view["A"] = 999
        self.assertEqual(sim.get_bikes()["A"], 12)
        
        # Run a quick empty step to populate history logs
        sim.step({"moves": [], "repairs": 0}, [])
        history_view = sim.get_history()
        
        # Attempt to corrupt history externally
        if history_view:
            history_view[0]["closing_cash"] = 0
            self.assertNotEqual(sim.get_history()[0]["closing_cash"], 0)

    def test_c3_atomic_transaction_sandbox_rollback(self):
        """Verify that a partially invalid plan rolls back completely with zero side-effects (C3)."""
        sim = BikeShare()
        initial_state = sim.get_bikes()
        
        # Setup a compound plan where move #1 is valid but move #2 fails (Station C only has 6 bikes)
        bad_decision = {
            "moves": [("B", "A", 3), ("C", "A", 10)], 
            "repairs": 0
        }
        
        with self.assertRaises(ValueError):
            sim.step(bad_decision, [])
            
        # Confirm that Move #1 (B -> A) was completely rolled back atomically
        self.assertEqual(sim.get_bikes(), initial_state)

    # --- Edge Case & Boundary Calculation Tests ---

    def test_parse_int_boundary_spaces(self):
        """Ensure inputs with heavy whitespace are trimmed and handled cleanly."""
        self.assertEqual(parse_int("   12   ", 1, 20), 12)

    def test_breakages_ceil_rounding_boundary(self):
        """Verify that breakages calculate exact ceilings correctly for 10% rate."""
        # 1 trip complete -> 1 * 0.1 = 0.1 -> ceil(0.1) = 1 broken bike
        self.assertEqual(breakages(1, 10), 1)
        # 10 trips complete -> 10 * 0.1 = 1.0 -> ceil(1.0) = 1 broken bike
        self.assertEqual(breakages(10, 10), 1)
        # 11 trips complete -> 11 * 0.1 = 1.1 -> ceil(1.1) = 2 broken bikes
        self.assertEqual(breakages(11, 10), 2)
