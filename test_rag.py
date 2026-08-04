from rag import ask_question

print("=" * 60)
print("📚 Academic Notes AI Chatbot")
print("=" * 60)

while True:

    question = input("\nAsk a Question (type exit to quit): ")

    if question.lower() == "exit":
        break

    result = ask_question(question)

    print("\n🤖 ANSWER")
    print("=" * 60)
    print(result["answer"])

    print("\n📚 SOURCES")
    print("=" * 60)

    if result["sources"]:

        for source in result["sources"]:
            print("•", source)

    else:
        print("No source documents found.")

    print("=" * 60)