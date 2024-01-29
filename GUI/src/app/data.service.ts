import { Injectable, Type } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface JobOffer {
  processID: number;
  professionTitel: string;
  professionType: string;
  numberProfessions: number;
  description: string;
}

interface JobStandards{
  ProcessID: number;
  JobTitle: string;
  JobType: string;
  RequiredExperience: number;
  JobDescription: string;
  Responsibilities: string;
  Location: string;
  JobMode: string;
  WeeklyHours: number;
  AnnualSalary: number;
  PaidTimeOff: number;
  Benefits: string;
  Industry: string;
  GraduationLevel: string; 
  Language: string;
  numberOfPositions: number;
}


@Injectable({
  providedIn: 'root'
})
export class DataServiceInterface {

  private apiUrl = 'http://127.0.0.1:5000/api/data';

  constructor(private http: HttpClient) { }

  // getData(): Observable<any[]> {
  //   console.log("TestAufruf")
  //   return this.http.get<any[]>(this.apiUrl+"/get_job_candidate");
  // }

  getTopCandidate(): Observable<any[]> {
    console.log("TopCandidates")
    return this.http.get<any[]>(this.apiUrl+"/get_top_candidates")
  }

  getJobStandards(): Observable<any[]> {
    console.log("JobStandards")
    return this.http.get<any[]>(this.apiUrl+"/get_job_standards")
  }

  //Hier werden die neuen Job Angebote abgefragt
  getJobOffer(): Observable<any[]> {
    console.log("JobOffers")
    return this.http.get<any[]>(this.apiUrl+"/get_job_offer")
  }

  //Hier ist die eingestellten Employees abgefragt
  getNewEmployees(): Observable<any[]> {
    console.log("NewEmployees")
    return this.http.get<any[]>(this.apiUrl+"/get_new_employees")
  }
  

  // Hier werden die neuen Job Offer ans Backend gesendet
  sendJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    return this.http.post<any>(this.apiUrl + "/add_job_offer", jobOffer); 

    // backend wird hier aufgerufen 

  }

  //update hier schreiben
  updateJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log(jobOffer.processID)
    return this.http.post<any>(this.apiUrl + "/update_job_offer", jobOffer); 
  }

  deleteJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log(jobOffer.processID)
    return this.http.post<any>(this.apiUrl + "/delete_job_offer", jobOffer); 
  }



   // Hier werden die neuen Job Standards ans Backend gesendet
   sendJobStandards(jobStandards: JobStandards): Observable<any> {
    console.log(jobStandards.JobTitle);
    console.log(jobStandards.JobType);
    console.log(jobStandards.RequiredExperience);
    console.log(jobStandards.JobDescription);
    console.log(jobStandards.Responsibilities);
    console.log(jobStandards.Location);
    console.log(jobStandards.JobMode);
    console.log(jobStandards.WeeklyHours);
    console.log(jobStandards.AnnualSalary);
    console.log(jobStandards.PaidTimeOff);
    console.log(jobStandards.Benefits);
    console.log(jobStandards.Industry);
    console.log(jobStandards.GraduationLevel);
    console.log(jobStandards.Language);
    console.log(jobStandards.numberOfPositions);
    return this.http.post<any>(this.apiUrl + "/add_job_standards", jobStandards);
  }


}

 