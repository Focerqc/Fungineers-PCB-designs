import json

# Let's check calibrate_landmarks.py or previous landmark scripts to see what was mapped
try:
    with open('scratch/calibrate_landmarks.py', 'r') as f:
        print(f.read())
except Exception as e:
    print(e)
