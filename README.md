# IT Career Guide AI

An AI-powered career guidance system that helps IT students and professionals find their ideal career path.

## What It Does

- Answers questions about IT careers
- Gives skill recommendations
- Suggests certifications
- Shows career paths
- Compares different careers

# Project Description
This application helps people explore IT careers and get personalized advice. You can ask questions like "What does a Cybersecurity Engineer do?" or "How to become a DevOps Engineer?" and the AI will give you detailed answers about skills, certifications, career paths, and salary expectations.

## Why I built this: 
Many people struggle to understand which IT career path is right for them. This app makes it easy to explore different options and get clear, actionable guidance.

## Who it's for:
IT students, career changers, and anyone curious about IT careers.

# Architecture Diagram
(drawio.io)
<img width="1222" height="720" alt="Architecture_Diagram" src="https://github.com/user-attachments/assets/a910e169-b305-4fa6-8427-4663e34f84ce" />

# Agent Communication Diagram
(drawio.io)
<img width="1062" height="827" alt="Agent_Communication_Diagram" src="https://github.com/user-attachments/assets/2cec77c2-6ac5-4bf8-af70-595e6005a458" />

## Model Selection Strategy
(drawio.io)
<img width="845" height="530" alt="Model Selection Strategy" src="https://github.com/user-attachments/assets/cc164df4-2408-464a-88d3-d8439964cc24" />

## Model Comparison

| Model    | Latency  | Context Window | Reasoning Quality|
| -------- | -------- | -------------- | ---------------- |
| Groq     | ~0.5s    |   8K tokens    | Good             |
|OpenRouter| ~2-3s    | 200K tokens    | Excellent        |

#### Why this strategy: 
I use Groq for simple tasks because it's fast. I use OpenRouter only for complex reasoning because it gives better quality answers.

# RAG Pipeline
### i. Knowledge Base

I created career documents for different IT roles:
| Career                | What's Included                             |
|-----------------------|---------------------------------------------|
| Cybersecurity	        | Skills, certifications, career path, salary |
| Software Developer	  | Skills, certifications, career path, salary |
| DevOps Engineer	      | Skills, certifications, career path, salary |
| Cloud Architect	      | Skills, certifications, career path, salary |
| AI/ML Engineer	      | Skills, certifications, career path, salary |

Each document contains practical career information that the AI uses to answer questions.

### ii. Chunking
I split each document into smaller pieces called "chunks" so the system can find the most relevant parts.
- Chunk size - 300 characters (Small enough to be specific)
- Overlap	30 - characters	(Keeps context between chunks)
- Method - Split by headings	(Preserves document structure)

### iii. Embedding

I used all-MiniLM-L6-v2 to convert text into numbers (embeddings). This helps the system find similar content.

### iv. Vector Store

I use ChromaDB to store all the document chunks and their embeddings.

### v. Retrieval

When user ask a question:

1. The question is converted to an embedding
2. ChromaDB finds the most similar document chunks
3. The top 3-5 results are retrieved
4. The AI uses this context to answer

## Links
- Live App: https://it-career-guide-ai-jrszdixb5jdrhntvhefmwf.streamlit.app/
- 
