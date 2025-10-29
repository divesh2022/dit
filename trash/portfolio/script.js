// Dynamic skills
const skills = [
  "FastAPI & Modular Router Design",
  "SQL Server Triggers & Auditability",
  "AI/ML Integration (Gemini, TTS, Speech)",
  "UML & Graphviz Diagramming",
  "Secure Admin APIs",
  "Linux OS Deployment (EduNix)",
  "Medical Triage Workflow Modeling"
];

const skillsList = document.getElementById("skills-list");
skills.forEach(skill => {
  const li = document.createElement("li");
  li.textContent = skill;
  skillsList.appendChild(li);
});

// Dynamic projects (placeholder)
const projects = [
  {
    title: "EduNix OS",
    description: "Lightweight Linux OS for college labs with GUI, CD deployment, and onboarding docs."
  },
  {
    title: "Medical Triage Chatbot",
    description: "Escalation-aware chatbot with override logic and severity scoring."
  },
  {
    title: "PPDT Story Generator",
    description: "Multimodal AI tool for emotional inference and visual overlays."
  }
];

const projectContainer = document.getElementById("project-container");
projects.forEach(project => {
  const div = document.createElement("div");
  div.className = "project";
  div.innerHTML = `<h3>${project.title}</h3><p>${project.description}</p>`;
  projectContainer.appendChild(div);
});
