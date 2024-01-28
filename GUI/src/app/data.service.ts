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
  getnewEmployees(): Observable<any[]> {
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
  }

}

 