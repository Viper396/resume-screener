import pandas as pd
import json
import argparse
import os
from ml_scorer import MLATSScorer
from tqdm import tqdm

def prepare_kaggle_dataset(input_file, output_file='training_data.json', max_samples=None):
    """
    Prepare Kaggle resume dataset for training
    
    Supports:
    - snehaanbhawal/resume-dataset (Resume.csv with 'Resume' column)
    - dhainjeamita/resume-dataset (UpdatedResumeDataSet.csv)
    """
    print(f"Loading dataset from: {input_file}")
    
    # Try to read CSV
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except:
        try:
            df = pd.read_csv(input_file, encoding='latin-1')
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Detect resume text column
    resume_column = None
    for col in ['Resume', 'resume', 'Resume_str', 'text', 'Text']:
        if col in df.columns:
            resume_column = col
            break
    
    if not resume_column:
        print("Could not find resume text column. Available columns:")
        print(df.columns.tolist())
        return
    
    print(f"Using column: '{resume_column}' for resume text")
    
    # Filter out empty/invalid resumes
    df = df[df[resume_column].notna()]
    df = df[df[resume_column].str.len() > 100]  # At least 100 characters
    
    if max_samples:
        df = df.head(max_samples)
    
    print(f"Processing {len(df)} resumes...")
    
    # Initialize scorer
    print("Loading ML scorer...")
    scorer = MLATSScorer()
    
    # Process resumes
    training_data = []
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Scoring resumes"):
        try:
            resume_text = str(row[resume_column])
            
            # Skip very short or very long resumes
            word_count = len(resume_text.split())
            if word_count < 50 or word_count > 2000:
                continue
            
            # Score the resume
            result = scorer.score_resume(resume_text)
            
            # Create training sample
            sample = {
                "text": resume_text[:1000],  # Store first 1000 chars for reference
                "scores": result['breakdown'],
                "overall_score": result['overall_score']
            }
            
            training_data.append(sample)
            
        except Exception as e:
            print(f"Error processing resume {idx}: {e}")
            continue
    
    print(f"\nSuccessfully processed {len(training_data)} resumes")
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"Training data saved to: {output_file}")
    
    # Print statistics
    scores = [s['overall_score'] for s in training_data]
    print(f"\nScore Statistics:")
    print(f"  Mean: {sum(scores)/len(scores):.2f}")
    print(f"  Min: {min(scores):.2f}")
    print(f"  Max: {max(scores):.2f}")
    
    return training_data

def prepare_custom_resumes(resume_dir, output_file='training_data.json'):
    """
    Prepare training data from a directory of resume files (PDF, DOCX, TXT)
    """
    print(f"Loading resumes from directory: {resume_dir}")
    
    scorer = MLATSScorer()
    training_data = []
    
    # Get all resume files
    resume_files = []
    for ext in ['*.pdf', '*.docx', '*.txt']:
        import glob
        resume_files.extend(glob.glob(os.path.join(resume_dir, ext)))
    
    print(f"Found {len(resume_files)} resume files")
    
    for filepath in tqdm(resume_files, desc="Processing resumes"):
        try:
            # Extract text
            text = scorer.extract_text_from_file(filepath)
            
            # Score
            result = scorer.score_resume(text)
            
            # Create sample
            sample = {
                "text": text[:1000],
                "scores": result['breakdown'],
                "overall_score": result['overall_score'],
                "filename": os.path.basename(filepath)
            }
            
            training_data.append(sample)
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            continue
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"Training data saved to: {output_file}")
    print(f"Processed {len(training_data)} resumes")
    
    return training_data

def manual_labeling_interface(training_data_file):
    """
    Simple CLI interface to manually review and adjust scores
    """
    print("=== Manual Labeling Interface ===\n")
    
    with open(training_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} samples")
    print("Commands: [n]ext, [p]revious, [a]djust scores, [s]ave, [q]uit\n")
    
    idx = 0
    
    while idx < len(data):
        sample = data[idx]
        
        print(f"\n--- Sample {idx + 1}/{len(data)} ---")
        print(f"Text preview: {sample['text'][:200]}...")
        print(f"\nCurrent Scores:")
        print(f"  Overall: {sample['overall_score']}")
        for key, value in sample['scores'].items():
            print(f"  {key}: {value}")
        
        cmd = input("\nCommand: ").strip().lower()
        
        if cmd == 'n':
            idx += 1
        elif cmd == 'p':
            idx = max(0, idx - 1)
        elif cmd == 'a':
            print("\nAdjust scores (press Enter to keep current value):")
            new_overall = input(f"Overall score [{sample['overall_score']}]: ").strip()
            if new_overall:
                sample['overall_score'] = float(new_overall)
            
            for key in sample['scores']:
                new_val = input(f"{key} [{sample['scores'][key]}]: ").strip()
                if new_val:
                    sample['scores'][key] = float(new_val)
            
            print("Scores updated!")
            idx += 1
        elif cmd == 's':
            with open(training_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved to {training_data_file}")
        elif cmd == 'q':
            save = input("Save before quitting? (y/n): ").strip().lower()
            if save == 'y':
                with open(training_data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print("Saved!")
            break

def main():
    parser = argparse.ArgumentParser(description='Prepare resume dataset for training')
    parser.add_argument('--input', type=str, help='Input CSV file or directory path')
    parser.add_argument('--output', type=str, default='training_data.json', 
                       help='Output JSON file')
    parser.add_argument('--max-samples', type=int, help='Maximum number of samples to process')
    parser.add_argument('--type', choices=['csv', 'dir'], default='csv',
                       help='Input type: csv file or directory of resumes')
    parser.add_argument('--review', action='store_true',
                       help='Open manual review interface after processing')
    
    args = parser.parse_args()
    
    if not args.input:
        print("Error: --input is required")
        print("\nExamples:")
        print("  python prepare_dataset.py --input data/Resume.csv")
        print("  python prepare_dataset.py --input resumes/ --type dir")
        return
    
    # Prepare dataset
    if args.type == 'csv':
        training_data = prepare_kaggle_dataset(args.input, args.output, args.max_samples)
    else:
        training_data = prepare_custom_resumes(args.input, args.output)
    
    if not training_data:
        print("No training data generated")
        return
    
    # Manual review
    if args.review:
        manual_labeling_interface(args.output)
    
    print("\n✅ Dataset preparation complete!")
    print(f"\nNext step: python train_model.py --data {args.output}")

if __name__ == '__main__':
    main()
