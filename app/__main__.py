import os

from app.run import run

os.umask(0o022)    
    
if __name__ == "__main__":
    run()
