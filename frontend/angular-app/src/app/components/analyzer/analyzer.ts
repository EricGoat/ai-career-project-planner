import { Component, ChangeDetectorRef, inject } from '@angular/core'
import { CommonModule } from '@angular/common'
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms'
import { HttpClient } from '@angular/common/http'
import { forkJoin, switchMap } from 'rxjs'

 interface Recommendation {
  skill: string[]
  project: string
  resource: string
}

interface Data {
  resume_skills: string[]
  job_skills: string[]
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
  result: Data | null = null
  readonly form = this.fb.nonNullable.group({
    resumeText: ['', Validators.required],
    jobText: ['', Validators.required]
  })

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  analyze() {
    if (this.form.invalid) {
      this.form.markAllAsTouched()
      return
    }

    this.result = null
    const { resumeText, jobText } = this.form.getRawValue()

    const resumePayload = { resume_text: resumeText }
    const jobPayload = { job_text: jobText }

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
}
