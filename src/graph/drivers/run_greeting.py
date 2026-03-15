from src.graph.greeting_generator.graph import build_graph
from pprint import pprint

def main():
    app = build_graph()
    
    result = app.invoke({
        "name": "John",
        "is_valid": "",
        "greeting": "",
        "timestamp": ""
    })
    
    pprint(result)
    
if __name__ == "__main__":
    main()