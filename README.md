# CS50 Final Project – Stock Analyzer

Currently in development. Python app that uses API data to display and analyze historical stock prices.

 # To Do

- Add clear instructions and requirements for setup (installation guide, `requirements.txt`)
- Improve DCF calculation logic (assumptions, model structure, valuation accuracy)
- Increase robustness against invalid input and API failures
- Integrate additional valuation methods (e.g. multiples, dividend discount model)
- Consider building a proper UI (e.g. command line interface, web interface)

# Update 3 (30.07.2025): 

Core functionality has been implemented successfully and is producing initial results. The current focus is on:

- Improving calculation logic and overall stability
- Handling API rate limits (Alpha Vantage)
- Refactoring for better code structure and reusability

# AI Usage

Artificial intelligence tools (such as ChatGPT) have been used exclusively for debugging support and syntax clarification during development.
All core logic, architectural decisions, and code structure have been designed and implemented independently by the developer.
The goal is to strengthen personal programming and problem-solving skills while using AI as a learning and troubleshooting assistant — not as a code generator.

# Update 2 (28.07.2025): 

- First working version of Free Cash Flow history and CAGR logic
- Growth assumptions and average FCF margins integrated
- Connected FRED API for 10-year treasury yield as risk-free rate

# Update 1 (23.07.2025): Switched from yfinance to Alpha Vantage

Switched because yfinance does not provide enough data for a professional DCF calculation.



