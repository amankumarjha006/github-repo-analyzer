const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Language {
  name: string;
  percentage: number;
  color: string;
}

export interface Metrics {
  documentation_score: number;
  test_coverage: number;
  code_duplication: number;
  health_grade: string;
}

export interface Activity {
  date: string;
  commits: number;
}

export interface RepoAnalysis {
  repo_name: string;
  owner: string;
  stars: number;
  forks: number;
  open_issues: number;
  description: string;
  languages: Language[];
  metrics: Metrics;
  activity: Activity[];
}

export async function getHealth() {
    const response = await fetch(`${API_URL}/health`);
    return response.json();
}

export async function analyzeRepo(repoUrl: string): Promise<RepoAnalysis> {
  const response = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ repo_url: repoUrl }),
  });
  
  if (!response.ok) {
    throw new Error("Failed to analyze repository");
  }
  
  return response.json();
}