import librosa
import numpy as np
import os
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
from datetime import datetime
import sys


def analyze_voice(audio_path):
    """
    Analyze voice for synthetic characteristics using librosa.
    Returns a detailed analysis result.
    """
    try:
        # First, check if required libraries are available
        try:
            import librosa
            import scipy
            import sounddevice
            print("[DEBUG] All required libraries loaded successfully")
        except ImportError as e:
            print(f"[ERROR] Missing required library: {str(e)}")
            return {
                'status': 'error',
                'error': f"Missing required library: {str(e)}. Please install librosa, scipy, and sounddevice."
            }
        
        print(f"[DEBUG] Starting voice analysis for: {audio_path}")
        
        # Check if file exists
        if not os.path.exists(audio_path):
            print(f"[ERROR] File not found: {audio_path}")
            return {
                'status': 'error',
                'error': f"File not found: {audio_path}"
            }
            
        # Check file size
        try:
            file_size = os.path.getsize(audio_path)
            print(f"[DEBUG] Audio file size: {file_size} bytes")
            
            if file_size == 0:
                print("[ERROR] Audio file is empty")
                return {
                    'status': 'error',
                    'error': "Audio file is empty or corrupted"
                }
        except OSError as e:
            print(f"[ERROR] File access error: {str(e)}")
            return {
                'status': 'error',
                'error': f"Could not access audio file: {str(e)}"
            }
        
        if file_size == 0:
            print(f"[ERROR] Empty audio file: {audio_path}")
            return {
                'status': 'error',
                'error': "Audio file is empty"
            }

        # Load and analyze the audio file
        print("[DEBUG] Loading audio file with librosa...")
        y = None
        sr = None
        try:
            y, sr = librosa.load(audio_path, duration=10, mono=True)
            if len(y) == 0:
                raise ValueError("No audio data loaded")
            print(f"[DEBUG] Audio loaded successfully: {len(y)} samples, {sr}Hz sample rate")
        except Exception as load_error:
            print(f"[ERROR] Failed to load audio: {str(load_error)}")
            import traceback
            print(f"[ERROR] Load traceback: {traceback.format_exc()}")
            return {
                'status': 'error',
                'error': f"Failed to load audio: {str(load_error)}"
            }
        
        # Extract features
        print("[DEBUG] Extracting audio features...")
        
        # Extract features with proper error handling
        try:
            # 1. Pitch variability
            print("[DEBUG] Computing pitch tracking...")
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            print("[DEBUG] Pitch tracking completed")
            
            pitch_mean = np.mean(pitches[pitches > 0])
            pitch_std = np.std(pitches[pitches > 0])
            pitch_variability = pitch_std / pitch_mean if pitch_mean > 0 else 0
            print(f"[DEBUG] Pitch variability: {pitch_variability}")
            
            # 2. Rhythm regularity
            print("[DEBUG] Computing rhythm regularity...")
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            rhythm_regularity = np.std(onset_env)
            print(f"[DEBUG] Rhythm regularity: {rhythm_regularity}")
            
            # 3. Harmonic ratio
            print("[DEBUG] Computing harmonic ratio...")
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            harmonic_ratio = np.mean(np.abs(y_harmonic)) / np.mean(np.abs(y))
            print(f"[DEBUG] Harmonic ratio: {harmonic_ratio}")
            
            # 4. Spectral Contrast (measures the difference between peaks and valleys in the spectrum)
            print("[DEBUG] Computing spectral contrast...")
            contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            contrast_mean = np.mean(contrast)
            contrast_std = np.std(contrast)
            print(f"[DEBUG] Spectral contrast - Mean: {contrast_mean}, Std: {contrast_std}")
            
            # 5. MFCCs (captures the overall shape of the spectral envelope)
            print("[DEBUG] Computing MFCCs...")
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfccs, axis=1)
            mfcc_std = np.std(mfccs, axis=1)
            mfcc_var = np.mean(mfcc_std)  # Variability in spectral shape
            print(f"[DEBUG] MFCC variability: {mfcc_var}")
            
            # 6. Zero Crossing Rate (measures signal noisiness)
            print("[DEBUG] Computing zero crossing rate...")
            zcr = librosa.feature.zero_crossing_rate(y)
            zcr_mean = np.mean(zcr)
            print(f"[DEBUG] Zero crossing rate: {zcr_mean}")
            
            # Enhanced decision logic with new features
            synthetic_indicators = [
                pitch_variability < 0.1,         # Low pitch variation
                rhythm_regularity < 0.1,         # Too regular rhythm
                harmonic_ratio > 0.95,           # Too harmonic
                contrast_std < 0.5,              # Low spectral contrast variation
                mfcc_var < 0.1,                  # Too consistent spectral shape
                zcr_mean < 0.01                  # Too smooth signal
            ]
            
            # Calculate confidence based on how many indicators are triggered
            num_synthetic_indicators = sum(synthetic_indicators)
            confidence_score = min(1.0, num_synthetic_indicators / len(synthetic_indicators))
            
            # Consider it synthetic if more than half of indicators suggest so
            is_synthetic = num_synthetic_indicators >= len(synthetic_indicators) / 2
            
            print(f"[DEBUG] Enhanced analysis complete:")
            print(f"  - Is synthetic: {is_synthetic}")
            print(f"  - Confidence score: {confidence_score}")
            print(f"  - Triggered indicators: {num_synthetic_indicators}/{len(synthetic_indicators)}")
            
            print(f"[DEBUG] Analysis complete - is_synthetic: {is_synthetic}, confidence: {confidence_score}")
            
            return {
                'status': 'success',
                'is_synthetic': is_synthetic,
                'confidence': confidence_score,
                'details': {
                    'pitch_variability': float(pitch_variability),
                    'rhythm_regularity': float(rhythm_regularity),
                    'harmonic_ratio': float(harmonic_ratio),
                    'spectral_contrast': {
                        'mean': float(contrast_mean),
                        'std': float(contrast_std)
                    },
                    'mfcc': {
                        'variability': float(mfcc_var)
                    },
                    'zero_crossing_rate': float(zcr_mean),
                    'synthetic_indicators_triggered': int(num_synthetic_indicators),
                    'total_indicators': len(synthetic_indicators)
                }
            }
            
        except Exception as feature_error:
            print(f"[ERROR] Failed to extract audio features: {str(feature_error)}")
            import traceback
            print(f"[ERROR] Feature extraction traceback: {traceback.format_exc()}")
            return {
                'status': 'error',
                'error': f"Failed to analyze audio features: {str(feature_error)}"
            }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def auto_record_and_analyze(duration=10, samplerate=16000):
    """
    Record audio from the default/active microphone for the specified duration and analyze it.
    Automatically uses the default input device without user selection.
    
    Args:
        duration (int): Recording duration in seconds (default: 10)
        samplerate (int): Sample rate for recording (default: 16000)
    
    Returns:
        dict: Analysis results
    """
    try:
        # Get default input device automatically
        try:
            default_device = sd.default.device[0]  # Get default input device
            device_info = sd.query_devices(default_device, 'input')
            print(f"[INFO] Using default device: {device_info['name']}")
        except sd.PortAudioError as e:
            raise RuntimeError(f"Error accessing default device: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Could not get default device: {str(e)}")
        
        print(f"[INFO] Starting {duration}-second voice recording...")
        print("[INFO] Please speak into your microphone...")
        
        # Create a temporary directory if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(__file__), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file = os.path.join(temp_dir, f"recording_{timestamp}.wav")
        
        # Record audio with the default device
        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype='float32'
            # device parameter not needed - uses default automatically
        )
        
        # Display countdown
        print("[INFO] Recording in progress:")
        for remaining in range(duration, 0, -1):
            print(f"  {remaining} seconds remaining...")
            sd.sleep(1000)  # Sleep for 1 second
            
        print("[INFO] Recording complete!")
        
        # Ensure recording is complete
        sd.wait()
        
        # Normalize the recording
        recording = recording / np.max(np.abs(recording))
        
        # Save the recording
        write(temp_file, samplerate, recording)
        print(f"[INFO] Recording saved to: {temp_file}")
        
        # Analyze the recording
        print("[INFO] Analyzing the recording...")
        results = analyze_voice(temp_file)
        
        # Clean up
        try:
            os.remove(temp_file)
            print("[INFO] Temporary recording file cleaned up")
        except Exception as e:
            print(f"[WARNING] Could not delete temporary file: {str(e)}")
        
        return results
        
    except Exception as e:
        print(f"[ERROR] Recording failed: {str(e)}")
        return {
            'status': 'error',
            'error': f'Recording failed: {str(e)}'
        }

if __name__ == "__main__":
    print("Voice Analysis Module - Synthetic Voice Detection")
    print("=" * 50)
    auto_record_and_analyze()
    
    