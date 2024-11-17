from dataclasses import dataclass, asdict
import random
import string
import json
import pickle
from pathlib import Path
from data_utils import SourceConcept, SourceConceptDataset, TargetConcept, TargetConceptDataset, ConceptMapping 

def generate_fake_data(num_source=5000, num_target=5000):
    
    # source concepts
    source_dataset = SourceConceptDataset()
    for i in range(num_source):
        concept_id = f"S{str(i).zfill(5)}"
        # random strings of random length
        word_length = random.randint(4, 10)
        concept_name = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        source_dataset.add_concept(SourceConcept(concept_id, concept_name))
    
    # target concepts
    target_dataset = TargetConceptDataset()
    for i in range(num_target):
        concept_id = f"T{str(i).zfill(5)}"
        word_length = random.randint(4, 10)
        concept_name = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        target_dataset.add_concept(TargetConcept(concept_id, concept_name))
    
    # random mappings
    mappings = []
    for source_concept in source_dataset.concepts:
        target_concept = random.choice(target_dataset.concepts)
        # create random similarity score
        similarity = round(random.uniform(0.5, 1.0), 2)
        mapping = ConceptMapping(
            source_concept_id=source_concept.concept_id,
            target_concept_id=target_concept.concept_id,
            similarity_score=similarity
        )
        mappings.append(mapping)

    return source_dataset, target_dataset, mappings

def save_all_data(source_dataset, target_dataset, mappings):
    
    Path("data").mkdir(exist_ok=True)
    
    source_dataset.save("data/source_concepts.pkl")
    
    target_dataset.save("data/target_concepts.pkl")
    
    # try json for live data
    mappings_dict = [asdict(m) for m in mappings]
    with open("data/concept_mappings.json", "w") as f:
        json.dump(mappings_dict, f, indent=2)

if __name__ == "__main__":
    source_dataset, target_dataset, mappings = generate_fake_data()
    save_all_data(source_dataset, target_dataset, mappings)
    print("synthetic data generated and saved to /data")