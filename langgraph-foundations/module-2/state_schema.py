import random
from typing import Literal, TypedDict, Callable, Type, Any, Dict
from dataclasses import dataclass
from pydantic import BaseModel, field_validator, ValidationError
from langgraph.graph import StateGraph, START, END

class TypedDictState(TypedDict):
    name: str
    mood: Literal["happy", "sad"]

def td_node_1(state: TypedDictState) -> Dict[str, str]:
    print("---Node 1 (TypedDict)---")
    return {"name": state["name"] + " is ... "}

def node_2(_: Any) -> Dict[str, str]:
    print("---Node 2---")
    return {"mood": "happy"}

def node_3(_: Any) -> Dict[str, str]:
    print("---Node 3---")
    return {"mood": "sad"}

def decide_mood(_: Any) -> Literal["node_2", "node_3"]:
    return "node_2" if random.random() < 0.5 else "node_3"

@dataclass
class DataclassState:
    name: str
    mood: Literal["happy", "sad"]

def attr_node_1(state: Any) -> Dict[str, str]:
    print("---Node 1 (attr access)---")
    return {"name": state.name + " is ... "}

class PydanticState(BaseModel):
    name: str
    mood: str

    @field_validator("mood")
    @classmethod
    def validate_mood(cls, value: str) -> str:
        if value not in ["happy", "sad"]:
            raise ValueError("Mood must be either 'happy' or 'sad'")
        return value

def build_graph(state_type: Type[Any], node_1: Callable[[Any], Dict[str, Any]]):
    builder = StateGraph(state_type)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)
    builder.add_edge(START, "node_1")
    builder.add_conditional_edges("node_1", decide_mood)
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)
    return builder.compile()

def demo_typed_dict():
    print("\n=== TypedDict State Demo ===")
    graph = build_graph(TypedDictState, td_node_1)
    result = graph.invoke({"name": "Lance", "mood": "happy"})
    print("Final State:", result)

def demo_dataclass():
    print("\n=== Dataclass State Demo ===")
    graph = build_graph(DataclassState, attr_node_1)
    result = graph.invoke(DataclassState(name="Lance", mood="happy"))
    print("Final State:", result)

def demo_pydantic():
    print("\n=== Pydantic State Demo ===")
    try:
        _ = PydanticState(name="Lance", mood="mad")
    except ValidationError as e:
        print("Validation Error (expected):", e.errors()[0]["msg"])
    graph = build_graph(PydanticState, attr_node_1)
    result = graph.invoke(PydanticState(name="Lance", mood="sad"))
    print("Final State:", result)

if __name__ == "__main__":
    random.seed(42)
    demo_typed_dict()
    demo_dataclass()
    demo_pydantic()
