# Fonte: AI-Powered Writing Assistant

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
   - [Frontend](#frontend)
   - [Backend](#backend)
3. [Technical Concepts](#technical-concepts)
   - [Python Generators](#python-generators)
   - [FastAPI Streaming Responses](#fastapi-streaming-responses)
4. [Getting Started](#getting-started)
5. [Future Topics](#future-topics)

## Project Overview

Fonte is an AI-powered writing assistant that helps users proofread and draft writing materials, from emails to academic papers. It leverages modern AI capabilities through Gemini's language models to provide intelligent writing assistance.

But it's mostly created for fun and myself because I often double-check my writings on POE. Plus I want to work on a side project so let's see if I can do it better.

## Architecture

### Frontend

- Vue.js with TypeScript
- TailwindCSS for styling

### Backend

- FastAPI Python backend
- Docker containerization
- Gemini API integration with streaming responses

## Technical Concepts

### Python Generators

Generators are a powerful Python feature used extensively in this project for streaming AI responses to the frontend. They allow functions to yield values one at a time and resume execution where they left off.

#### Key Generator Concepts

1. **Definition**: A generator is a function that returns an iterator which produces a sequence of values when iterated over.

2. **The `yield` Keyword**: Instead of returning a single value and terminating, generator functions use `yield` to produce a sequence of values. When a generator function reaches a `yield` statement:

   - It returns the yielded value
   - It pauses execution at that point
   - It preserves its entire state (variables, execution position)
   - When called again, it resumes from the line after the `yield`

3. **Creating a Generator**: Any function that contains at least one `yield` statement becomes a generator function. When called, it returns a generator object, not the function's result.

4. **One-time Consumption**: Once a value is yielded from a generator, it's consumed and can't be accessed again without recreating the generator.

#### Example from Fonte

In our backend, we use a generator to stream Gemini API responses to the client:

```python
# From backend/main.py
def gemini_stream():
    try:
        for chunk in response:
            if chunk.text:
                full_response.append(chunk.text)
                yield chunk.text

        # Save the assistant's response to chat history
        if full_response:
            complete_response = "".join(full_response)
            chats[chat_id].append({"role": "model", "message": complete_response})

            # Also yield the chat_id so the client knows it for future messages
            yield f"\n\n__CHAT_ID__:{chat_id}"
    except Exception as e:
        yield f"[ERROR] {str(e)}"
```

This generator:

1. Yields text chunks as they arrive from the Gemini API
2. Accumulates the complete response for saving to chat history
3. Yields a special marker with the chat ID at the end
4. Handles errors by yielding error messages

### FastAPI Streaming Responses

FastAPI provides the `StreamingResponse` class that works seamlessly with Python generators to enable server-sent events and streaming data to clients.

#### How It Works

1. **Creating the Streaming Response**: We pass our generator to `StreamingResponse`:

   ```python
   return StreamingResponse(gemini_stream(), media_type="text/plain")
   ```

2. **FastAPI's Processing**:

   - FastAPI doesn't wait for the generator to complete
   - It sets up appropriate HTTP headers for streaming content
   - It iterates through the generator, sending each yielded value to the client immediately
   - The client receives data incrementally, not all at once

3. **Client-Side Processing**:
   - The frontend uses the Fetch API's streaming capabilities
   - It processes each chunk as it arrives, updating the UI in real-time
   - This creates a responsive "typing" effect like modern AI assistants

## Getting Started

### Frontend Setup

```bash
cd frontend
yarn
yarn dev
```

### Backend Setup

```bash
cd backend
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

### Starting Docker Stack

```bash
cd backend
docker-compose -p "fonte-api" up --build
```
