from langchain_community.document_loaders import UnstructuredURLLoader

from utils.parser import parse_query
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from utils.spoon_api import *

load_dotenv()
openai_key = os.getenv("openai_key")
os.environ['OPENAI_API_KEY'] = openai_key


class RecipeModel:

    def __init__(self, dish):
        self.llm = OpenAI(temperature=0.7, max_tokens=700)
        self.chain = None
        self.loaders = None
        self.docs = None
        self.vector_index = None
        self.recipe_urls = []

        self.get_recipe_urls(dish)
        self.set_loader()
        self.set_text_spliter()
        self.create_vectorstore()
        self.set_chain()

    def get_recipe_urls(self, dish):
        response_urls = get_spoonacular_recipe(dish, 5)
        self.recipe_urls = response_urls

    def set_loader(self):
        self.loaders = UnstructuredURLLoader(urls=self.recipe_urls)

    def set_text_spliter(self):
        text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        data = self.loaders.load()
        self.docs = text_spliter.split_documents(data)

    def create_vectorstore(self):
        embedder = OpenAIEmbeddings()
        self.vector_index = FAISS.from_documents(self.docs, embedder)

    def set_chain(self):

        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # or use "map_reduce" / "refine" if applicable
            retriever=self.vector_index.as_retriever(),
            return_source_documents=True
        )

    def ask_query(self, question):
        # langchain.debug = True
        result = self.chain({"query": question})
        if isinstance(result, dict):
            return {
                "result": result.get("result"),
                # "source_documents": [doc.to_dict() for doc in result.get("source_documents", [])]
            }
        else:
            # If it's not a dictionary, handle other cases
            return {"result": result}
#
# query = "Ingredients for blueberry cheesecake?"
#
# dish = parse_query(query)
# print(dish, "--dish--")
#
# recipeModel = RecipeModel(dish)
# response = recipeModel.ask_query(query)
# print(response)
