from dotenv import load_dotenv
load_dotenv('local_run.env')

import uvicorn
if __name__ == "__main__":

    uvicorn.run(
        "main_API:webapp",
        host="127.0.0.1",
        port=8000,
        reload=True,  # Automatyczne odświeżanie przy zmianach w kodzie
        workers=1
    )