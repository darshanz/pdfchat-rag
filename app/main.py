from flask import Flask, request, jsonify, render_template, send_file
from celery_worker import process_document_task, query_chroma
from pymongo import MongoClient 
from flask_socketio import SocketIO 
import os
import uuid
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = "NOT_SO_SECRET!!"  
socketio = SocketIO(app, message_queue='redis://redis:6379/0', cors_allowed_origins='*')

# MongoDB 
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/paper_xplainer")
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_database()

upload_folder = os.getenv("UPLOAD_FOLDER", "/uploads")
 
def get_paper_list():
    papers = db.papers.find().sort("date_created", -1).limit(10)
    paper_list = []
    for paper in papers:
        paper_list.append({
            "paper_id": paper["paper_id"],
            "filename": paper["filename"],
            "date_created": paper["date_created"],
            "date_updated": paper["date_updated"]
        })
    
    return paper_list
 
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", papers=get_paper_list())


@app.route("/upload", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
     
    paper_id = str(uuid.uuid4())
    paper_folder = os.path.join(upload_folder, paper_id)
    os.makedirs(paper_folder, exist_ok=True)
    filepath = f"{paper_folder}/{paper_id}.pdf"
    print(filepath)
    file.save(filepath)
 
    task = process_document_task.apply_async(args=[filepath, paper_id])
    
    # Save paper metadata to MongoDB
    db.papers.insert_one({
        "paper_id": paper_id,
        "file_path": filepath,
        "filename": file.filename,
        "date_created": datetime.utcnow().isoformat(),
        "date_updated": datetime.utcnow().isoformat()
    })

    # TODO handle failure cases later.. 
    return jsonify({"status": "success", "message": "File uploaded", "task_id": task.id, "paper_id":paper_id}), 202 

@app.route('/processing/<paper_id>', methods=['GET'])
def processing(paper_id):
    return render_template("processing.html", paper_id=paper_id, papers=get_paper_list())

@app.route('/paper/<paper_id>', methods=['GET'])
def paper_chat(paper_id):
    return render_template("pdf_chat.html", paper_id=paper_id, papers=get_paper_list())

 

@app.route("/paper-list/<page_num>", methods=["GET"])
def paper_list(page_num):
    paper_list= []
    page_size = 10
    skip = (int(page_num) - 1) * page_size
    papers = db.papers.find().sort("date_created", -1).skip(skip).limit(page_size)
    for paper in papers:
        paper_list.append({
            "paper_id": paper["paper_id"],
            "filename": paper["filename"],
            "date_created": paper["date_created"],
            "date_updated": paper["date_updated"]
        })
    if not paper_list:
        return jsonify({"error": "No more papers found"}), 404
    return paper_list

@app.route("/pdf/<paper_id>")
def serve_pdf(paper_id):
    paper_folder = os.path.join(upload_folder, paper_id)
    return send_file(f"{paper_folder}/{paper_id}.pdf")

@app.route("/send-chat", methods=["POST"])
def send_chat():
    data = request.json
    query_text = data.get("query")
    paper_id = data.get("paper_id")
    
    if not query_text or not paper_id:
        return jsonify({"error": "Missing query or paper_id"}), 400

    task = query_chroma.apply_async(args=[paper_id, query_text, 3])
    return jsonify({"status": "success", "task_id": task.id}), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
