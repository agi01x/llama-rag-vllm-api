qa_prompt_tmpl_str = (
"Context information is below.\n"
"---------------------\n"
"{context}\n"
"---------------------\n"
"Given the context information above I want you to think step by step to answer the query in a crisp manner, incase case you don't know the answer say 'I don't know!'.\n"
"Query: {query}\n"
"Answer: "
)