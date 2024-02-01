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

interface TopCandidate {
  CandidateID: number;
  adress: string;
  age: number;
  city: string;
  country: string;
  email: string;
  first_name: string;
  gender: string;
  last_name: string;
  linkedin: string;
  previous_company: string;
  rating: number;
  zip_code: string; 
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

  // Funktion die top candidates vom backend abruft
  getTopCandidate(): Observable<any[]> {
    console.log("Data top candidates from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_top_candidates")
  }

  // Funktion die job standards vom backend abruft
  getJobStandards(): Observable<any[]> {
    console.log("Data job standards from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_job_standards")
  }

  // Funktion die job offer vom backend abruft
  getJobOffer(): Observable<any[]> {
    console.log("Data job offers from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_job_offer")
  }

   // Funktion die akzeptierte job offer vom backend abruft
   getJobOfferAccepted(): Observable<any[]> {
    console.log("Data accepted job offers from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_job_offer_accepted")
  }

  // Funktion die new employees vom backend abruft
  getNewEmployees(): Observable<any[]> {
    console.log("Data new employees from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_new_employees")
  }
  

  // Funktion die neuen job offer ans backend sendet
  sendJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log("Data new job offer sent to backend");
    return this.http.post<any>(this.apiUrl + "/add_job_offer", jobOffer); 
  }

  // Funktion die neuen job offer update ans backend sendet
  updateJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log(jobOffer.processID)
    console.log("Data update job offer sent to backend");
    return this.http.post<any>(this.apiUrl + "/update_job_offer", jobOffer); 
  }

  // Funktion die job offer delete ans backend sendet
  deleteJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log(jobOffer.processID)
    console.log("Data delete job offer sent to backend");
    return this.http.post<any>(this.apiUrl + "/delete_job_offer", jobOffer); 
  }

   // Funktion die neuen job standards ans backend gesendet
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
    console.log("Data job standards sent to backend");
    return this.http.post<any>(this.apiUrl + "/add_job_standards", jobStandards);
  }

  ////////////////////////////////////////////////////////
    // Funktion die neuen top candidate update ans backend sendet
    updateTopCandidate(topCandidate: TopCandidate): Observable<any> {
      console.log(topCandidate.CandidateID);
      console.log(topCandidate.adress);
      console.log(topCandidate.age);
      console.log(topCandidate.country);
      console.log(topCandidate.email);
      console.log(topCandidate.first_name);
      console.log(topCandidate.gender);
      console.log(topCandidate.last_name);
      console.log(topCandidate.linkedin);
      console.log(topCandidate.previous_company);
      console.log(topCandidate.rating);
      console.log(topCandidate.zip_code)
      console.log("Data update top candidate sent to backend");
      return this.http.post<any>(this.apiUrl + "/update_top_candidate", topCandidate); 
    }
  
    // Funktion die top Candidate delete ans backend sendet
    deleteTopCandidate(topCandidate: TopCandidate): Observable<any> {
      console.log(topCandidate.CandidateID);
      console.log(topCandidate.adress);
      console.log(topCandidate.age);
      console.log(topCandidate.country);
      console.log(topCandidate.email);
      console.log(topCandidate.first_name);
      console.log(topCandidate.gender);
      console.log(topCandidate.last_name);
      console.log(topCandidate.linkedin);
      console.log(topCandidate.previous_company);
      console.log(topCandidate.rating);
      console.log(topCandidate.zip_code)
      console.log("Data delete job offer sent to backend");
      return this.http.post<any>(this.apiUrl + "/delete_top_candidate", topCandidate); 
    }


}

 