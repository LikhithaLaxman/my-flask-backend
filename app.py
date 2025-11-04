from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from success_score import *
from voice_check import *
import sys
import io


# Simulated list of mobile numbers with country info
MOBILE_NUMBERS = [
    "+36719991000 (Hungary - Vodafone)",
    "+447911123456 (UK - Vodafone)",
    "+14155552671 (USA - AT&T)",
    "+99999991000 (Test Number)"
]

# Helper function to capture print() output
def capture_output(func, *args, **kwargs):
    buffer = io.StringIO()
    sys.stdout = buffer
    func(*args, **kwargs)
    sys.stdout = sys.__stdout__
    return buffer.getvalue()


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html', numbers=MOBILE_NUMBERS)

@app.route('/check_security', methods=['POST'])
def check_security():
    # Handle both JSON and form data
    if request.is_json:
        mobile_number = request.json.get('number')
    else:
        mobile_number = request.form.get('mobile_number')

    if not mobile_number:
        return jsonify({'error': 'Mobile number is required'}), 400

    try:
        # Run all security checks
        kyc_result = kyc_match_check(mobile_number)
        sim_result = sim_swap_check(mobile_number)
        device_result = get_device_status(mobile_number)
        device_swap_result = device_swap_check(mobile_number)
        number_result = number_verification_check(mobile_number)
        
        # Update check statuses
        checks = {
            'kyc': {
                'status': 'success' if kyc_result else 'failed',
                'message': 'KYC Verification Successful' if kyc_result else 'KYC Check Failed'
            },
            'sim_swap': {
                'status': 'success' if sim_result else 'failed',
                'message': 'No SIM Swap Detected' if sim_result else 'Suspicious SIM Activity'
            },
            'device': {
                'status': 'success' if device_result else 'failed',
                'message': 'Device Verified' if device_result else 'Device Check Failed'
            },
            'device_swap': {
                'status': 'success' if device_swap_result else 'failed',
                'message': 'No Device Change Detected' if device_swap_result else 'Recent Device Change'
            },
            'number_verification': {
                'status': 'success' if number_result else 'failed',
                'message': 'Number Verified' if number_result else 'Number Verification Failed'
            }
        }
        
        # Calculate final score
        score, recommendation = calculate_security_score(mobile_number)
        
        return jsonify({
            'checks': checks,
            'score': score,
            'recommendation': recommendation
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Convert NumPy types to native Python before jsonify
def convert_numpy(obj):
    if isinstance(obj, np.generic):  # e.g. np.float64, np.bool_
        return obj.item()
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(v) for v in obj]
    else:
        return obj

@app.route('/auto_record_and_analyze1', methods =['POST'])
def auto_record_and_analyze1():
    try:
        rslt = auto_record_and_analyze()
        converted_result = convert_numpy(rslt)
        
        # Format the voice analysis results for better display
        if converted_result.get('status') == 'success':
            voice_checks = {
                'voice_type': {
                    'status': 'danger' if converted_result.get('is_synthetic', False) else 'success',
                    'message': 'Computer Generated Voice Detected' if converted_result.get('is_synthetic', False) else 'Human Voice Detected',
                    'icon': 'robot' if converted_result.get('is_synthetic', False) else 'user'
                },
                'confidence': {
                    'status': 'info',
                    'message': f"Detection Confidence: {converted_result.get('confidence', 0) * 100:.1f}%",
                    'icon': 'percentage'
                }
            }
            
            # Add detailed metrics if available
            details = converted_result.get('details', {})
            if details:
                voice_checks.update({
                    'pitch': {
                        'status': 'info',
                        'message': f"Pitch Variability: {details.get('pitch_variability', 0):.3f}",
                        'icon': 'wave-square'
                    },
                    'rhythm': {
                        'status': 'info',
                        'message': f"Rhythm Regularity: {details.get('rhythm_regularity', 0):.3f}",
                        'icon': 'music'
                    },
                    'harmonics': {
                        'status': 'info',
                        'message': f"Harmonic Ratio: {details.get('harmonic_ratio', 0):.3f}",
                        'icon': 'chart-line'
                    }
                })
            
            return jsonify({
                'status': 'success',
                'voice_checks': voice_checks,
                'summary': {
                    'is_synthetic': converted_result.get('is_synthetic', False),
                    'confidence': converted_result.get('confidence', 0),
                    'details': details
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'error': converted_result.get('error', 'Unknown error occurred'),
                'voice_checks': {
                    'error': {
                        'status': 'danger',
                        'message': converted_result.get('error', 'Voice analysis failed'),
                        'icon': 'exclamation-triangle'
                    }
                }
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'voice_checks': {
                'error': {
                    'status': 'danger',
                    'message': f'Voice analysis failed: {str(e)}',
                    'icon': 'exclamation-triangle'
                }
            }
        }), 500


if __name__ == '__main__':
    app.run(debug=True)