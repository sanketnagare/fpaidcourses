"""
Logging configuration for FuckPaidCourses backend.
Provides structured, detailed logging with colors and timing.
"""

import logging
import sys
import time
from functools import wraps
from typing import Callable, Any


# ANSI color codes for terminal
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    # Background
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors and emojis."""
    
    LEVEL_COLORS = {
        logging.DEBUG: Colors.CYAN,
        logging.INFO: Colors.GREEN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.BG_RED + Colors.WHITE,
    }
    
    LEVEL_EMOJIS = {
        logging.DEBUG: "🔍",
        logging.INFO: "ℹ️ ",
        logging.WARNING: "⚠️ ",
        logging.ERROR: "❌",
        logging.CRITICAL: "🔥",
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, Colors.WHITE)
        emoji = self.LEVEL_EMOJIS.get(record.levelno, "")
        
        # Format timestamp
        timestamp = time.strftime("%H:%M:%S", time.localtime(record.created))
        
        # Format message
        formatted = f"{Colors.BOLD}{timestamp}{Colors.RESET} {emoji} {color}{record.getMessage()}{Colors.RESET}"
        
        # Add exception info if present
        if record.exc_info:
            formatted += f"\n{Colors.RED}{self.formatException(record.exc_info)}{Colors.RESET}"
        
        return formatted


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return the application logger."""
    logger = logging.getLogger("fpc")
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ColoredFormatter())
    
    logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_logging()


def log_timing(operation: str):
    """Decorator to log function execution time."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            logger.info(f"⏳ Starting: {operation}")
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start
                logger.info(f"✅ Completed: {operation} ({elapsed:.2f}s)")
                return result
            except Exception as e:
                elapsed = time.time() - start
                logger.error(f"Failed: {operation} ({elapsed:.2f}s) - {str(e)}")
                raise
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start = time.time()
            logger.info(f"⏳ Starting: {operation}")
            
            try:
                result = await func(*args, **kwargs)
                elapsed = time.time() - start
                logger.info(f"✅ Completed: {operation} ({elapsed:.2f}s)")
                return result
            except Exception as e:
                elapsed = time.time() - start
                logger.error(f"Failed: {operation} ({elapsed:.2f}s) - {str(e)}")
                raise
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper
    return decorator


class RequestLogger:
    """Context manager for logging request lifecycle."""
    
    def __init__(self, request_type: str, identifier: str = ""):
        self.request_type = request_type
        self.identifier = identifier
        self.start_time = None
        self.steps = []
    
    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"{'='*50}")
        logger.info(f"🚀 {Colors.BOLD}NEW REQUEST: {self.request_type}{Colors.RESET}")
        if self.identifier:
            logger.info(f"   📍 Target: {self.identifier[:80]}...")
        logger.info(f"{'='*50}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        
        if exc_type:
            logger.error(f"{'='*50}")
            logger.error(f"❌ REQUEST FAILED after {elapsed:.2f}s")
            logger.error(f"   Error: {exc_val}")
            logger.error(f"{'='*50}")
        else:
            logger.info(f"{'='*50}")
            logger.info(f"🎉 {Colors.GREEN}REQUEST COMPLETED in {elapsed:.2f}s{Colors.RESET}")
            logger.info(f"{'='*50}")
        
        return False
    
    def step(self, name: str, details: str = ""):
        """Log a step in the request."""
        step_num = len(self.steps) + 1
        self.steps.append(name)
        
        elapsed = time.time() - self.start_time
        
        if details:
            logger.info(f"   [{step_num}] {name}: {details} (+{elapsed:.2f}s)")
        else:
            logger.info(f"   [{step_num}] {name} (+{elapsed:.2f}s)")
    
    def detail(self, message: str):
        """Log additional detail."""
        logger.info(f"       ↳ {message}")
