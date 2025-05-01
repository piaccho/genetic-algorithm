import logging
import os
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored timestamp"""
    
    # ANSI color codes
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    
    def format(self, record):
        # Store the original format
        orig_fmt = self._style._fmt
        
        # Apply colors to the datetime portion
        self._style._fmt = f"{self.BLUE}%(asctime)s{self.RESET} - %(message)s"
        
        # Call the original formatter's format method
        result = logging.Formatter.format(self, record)
        
        # Restore the original format
        self._style._fmt = orig_fmt
        
        return result

# Module-level logger instance - initialized on first use
_logger = None

def _initialize_logger():
    """Initialize the logger if not already done"""
    global _logger
    
    if _logger is not None:
        return _logger
        
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(log_dir, f"run_{time_stamp}.log")

    logger = logging.getLogger("GenAlgLogger")
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()

    # Standard formatter for file output (no colors)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(message)s",
        "[%Y-%m-%d][%H:%M:%S]"
    )

    # Colored formatter for console output
    console_formatter = ColoredFormatter(
        "%(asctime)s - %(message)s",
        "[%Y-%m-%d][%H:%M:%S]"
    )

    # Console handler with colored output
    ch = logging.StreamHandler()
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)

    # File handler (no colors in file)
    fh = logging.FileHandler(log_file)
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)
    
    _logger = logger
    return logger

# Expose logging methods directly
def log(msg, *args, **kwargs):
    if _logger is None:
        _initialize_logger()
    return _logger.info(msg, *args, **kwargs)
