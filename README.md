# News Headline Detector

## Overview
News Headline Detector is a simple web application that analyzes news headlines or article links and tells whether they are likely real or fake.  
Users can paste a headline or a news article URL to quickly check its authenticity.



## Features
- Accepts both a headline or a URL as input  
- Gives instant analysis of real or fake news  
- Shows a confidence score in percentage  
- Simple and easy to use interface, can be used through smart phones / laptop it is media friendly
- Lightweight and fast without relying on heavy external services  becuse we have used PAssive Aggressive Classifier  with TF-IDF parameter.



## Purpose
Fake news is a growing issue in today’s digital world.  
This project was created to provide a lightweight and accessible tool that helps people verify the credibility of news headlines before sharing them further.  



## How It Works
1. The user provides a headline or article URL  
2. The system extracts the news title  
3. It compares the text with patterns learned from real and fake news data  
4. The output includes:  
   - The analyzed headline  
   - The prediction result: Real or Fake  
   - A confidence percentage  



## Use Cases
- Individuals who want to verify trending news  
- Students and researchers studying media literacy  
- Everyday users looking for a quick credibility check before sharing news
- Journalist, News Channel editors can also use to before publishing  news coming via diffrent sources.


## Project Highlights
- Simple to use, no technical background needed  
- Focuses only on headlines, because tempering happens on headlines first.
- Tried to achieve novelty throught this approach without using paid API and LLM models .  
- Can be expanded further for more advanced use cases  
