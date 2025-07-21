from celery import Celery
from flask_socketio import SocketIO
import time
import uuid
from utils import generate_chunks_from_pdf
from chroma_client import ChromaDBClient
from llm_helper import OllamaClient
import re
import markdown

 
socketio = SocketIO(message_queue='redis://redis:6379/0')
chroma = ChromaDBClient()
ollama_client = OllamaClient()

celery_app = Celery(
    'worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)
 
@celery_app.task(bind=True)
def process_document_task(self, file_path, paper_id):
    print("Reading Document")
    chunks = generate_chunks_from_pdf(file_path)
    socketio.emit('task_progress', {
        'task_id': self.request.id,
        'progress': 20
    }) 
    # For now just adding basic metadata for the minimal working example. 
    metadatas = [{'paper_id': paper_id,'source': file_path, 'chunk_id': str(uuid.uuid4())} for _ in chunks]

    ids = [str(uuid.uuid4()) for _ in chunks]
    texts = [chunk.page_content for chunk in chunks]
    chroma.add_chunks(texts, metadatas, ids)

    socketio.emit('task_progress', {
        'task_id': self.request.id,
        'progress': 100
    })  
   
    return "done"
 

@celery_app.task(bind=True)
def query_chroma(self, paper_id, query_text, k=3):
    db_response =  chroma.query(paper_id, query_text, k=k) 
    chunks = db_response['documents'][0] # don't know why this is a list of lists, check later 
    context = "\n\n".join(chunks) 
    reply = ollama_client.generate(context=context, question=query_text)
    thinking_excluded =  re.sub(r"<think>.*?</think>\s*", "", reply, flags=re.DOTALL) # deepseek repsonses have <think> tags, remove them
    html_text = markdown.markdown(thinking_excluded)

    # send back the chat response
    socketio.emit('chat_response', {
        'task_id': self.request.id,
        'message': html_text
    }) 
    return "done"




 