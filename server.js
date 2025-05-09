const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 5000;

app.use(cors());

const jobs = [
  {
    id: 1,
    title: "Project Management Apprenticeship 2025",
    type: "Internship",
    company: "Google",
    salary: "Not Disclosed",
    location: "Brazil",
    address: "Google Brazil Office",
    applyLink: "https://www.google.com/about/careers/applications/jobs/results/78961405155254982-project-management-apprenticeship-2025-jovem-aprendiz"
  },
  {
    id: 2,
    title: "Software Engineering Intern 2025",
    type: "Internship",
    company: "Google",
    salary: "Not Disclosed",
    location: "Global",
    address: "Google Office",
    applyLink: "https://www.google.com/about/careers/applications/jobs/results/126134432737174214-software-engineering-intern-2025"
  },
  {
    id: 3,
    title: "Student Researcher (PhD) Winter/Summer 2025",
    type: "Internship",
    company: "Google",
    salary: "Not Disclosed",
    location: "Global",
    address: "Google Office",
    applyLink: "https://www.google.com/about/careers/applications/jobs/results/101250764885631686-student-researcher-phd-wintersummer-2025"
  },
  {
    id: 4,
    title: "Software Engineer III (Infrastructure Core)",
    type: "Full-Time",
    company: "Google",
    salary: "Competitive",
    location: "Global",
    address: "Google Headquarters",
    applyLink: "https://www.google.com/about/careers/applications/jobs/results/110690555461018310-software-engineer-iii-infrastructure-core"
  },
  {
    id: 5,
    title: "Software Engineer - Microsoft",
    type: "Full-Time",
    company: "Microsoft",
    salary: "Competitive",
    location: "Global",
    address: "Microsoft HQ",
    applyLink: "https://jobs.careers.microsoft.com/global/en/share/1818464/"
  },
  {
    id: 6,
    title: "Frontend Developer - LinkedIn",
    type: "Full-Time",
    company: "LinkedIn",
    salary: "Competitive",
    location: "India",
    address: "LinkedIn India",
    applyLink: "https://www.linkedin.com/jobs/view/4214535361/"
  },
  {
    id: 7,
    title: "Backend Developer - LinkedIn",
    type: "Full-Time",
    company: "LinkedIn",
    salary: "Competitive",
    location: "India",
    address: "LinkedIn India",
    applyLink: "https://www.linkedin.com/jobs/view/4208788502/"
  },
  {
    id: 8,
    title: "Content Development (English) Internship",
    type: "Internship",
    company: "Marpu Foundation",
    salary: "Stipend Available",
    location: "Work From Home",
    address: "Remote",
    applyLink: "https://internshala.com/internship/detail/work-from-home-content-development-english-internship-at-marpu-foundation1745671119"
  },
  {
    id: 9,
    title: "Java Development Internship",
    type: "Internship",
    company: "NatWest Group",
    salary: "Stipend Available",
    location: "Gurgaon, India",
    address: "NatWest Group Office",
    applyLink: "https://internshala.com/internship/detail/java-development-internship-in-gurgaon-at-natwest-group1744355521"
  },
  {
    id: 10,
    title: "Artificial Intelligence (AI) Internship",
    type: "Internship",
    company: "Hungama Digital Media",
    salary: "Stipend Available",
    location: "Noida, India",
    address: "Hungama Digital Media Office",
    applyLink: "https://internshala.com/internship/detail/artificial-intelligence-ai-internship-in-noida-at-hungama-digital-media-entertainment-private-limited1743823953"
  }
];

app.get('/api/internships', (req, res) => {
  res.json(jobs);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
