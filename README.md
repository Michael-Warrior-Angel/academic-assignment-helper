# academic-assignment-helper
Academic Assignment Helper & Plagiarism Detector (RAG-Powered)

This project is a full-stack academic assignment helper that allows students to upload assignments and receive AI-powered analysis. It provides plagiarism detection, research suggestions, topic insights, and optional Slack notifications to the instructor. It integrates FastAPI backend, Neon PostgreSQL, n8n workflow automation, and OpenAI GPT analysis.
Features
•	Student registration and authentication using JWT.
•	Upload assignments via a secure API endpoint.
•	AI-powered assignment analysis, including:
o	Topic and key themes extraction.
o	Research questions suggestions.
o	Academic level estimation.
o	Suggested references and recommended citation format.
•	Plagiarism detection with similarity scoring.
•	Stores analysis results in a PostgreSQL database.
•	Optional Slack notifications for instructors.
Project Structure
•	backend/ contains:
o	main.py — FastAPI app entrypoint.
o	auth.py — JWT authentication and password handling.
o	models.py — SQLAlchemy models for students, assignments, analysis.
o	rag_service.py — RAG (retrieval-augmented generation) helper.
o	requirements.txt — Python dependencies.
o	Dockerfile — optional containerization.
•	workflows/ contains:
o	assignment_analysis_workflow.json — n8n workflow for automated assignment analysis.
Prerequisites
•	Python 3.12 or higher.
•	pip and virtualenv.
•	Neon PostgreSQL account.
•	Node.js 18+ for n8n.
•	n8n CLI (npm install -g n8n).
•	Optional: OpenAI API key.
•	Optional: Slack workspace and Slack App for notifications.
Setup Instructions
1.	Clone the repository:
o	Run git clone https://github.com/Michael-Warrior-Angel/academic-assignment-helper.git
o	Navigate into the project: cd academic-assignment-helper.
2.	Setup Python environment:
o	Navigate to backend: cd backend.
o	Create virtual environment: python -m venv venv.
o	Activate the environment: source venv/bin/activate (Linux/macOS) or venv\Scripts\activate (Windows).
o	Upgrade pip and install dependencies: pip install --upgrade pip and pip install -r requirements.txt.
3.	Configure PostgreSQL (Neon):
o	Create a Neon project and database.
o	Copy your connection string: postgresql://<user>:<password>@<host>/<database>?sslmode=require.
o	Connect using psql to verify tables exist (students, assignments, analysis_results, academic_sources).
4.	Configure FastAPI environment variables:
o	Set DATABASE_URL to your Neon connection string.
o	Set JWT_SECRET_KEY to a secret key for JWT tokens.
o	Set N8N_WEBHOOK_URL to your n8n tunnel URL, ending with /webhook/assignment-upload.
o	Set OPENAI_API_KEY if using AI analysis.
5.	Run FastAPI backend:
o	Execute uvicorn main:app --reload --host 0.0.0.0 --port 8000.
o	Test endpoints: register students, login, and upload assignments.
6.	Setup and run n8n:
o	Install n8n globally: npm install -g n8n.
o	Start n8n with tunnel: n8n start --tunnel.
o	Copy the generated tunnel URL.
o	Import workflow: n8n import:workflow --input workflows/assignment_analysis_workflow.json.
o	Activate the workflow in n8n editor.
7.	Configure OpenAI node in n8n:
o	In n8n, open AI Analysis node.
o	Add credentials with your OpenAI API key.
o	Select GPT-4 as the model.
8.	Configure Slack notifications (optional):
o	Create a Slack App in your workspace.
o	Enable chat:write scope.
o	Install app to workspace and copy Bot User OAuth Token.
o	Add token to Slack node in n8n.
o	Set the channel name (e.g., #instructors).
API Endpoints
•	POST /auth/register — register a new student.
•	POST /auth/login — login and receive JWT.
•	POST /assignments/upload — upload assignment files (PDF/DOCX).
•	GET /analysis/{id} — retrieve assignment analysis results.
n8n Workflow Overview
•	Webhook node receives assignment file upload.
•	Text Extraction node reads PDF/DOCX content.
•	RAG Source Search node fetches suggested references.
•	AI Analysis node provides GPT-powered insights.
•	Plagiarism Detection node flags potential plagiarism.
•	Store Results node saves output to PostgreSQL.
•	Slack Notification node optionally alerts instructors.
Troubleshooting
•	If FastAPI returns 404 for n8n webhook, ensure webhook URL ends with /webhook/assignment-upload.
•	If n8n tunnel is not accessible, kill existing instances and restart n8n start --tunnel.
•	If OpenAI node fails, verify that OPENAI_API_KEY is correct and valid.
•	Database errors usually indicate an incorrect Neon connection string or missing tables.

