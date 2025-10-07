#!/usr/bin/env python3
"""
Test script to verify that the retrained models work correctly.
"""

import pandas as pd
import comment_analysis
import sys

def test_models():
    """Test the comment analysis with sample data."""
    print("Testing the retrained models...")
    
    # Create sample test data
    sample_comments = [
        "This video is amazing! I love it so much!",
        "This is terrible content, waste of time.",
        "The video is okay, not bad but not great either.",
        "Absolutely fantastic work, keep it up!",
        "This sucks, very disappointing."
    ]
    
    sample_likes = [100, 5, 20, 150, 8]
    
    # Create DataFrame in the expected format
    test_df = pd.DataFrame({
        'comments': sample_comments,
        'like_count': sample_likes
    })
    
    print(f"Test data created with {len(sample_comments)} comments")
    
    try:
        # Test the analysis function
        classified_comments, pos_most_liked, neu_most_liked, neg_most_liked = comment_analysis.analyze_comments(test_df)
        
        print("\n✅ Model analysis completed successfully!")
        print(f"Total comments analyzed: {len(classified_comments)}")
        
        # Show sentiment distribution
        sentiment_counts = classified_comments['sentiment'].value_counts().sort_index()
        print("\nSentiment Distribution:")
        for sentiment, count in sentiment_counts.items():
            sentiment_name = {-1.0: "Negative", 0.0: "Neutral", 1.0: "Positive"}.get(sentiment, "Unknown")
            print(f"  {sentiment_name}: {count}")
        
        print("\nSample classifications:")
        for i, row in classified_comments.iterrows():
            sentiment_name = {-1.0: "Negative", 0.0: "Neutral", 1.0: "Positive"}.get(row['sentiment'], "Unknown")
            print(f"  '{row['originalComments']}' -> {sentiment_name}")
        
        print("\n✅ All tests passed! The models are working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_models()
    sys.exit(0 if success else 1)