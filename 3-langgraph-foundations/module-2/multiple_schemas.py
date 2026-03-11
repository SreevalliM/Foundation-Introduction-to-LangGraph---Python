from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

def private_state_example():
    class OverallState(TypedDict):
        foo: int

    class PrivateState(TypedDict):
        baz: int

    def node_1(state: OverallState) -> PrivateState:
        print("---Node 1---")
        return {"baz": state["foo"] + 1}

    def node_2(state: PrivateState) -> OverallState:
        print("---Node 2---")
        return {"foo": state["baz"] + 1}

    builder = StateGraph(OverallState)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2", END)

    graph = builder.compile()

    print("\n[Private State Example] Invoke with foo=1")
    output = graph.invoke({"foo": 1})
    print("Result:", output)
    return output

def single_schema_example():
    class OverallState(TypedDict):
        question: str
        answer: str
        notes: str

    def thinking_node(state: OverallState):
        return {"answer": "bye", "notes": "... his name is Lance"}

    def answer_node(state: OverallState):
        return {"answer": "bye Lance"}

    graph = StateGraph(OverallState)
    graph.add_node("answer_node", answer_node)
    graph.add_node("thinking_node", thinking_node)
    graph.add_edge(START, "thinking_node")
    graph.add_edge("thinking_node", "answer_node")
    graph.add_edge("answer_node", END)

    graph = graph.compile()

    print("\n[Single Schema Example] Invoke with question='hi'")
    output = graph.invoke({"question": "hi"})
    print("Result:", output)
    return output

def multiple_schema_example():
    class InputState(TypedDict):
        question: str

    class OutputState(TypedDict):
        answer: str

    class OverallState(TypedDict):
        question: str
        answer: str
        notes: str

    def thinking_node(state: InputState):
        return {"answer": "bye", "notes": "... his is name is Lance"}

    def answer_node(state: OverallState) -> OutputState:
        return {"answer": "bye Lance"}

    graph = StateGraph(
        OverallState,
        input_schema=InputState,
        output_schema=OutputState,
    )
    graph.add_node("answer_node", answer_node)
    graph.add_node("thinking_node", thinking_node)
    graph.add_edge(START, "thinking_node")
    graph.add_edge("thinking_node", "answer_node")
    graph.add_edge("answer_node", END)

    graph = graph.compile()

    print("\n[Multiple Schemas Example] Invoke with question='hi'")
    output = graph.invoke({"question": "hi"})
    print("Result (filtered to OutputState):", output)
    return output

if __name__ == "__main__":
    private_state_example()
    single_schema_example()
    multiple_schema_example()
