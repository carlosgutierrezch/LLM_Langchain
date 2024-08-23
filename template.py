import os

def main():
    folders= [
        "app/api",
        "app/services",
        "app/utils"
    ]    

    files= [
            "app/__init__.py",
            "app/api/__init__.py",
            "app/api/routes.py",
            "app/utils/__init__.py",
            "app/services/anthropic_services.py",
            "app/services/ollama_services.py",
            "app/services/pinecone_services.py",
            "app/utils/__init__.py",
            "app/utils/helper_functions.py",
            "run.py"
    ]

    for folder in folders:
        os.makedirs(folder,exist_ok=True)
        
    for file in files:
        with open(file,'w') as f:
            pass
        
if __name__=='__main__':
    main()