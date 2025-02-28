from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/package_digistump_index.json")
async def get_package_digistump_index():
    # Return the file as a response
    return FileResponse("package_digistump_index.json")
