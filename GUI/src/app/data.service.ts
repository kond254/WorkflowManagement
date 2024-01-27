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
    return this.http.get<any[]>(this.apiUrl);
  }

  getTopCandidate(): Observable<any[]> {
    console.log("TopCandidates")
    return this.http.get<any[]>(this.apiUrl+"/get_job_information")
  }

}