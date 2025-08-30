# Web Reader

A Python tool for scraping and summarizing website content using OpenAI's GPT models.

## Features

- **Website Scraping**: Extract text content from any website
- **AI-Powered Summaries**: Generate intelligent summaries using OpenAI's GPT-4o-mini
- **Price Detection**: Specifically designed to identify and summarize pricing information
- **Clean Text Processing**: Removes navigation elements and cleans up content for better analysis
- **Error Handling**: Robust error handling for network issues and parsing problems

## Installation

1. Clone this repository:
```bash
git clone https://github.com/pppop00/webreader.git
cd webreader
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy `env.example` to `.env`
   - Add your OpenAI API key to the `.env` file
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

```bash
cp env.example .env
# Edit .env and add your API key
```

## Usage

### Basic Usage

```python
from web_reader import WebReader

# Initialize the Web Reader
reader = WebReader()

# Summarize a website
url = "https://example.com"
summary = reader.summarize(url)
print(summary)
```

### Command Line Usage

Run the script directly to test with the default example:

```bash
python web_reader.py
```

### Custom System Prompts

You can customize the AI's behavior by setting a custom system prompt:

```python
reader = WebReader()
reader.set_system_prompt("You are a technical analyst. Summarize the technical specifications and features.")
summary = reader.summarize("https://example.com")
```

## Classes

### `Website`
Handles website scraping and content extraction.
- Automatically extracts title and clean text content
- Removes scripts, styles, and navigation elements
- Handles network errors gracefully

### `WebReader`
Main class for AI-powered website analysis.
- Manages OpenAI API integration
- Validates API keys
- Generates structured prompts for better AI responses
- Handles summarization workflow

## Configuration

The tool uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for website scraping and API calls

## Dependencies

- `requests`: For web scraping
- `beautifulsoup4`: For HTML parsing
- `python-dotenv`: For environment variable management
- `openai`: For AI-powered summaries
- `ipython`: For enhanced display capabilities

## Error Handling

The tool includes comprehensive error handling for:
- Invalid or missing API keys
- Network connection issues
- Website parsing errors
- OpenAI API errors

## License

This project is open source. Feel free to use and modify as needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

If you encounter any issues, please check:
1. Your API key is correctly set in the `.env` file
2. Your internet connection is stable
3. The target website is accessible

For additional help, please open an issue in the GitHub repository.
