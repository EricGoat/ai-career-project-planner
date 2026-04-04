import { Component, ChangeDetectorRef } from '@angular/core'
import { CommonModule } from '@angular/common'
import { FormsModule } from '@angular/forms'
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
  imports: [CommonModule, FormsModule],
  templateUrl: './analyzer.html',
  styleUrls: ['./analyzer.css']
})
export class AnalyzerComponent {
  resumeText = ''
  jobText = ''
  result: Data | null = null

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  analyze() {
    console.log('Analyze clicked')

    this.result = null

    const resumePayload = { resume_text: this.resumeText }
    const jobPayload = { job_text: this.jobText }

    forkJoin({
      resume: this.http.post<any>('http://127.0.0.1:5000/api/resume/parse', resumePayload),
      job: this.http.post<any>('http://127.0.0.1:5000/api/job/analyze', jobPayload)
    }).pipe(
      switchMap(({ resume, job }) => {
        console.log('Resume response:', resume)
        console.log('Job response:', job)

        const combined = {
          resume_skills: resume.resume_skills,
          job_skills: job.job_skills
        }

        console.log('Sending combined:', combined)

        return this.http.post<any>('http://127.0.0.1:5000/api/recommend', combined)
      })
    ).subscribe(finalResponse => {
      console.log('Final response:', finalResponse)
      this.result = { ...finalResponse }
      this.cdr.detectChanges()
    })
  }
}
