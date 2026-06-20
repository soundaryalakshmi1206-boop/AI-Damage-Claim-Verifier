AI Damage Claim Verifier
AI-Powered Multimodal Insurance Claim Verification System

An intelligent multi-agent system that verifies insurance damage claims by combining computer vision, image quality analysis, historical claim analysis, and rule-based evidence verification using Qwen2.5-VL-3B-Instruct running locally through LM Studio.

The system determines whether an insurance claim is Supported, Contradicted, or Not Enough Information based on uploaded evidence instead of relying solely on the customer's statement.

Problem Statement

Insurance companies receive thousands of claims every day.

Many claims contain:

Poor quality images
Cropped images
Edited images
Missing evidence
Incorrect claim descriptions
Fraudulent submissions

Manual verification is slow, expensive, and inconsistent.

This project automates the first stage of claim verification using AI.

Key Features
Multi-Agent AI Architecture

The system is divided into specialized AI agents.

Conversation Agent
Vision Agent (Qwen2.5-VL)
Image Validator
Evidence Agent
History Agent
Decision Engine

Each agent performs one responsibility and passes structured information to the next module.

Vision-Based Damage Verification

Uses Qwen2.5-VL-3B-Instruct to analyze uploaded images and identify:

Vehicle / Laptop / Package
Damage Type
Damaged Parts
Damage Severity
Image Quality
Camera Angle
Object Visibility
Possible Image Manipulation
Final Claim Decision
Confidence Score
Image Validation

Before sending images to the Vision Model, the system validates image quality using OpenCV.

Checks include:

Blur Detection
Brightness Analysis
Screenshot Detection
Duplicate Image Detection
Crop Detection
Metadata Analysis
Image Quality Score
Evidence Verification

Matches detected damaged parts against predefined insurance evidence requirements.

Supports:

Multiple damaged parts
Synonym matching
General claim rules
Missing evidence detection
Historical Risk Analysis

Analyzes claimant history using previous claim records.

Calculates:

Risk Score
Risk Level
Fraud Indicators
Frequent Claim Detection
Historical Risk Flags
Decision Engine

Combines outputs from all AI agents.

Considers:

Vision Confidence
Image Quality
Historical Risk
Evidence Rules
Camera Angle
Object Visibility
Damage Visibility

Returns:

Supported
Contradicted
Not Enough Information

System Architecture
                    User Claim
                         │
                         ▼
              Conversation Agent
                         │
                         ▼
               Image Validator
                         │
                         ▼
        Vision Agent (Qwen2.5-VL)
                         │
                         ▼
                Evidence Agent
                         │
                         ▼
                 History Agent
                         │
                         ▼
                Decision Engine
                         │
                         ▼
                    Output CSV

                    
Project Structure

hackerrank/

├── dataset/
│   ├── claims.csv
│   ├── sample_claims.csv
│   ├── user_history.csv
│   ├── evidence_requirements.csv
│   └── images/
│
├── code/
│
│── agents/
│   ├── conversation_agent.py
│   ├── vision_agent.py
│   ├── evidence_agent.py
│   ├── history_agent.py
│   └── decision_engine.py
│
├── utils/
│   ├── image_validator.py
│   ├── csv_writer.py
│   └── helpers.py
│
├── outputs/
│   └── output.csv
│
├── config.py
├── main.py
└── README.md

# 🏗️ System Architecture and work flow

<p align="center">
  <img src="assets/"C:\Users\Asus\Downloads\ChatGPT Image Jun 21, 2026, 01_13_17 AM.png" width="900">
</p>



Technologies Used
Programming Language
Python 3.11
AI Model
Qwen2.5-VL-3B-Instruct
Vision
OpenCV
Image Processing
Pillow
ImageHash
NumPy
Data Processing
Pandas
LLM Runtime
LM Studio
Workflow

Step 1

User submits:

Claim description
Uploaded images

↓

Step 2

Conversation Agent extracts structured claim information.

↓

Step 3

Image Validator checks:

Blur
Brightness
Crop
Screenshot
Metadata
Duplicate Images

↓

Step 4

Vision Agent analyzes uploaded images using Qwen2.5-VL.

↓

Step 5

Evidence Agent validates whether required evidence has been provided.

↓

Step 6

History Agent evaluates previous insurance claims.

↓

Step 7

Decision Engine combines all information into the final decision.

↓

Step 8

Output is written to CSV.

Output Format

The generated CSV contains:

user_id
image_paths
user_claim
claim_object
evidence_standard_met
evidence_standard_met_reason
risk_flags
issue_type
object_part
claim_status
claim_status_justification
supporting_image_ids
valid_image
severity
Example Decision

Customer Claim

My front bumper has a dent after a collision.

↓

Vision Agent

Object:
Car

Damage:
Dent

Part:
Front Bumper

Confidence:
0.95

↓


hackerrank/
│
├── .gitignore          ✅ Create here
├── README.md
├── LICENSE             (Optional)
│
├── code/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── agents/
│   ├── utils/
│   └── outputs/
│
└── dataset/
    ├── claims.csv
    ├── sample_claims.csv
    ├── user_history.csv
    ├── evidence_requirements.csv
    └── images/

    # 💻 Console Output

<p align="center">
  <img src="assets/"C:\Users\Asus\OneDrive\Pictures\Screenshots\Screenshot 2026-06-21 021335.png" width="900">
</p>

<p align="center">
  <img src="assets/"C:\Users\Asus\OneDrive\Pictures\Screenshots\Screenshot 2026-06-21 021355.png"
  " width="900">
</p>

# 📊 Output

<p align="center">
  <img src="assets/"C:\Users\Asus\OneDrive\Pictures\Screenshots\Screenshot 2026-06-21 021414.png" width="900">
</p>

## LM Studio Setup

This project uses **Qwen2.5-VL-3B-Instruct** running locally through **LM Studio**.

### Steps

1. Install LM Studio.
2. Download the **Qwen2.5-VL-3B-Instruct** model.
3. Load the model in LM Studio.
4. Start the Local Server.
5. Ensure the server is running at:

```text
http://127.0.0.1:1234/v1
```

The Vision Agent connects to the local server using:

```python
self.client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)
```
Decision Engine

Claim Status:
Supported
Future Improvements
OCR for extracting text from images
Explainable AI reports
Real-time REST API
Web Dashboard
Mobile Application
Cloud Deployment
Multi-language Support
Video-based Damage Verification
Fraud Detection using Deep Learning

Highlights
Multi-Agent AI Architecture
Vision Language Model Integration
Computer Vision Based Validation
Rule-Based Evidence Verification
Historical Risk Analysis
Weighted Decision Engine
Modular and Scalable Design
Local AI Inference using LM Studio

 author

 soundaryalakshmi s

Third Year – cse

kiot

License

This project was developed for educational purposes and hackathon participation.
