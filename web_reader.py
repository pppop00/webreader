"""
Web Reader - A tool for scraping and summarizing website content using OpenAI
"""

import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI


class Website:
    """
    A utility class to represent a website and extract its content
    """
    
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.text = ""
        self._scrape()
    
    def _scrape(self):
        """Scrape the website content"""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            self.title = title_tag.get_text().strip() if title_tag else "No Title Found"
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            self.text = soup.get_text()
            
            # Clean up text - remove extra whitespace
            lines = (line.strip() for line in self.text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            self.text = ' '.join(chunk for chunk in chunks if chunk)
            
        except requests.exceptions.RequestException as e:
            self.title = "Error loading website"
            self.text = f"Failed to load website: {str(e)}"
        except Exception as e:
            self.title = "Error parsing website"
            self.text = f"Failed to parse website content: {str(e)}"


class WebReader:
    """
    Main class for the Web Reader functionality
    """
    
    def __init__(self):
        # Load environment variables
        load_dotenv(override=True)
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # Validate API key
        self._validate_api_key()
        
        # Initialize OpenAI client
        self.openai = OpenAI()
        
        # Default system prompt
        self.system_prompt = """You are an assistant that analyzes the contents of a website 
and provides a short summary of price, ignoring text that might be navigation related. 
Respond in markdown."""
    
    def _validate_api_key(self):
        """Validate the OpenAI API key"""
        if not self.api_key:
            raise ValueError("No API key was found - please check your .env file!")
        elif not self.api_key.startswith("sk-proj-"):
            raise ValueError("API key doesn't start with sk-proj-; please check you're using the right key")
        elif self.api_key.strip() != self.api_key:
            raise ValueError("API key has whitespace at start or end - please remove them")
        else:
            print("API key found and looks good!")
    
    def set_system_prompt(self, prompt):
        """Set a custom system prompt"""
        self.system_prompt = prompt
    
    def user_prompt_for(self, website):
        """Generate user prompt for a website"""
        user_prompt = f"You are looking at a website titled {website.title}"
        user_prompt += "\nThe contents of this website is as follows; "
        user_prompt += "please provide a short summary of this website in markdown. "
        user_prompt += "If it includes news or price, then summarize these too.\n\n"
        user_prompt += website.text
        return user_prompt
    
    def messages_for(self, website):
        """Create message structure for OpenAI API"""
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt_for(website)}
        ]
    
    def summarize(self, url):
        """
        Scrape a website and generate a summary using OpenAI
        
        Args:
            url (str): The URL of the website to summarize
            
        Returns:
            str: The generated summary
        """
        try:
            website = Website(url)
            
            if website.title.startswith("Error"):
                return f"Failed to process website: {website.text}"
            
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages_for(website)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def test_connection(self):
        """Test the OpenAI connection"""
        try:
            message = "Hello, GPT! This is a test message. Please reply with a random number."
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Connection test failed: {str(e)}"


def main():
    """Main function for testing the Web Reader"""
    try:
        # Initialize Web Reader
        reader = WebReader()
        
        # Test connection
        print("Testing OpenAI connection...")
        test_result = reader.test_connection()
        print(f"Test result: {test_result}\n")
        
        # Example usage
        url = "https://www.avaloncommunities.com/massachusetts/somerville-apartments/avalon-at-assembly-row"
        print(f"Summarizing website: {url}")
        print("=" * 50)
        
        summary = reader.summarize(url)
        print(summary)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
