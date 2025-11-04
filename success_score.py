import importlib.util
import os
import sys

def import_from_file(file_path):
    """Import a module from file path."""
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Import our security check modules
kyc_module = import_from_file(os.path.join(current_dir, "kyc-match.py"))
sim_swap_module = import_from_file(os.path.join(current_dir, "sim-swap-check.py"))
device_module = import_from_file(os.path.join(current_dir, "device-check.py"))
number_module = import_from_file(os.path.join(current_dir, "number-varification.py"))
device_swap_module = import_from_file(os.path.join(current_dir, "device-swapped.py"))


# Get the functions we need
kyc_match_check = kyc_module.kyc_match_check
sim_swap_check = sim_swap_module.sim_swap_check
get_device_status = device_module.get_device_status
number_verification_check = number_module.number_verification_check
device_swap_check = device_swap_module.device_swapped_check


def calculate_security_score(mobile_number):
    """
    Calculate a security score based on all security checks.
    Each check contributes 25% to the total score.
    Returns a percentage score and a status message.
    """
    score = 0
    results = []
    
    # Run KYC Match Check
    print("\nRunning KYC Match Check...")
    kyc_result = kyc_match_check(mobile_number)
    if kyc_result:
        score += 20
        results.append("✓ KYC Match: Passed")
    else:
        results.append("✗ KYC Match: Failed")

    # Run SIM Swap Check
    print("\nRunning SIM Swap Check...")
    sim_result = sim_swap_check(mobile_number)
    if sim_result:
        score += 20
        results.append("✓ SIM Swap Check: Passed")
    else:
        results.append("✗ SIM Swap Check: Failed")

    # Run Device Status Check
    print("\nRunning Device Status Check...")
    device_result = get_device_status(mobile_number)
    if device_result:
        score += 20
        results.append("✓ Device Status: Passed")
    else:
        results.append("✗ Device Status: Failed")



    # Run Device Swaped Check
    print("\nRunning Device Swaped Check...")
    device_swap_result = device_swap_check(mobile_number)

    if device_swap_result:
        score += 20
        results.append("✓ Device Status: Passed")
    else:
        results.append("✗ Device Status: Failed")

    # Run Number Verification
    print("\nRunning Number Verification...")
    number_result = number_verification_check(mobile_number)
    if number_result:
        score += 20
        results.append("✓ Number Verification: Passed")
    else:
        results.append("✗ Number Verification: Failed")

    # Print detailed results
    print("\n=== Security Check Results ===")
    for result in results:
        print(result)
    print(f"\nFinal Security Score: {score}%")

    # Return recommendation based on score
    if score >= 75:
        return score, "HIGH SECURITY - Registration Recommended"
    elif score >= 50:
        return score, "MEDIUM SECURITY - Proceed with Caution"
    else:
        return score, "LOW SECURITY - Additional Verification Recommended"

