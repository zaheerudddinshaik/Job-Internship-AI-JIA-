from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Short name expansion
short_form_mapping = {
    "ai": "Artificial Intelligence",
    "ml": "Machine Learning",
    "ds": "Data Science",
    "se": "Software Engineering",
    "cv": "Computer Vision",
    "nlp": "Natural Language Processing",
    "devops": "Development Operations",
    "cloud": "Cloud Computing",
    "blockchain": "Blockchain Development",
    "cybersec": "Cybersecurity",
    "web3": "Web3 Development",
    "qa": "Quality Assurance",
    "ui": "User Interface Design",
    "ux": "User Experience Design",
    "pm": "Product Management",
    "sde": "Software Development Engineer",
    "fullstack": "Full Stack Development",
    "fe": "Frontend Development",
    "be": "Backend Development",
    "quantum": "Quantum Computing",
    "vr": "Virtual Reality",
    "ar": "Augmented Reality",
    "iot": "Internet of Things",
    "bioinfo": "Bioinformatics",
    "robotics": "Robotics Engineering",
    "bigdata": "Big Data Analytics",
    "datasci": "Data Science",
    "medtech": "Medical Technology",
    "fintech": "Financial Technology",
    "autonomous": "Autonomous Vehicles Engineering"
}

# Trending job roles
job_database = [
    {"title": "AI Engineer", "skills": "Artificial Intelligence, Machine Learning, Deep Learning, Python, TensorFlow"},
    {"title": "Machine Learning Engineer", "skills": "Machine Learning, Python, Scikit-Learn, TensorFlow, NLP"},
    {"title": "Data Scientist", "skills": "Data Analysis, Machine Learning, Python, R, SQL"},
    {"title": "Software Engineer", "skills": "Software Development, Algorithms, Java, Python, C++"},
    {"title": "Full Stack Developer", "skills": "React, Node.js, MongoDB, Express, JavaScript"},
    {"title": "Frontend Developer", "skills": "HTML, CSS, JavaScript, React, UI Design"},
    {"title": "Backend Developer", "skills": "Node.js, Express, Python, SQL, APIs"},
    {"title": "Cybersecurity Analyst", "skills": "Network Security, Ethical Hacking, Risk Assessment, Penetration Testing"},
    {"title": "Cloud Solutions Architect", "skills": "AWS, Azure, Google Cloud, Cloud Architecture, DevOps"},
    {"title": "Blockchain Developer", "skills": "Solidity, Ethereum, Smart Contracts, Web3"},
    {"title": "DevOps Engineer", "skills": "CI/CD, AWS, Azure, Docker, Kubernetes"},
    {"title": "Product Manager", "skills": "Product Strategy, Roadmaps, Agile, User Research"},
    {"title": "UI/UX Designer", "skills": "Figma, Adobe XD, User Research, Wireframing"},
    {"title": "Data Engineer", "skills": "Big Data, Hadoop, Spark, ETL, SQL"},
    {"title": "Web3 Developer", "skills": "Smart Contracts, Blockchain, Ethereum, Solidity"},
    {"title": "AR/VR Developer", "skills": "Unity, Unreal Engine, Augmented Reality, Virtual Reality"},
    {"title": "Quantum Computing Researcher", "skills": "Quantum Algorithms, Qiskit, Quantum Mechanics"},
    {"title": "Internet of Things (IoT) Engineer", "skills": "Embedded Systems, Sensors, Connectivity, IoT Platforms"},
    {"title": "AI Research Scientist", "skills": "Deep Learning, Reinforcement Learning, Machine Learning, Research"},
    {"title": "Autonomous Vehicle Engineer", "skills": "Computer Vision, Deep Learning, Robotics, Control Systems"},
    {"title": "Robotics Engineer", "skills": "Robot Design, Motion Planning, Control Systems, ROS"},
    {"title": "Big Data Analyst", "skills": "Hadoop, Spark, BigQuery, Data Warehousing"},
    {"title": "Bioinformatics Scientist", "skills": "Genomics, Python, R, Computational Biology"},
    {"title": "Fintech Product Manager", "skills": "Finance, Banking Tech, Blockchain, APIs, Agile"},
    {"title": "Medical Technology Specialist", "skills": "Medical Devices, Healthcare IT, Clinical Trials"},
]

# Vectorizer
vectorizer = TfidfVectorizer()

# Build corpus
job_corpus = [job['skills'] for job in job_database]
job_vectors = vectorizer.fit_transform(job_corpus)

@app.route('/find_jobs', methods=['POST'])
def find_jobs():
    data = request.json
    user_skills = data.get('skills', [])

    if not user_skills:
        return jsonify({"error": "No skills provided"}), 400

    # Expand short forms
    expanded_skills = []
    for skill in user_skills:
        expanded_skills.append(short_form_mapping.get(skill.lower(), skill))

    user_query = " ".join(expanded_skills)
    user_vector = vectorizer.transform([user_query])

    similarities = cosine_similarity(user_vector, job_vectors).flatten()

    # Top 10 jobs
    top_indices = similarities.argsort()[-10:][::-1]

    results = []
    for idx in top_indices:
        job = job_database[idx]
        results.append({
            "title": job['title'],
            "skills_required": job['skills'],
            "similarity": round(float(similarities[idx]), 2)
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
