"""
Ontology Pipeline (ZenML step)
"""
from zenml import step
from world_model.ontology_builder import OntologyBuilder

@step
def ontology_step(config=None):
    """ZenML step for ontology building."""
    builder = OntologyBuilder(config)
    return builder.update("sample_concept")

def main():
    print(ontology_step())

if __name__ == "__main__":
    main() 