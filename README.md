# Emotion-Based Social Event Detection (ESED)

## Overview
ESED is a novel approach designed to detect social events on Twitter by analyzing the underlying emotions expressed in tweets. This method leverages the intensity of specific emotions within tweets to identify significant events, providing a more nuanced understanding than traditional methods that rely solely on keyword frequency or basic sentiment analysis.

## Key Features
- **Emotion Intensity Extraction**: Utilizes a Convolutional Neural Network (CNN) to analyze the emotional content of tweets, focusing on four primary emotions: anger, fear, joy, and sadness.
- **Emoji and Emoticon Analysis**: Enhances emotion detection accuracy by incorporating the analysis of emojis and emoticons alongside textual content.
- **Event Detection via Emotional Spikes**: Identifies events by detecting spikes in emotional expressions over time, rather than mere increases in keyword usage.

## Methodology
### 1. Preprocessing
- Cleansing tweets to remove noise and prepare data for further analysis.
- Processing emojis and emoticons to capture additional emotional context often omitted in text-only analyses.

### 2. Emotion Recognition
- Applying a CNN to each tweet to determine the intensity of the four targeted emotions.
- The model is trained to recognize nuanced emotional expressions, enhancing the accuracy of emotion detection.

### 3. Event Detection
- Monitoring the stream of tweets for emotional spikes within specified time windows.
- Declaring an event when there is a significant change in the collective emotional state of tweets.

## Getting Started

### Prerequisites
- Python 3.x
- TensorFlow or another compatible deep learning framework
- Libraries: NumPy, Pandas, Matplotlib (for data manipulation and visualization)
