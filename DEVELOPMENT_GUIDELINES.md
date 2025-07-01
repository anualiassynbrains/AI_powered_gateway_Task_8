 Groq-powered summarization Service

Environment & Dependencies
--------------------------

*   Use **Poetry** for dependency management: 
    
*   poetry init
    
    poetry add fastapi uvicorn pydantic redis python-dotenv groq
    
*   Core Concepts
    -------------
    
    ### 1\. **FastAPI App (`main.py`)**
    
    *   Exposes a `/summarize` POST endpoint
        
    *   Parses input text using `Textdata` Pydantic model
        
    *   Injects rate limiting logic with:
        
    *   cost\_dependency = Annotated\[dict, Depends(cost\_based\_limiter)\]
        
    *   ### **Rate Limiting (`auth/rate_limiter.py`)**
        
        *   Checks if user has enough balance in Redis (based on `X-API-Key`)
            
        *   Calculates estimated cost using the `estimate_cost_request()` function
            
        *   If allowed, it decrements the balance and returns cost + remaining credits
            
    ### **Summarization Logic (`phase1/summarizer.py`)**
            
            *   Uses `llama3-70b-8192` via Groq API to summarize text
                
            *   Wraps output cleanly and returns trimmed response
                
    ### **Cost Estimation (`phase1/costestimator.py`)**
                
                *   Sends text to Groq and gets a numeric "cost" between 1–10
                    
                *   Parses Groq’s raw JSON-like response to extract cost
                    
                
    **Logging & Debugging**
                    
                    *   Print model outputs during dev (`print("Raw Model Output:", content)`)
                        
                    *   Add logging later for better traceability
                        
                
    **Async/Await Awareness**
                    
                    *   Use `async` Redis client and `await` all I/O
                        
                    *   Set event loop policy on Windows as you’ve done:
    

    ### How to run
```bash
cd src
cd costmanagement
uvicorn main:app--reload
```