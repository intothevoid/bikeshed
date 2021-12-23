import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    portno = os.environ.get('PORT') or 8000
    uvicorn.run(app, port=portno, host="0.0.0.0")