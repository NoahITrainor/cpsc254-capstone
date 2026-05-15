import json
import sys
import os

# Add the root directory to sys.path so we can import engine.py
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)

from app.engine import recommend  # Adjust 'app.engine' if your folder structure is different

def run_evaluation():
    # 1. Load the test cases
    test_file_path = os.path.join(current_dir, "test_cases.json")
    with open(test_file_path, "r") as f:
        test_cases = json.load(f)

    print(f"Starting Evaluation on {len(test_cases)} test cases...\n")
    
    passed = 0
    total = len(test_cases)

    # 2. Run the metric test loop
    for i, test in enumerate(test_cases, 1):
        movie = test["input"]
        expected = test["expected_behavior"]
        
        print(f"Test {i}/{total}: '{movie}' (Expected: {expected})")
        
        try:
            # Call your AI logic
            results = recommend(movie)
            
            # 3. Determine Pass/Fail based on the expected behavior
            # If we expect fake, the results list should be empty (caught by your bouncer)
            if expected == "fake" and len(results) == 0:
                print("  ✅ PASS: Fake movie successfully blocked.")
                passed += 1
            
            # If we expect real, the results list should contain movies
            elif expected == "real" and len(results) > 0:
                print("  ✅ PASS: Real movie successfully processed.")
                passed += 1
                
            else:
                print(f"  ❌ FAIL: AI behaved unexpectedly. Returned {len(results)} items.")

        except Exception as e:
            print(f"  ❌ FAIL: Code crashed with error: {e}")

    # 4. Calculate Final Metric Score
    score = (passed / total) * 100
    print("\n" + "="*30)
    print(f"EVALUATION COMPLETE")
    print(f"Final Score: {passed}/{total} ({score}%)")
    print("="*30)

if __name__ == "__main__":
    run_evaluation()