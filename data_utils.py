from dataclasses import dataclass, asdict
import pickle

## source concepts
@dataclass
class SourceConcept:
    concept_id: str
    concept_name: str

class SourceConceptDataset:
    def __init__(self):
        self.concepts = []
    
    def add_concept(self, concept):
        self.concepts.append(concept)
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.concepts, f)
    
    @classmethod
    def load(cls, filepath):
        dataset = cls()
        with open(filepath, 'rb') as f:
            dataset.concepts = pickle.load(f)
        return dataset

@dataclass
class TargetConcept:
    concept_id: str
    concept_name: str

class TargetConceptDataset:
    def __init__(self):
        self.concepts = []
    
    def add_concept(self, concept):
        self.concepts.append(concept)
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.concepts, f)
    
    @classmethod
    def load(cls, filepath):
        dataset = cls()
        with open(filepath, 'rb') as f:
            dataset.concepts = pickle.load(f)
        return dataset

@dataclass
class ConceptMapping:
    source_concept_id: str
    target_concept_id: str
    similarity_score: float



