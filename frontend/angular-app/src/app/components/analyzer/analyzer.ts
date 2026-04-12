import { Component, ChangeDetectorRef, inject } from '@angular/core'
import { CommonModule } from '@angular/common'
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms'
import { HttpClient } from '@angular/common/http'
import { forkJoin, switchMap } from 'rxjs'

interface Recommendation {
  skill: string
  category: string
  project: string
  resource: string
  resource_link: string
}

type SkillCategories = Record<string, string[]>

interface Data {
  resume_skills: string[]
  job_skills: string[]
  missing_skill_categories: SkillCategories
  missing_skills: string[]
  recommendations: Recommendation[]
}

@Component({
  selector: 'app-analyzer',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './analyzer.html',
  styleUrls: ['./analyzer.css']
})
export class AnalyzerComponent {
  private readonly fb = inject(FormBuilder)
  readonly categoryOrder = [
    'languages',
    'cloud_services',
    'databases',
    'frameworks',
    'devops',
    'version_control',
    'ai_ml',
    'other'
  ]
  result: Data | null = null
  selectedResumeFile: File | null = null
  readonly form = this.fb.nonNullable.group({
    targetRole: ['', Validators.required]
  })

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  onResumeFileSelected(event: Event) {
    const input = event.target as HTMLInputElement
    this.selectedResumeFile = input.files?.[0] ?? null
  }

  analyze() {
    if (this.form.invalid || !this.selectedResumeFile) {
      this.form.markAllAsTouched()
      return
    }

    this.result = null
    const { targetRole } = this.form.getRawValue()

    const resumePayload = new FormData()
    resumePayload.append('resume_file', this.selectedResumeFile)
    const jobPayload = { target_role: targetRole }

    forkJoin({
      resume: this.http.post<any>('http://127.0.0.1:5000/api/resume/parse', resumePayload),
      job: this.http.post<any>('http://127.0.0.1:5000/api/job/analyze', jobPayload)
    }).pipe(
      switchMap(({ resume, job }) => {
        const combined = {
          resume_skills: resume.resume_skills,
          job_skills: job.job_skills
        }

        return this.http.post<any>('http://127.0.0.1:5000/api/recommend', combined)
      })
    ).subscribe(finalResponse => {
      this.result = { ...finalResponse }
      this.cdr.detectChanges()
    })
  }

  getVisibleCategories(categories: SkillCategories): Array<{ key: string, label: string, skills: string[] }> {
    return this.categoryOrder
      .map(key => ({
        key,
        label: this.formatCategoryLabel(key),
        skills: categories[key] ?? []
      }))
      .filter(category => category.skills.length > 0)
  }

  private formatCategoryLabel(category: string): string {
    return category
      .split('_')
      .map(part => part.charAt(0).toUpperCase() + part.slice(1))
      .join(' ')
  }
}
