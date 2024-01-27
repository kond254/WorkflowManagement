import { Injectable, Type } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataServiceInterface {

  private apiUrl = 'http://127.0.0.1:5000/api/data';

  constructor(private http: HttpClient) { }

  getData(): Observable<any[]> {
    console.log("TestAufruf")
    return this.http.get<any[]>(this.apiUrl+"/get_jcandidate");
  }

  getTopCandidate(): Observable<any[]> {
    console.log("TopCandidates")
    return this.http.get<any[]>(this.apiUrl+"/get_job_information")
  }

  //Hier ist die neue Funktion 
  getJobOffer(): Observable<any[]> {
    console.log("JobOffers")
    return this.http.get<any[]>(this.apiUrl+"/get_job_offer")
  }

  // Hier ist die neue send funktion
//   sendJobOffer(caData: any): Observable<any> {
//     console.log("Sending Job Offer:", candidateData);
//     return this.http.post<any>(`${this.apiUrl}/send_candidndidateate`, candidateData);
// }

}

 