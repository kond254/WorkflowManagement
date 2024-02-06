import { Injectable, Type } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

//This interface defines the structure of the JobOffer Object
interface JobOffer {
  processID: number;
  professionTitel: string;
  professionType: string;
  numberProfessions: number;
  description: string;
}

//This interface defines the structure of the Contract Object
interface Contract{
  ProcessID: number,
  numberProfessions: number,
  suggestion: number,
  compensation: number,
  professionType: string
}

//This interface defines the structure of the JobStandards Object
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

//This interface defines the structure of the JobStandardsWithTopCandidates Object
interface JobStandardsWithTopCandidates {
  AnnualSalary: number;
  Benefits: string;
  CandidateID: number;
  GraduationLevel: string;
  Industry: string;
  JobDescription: string;
  JobMode: string;
  JobTitle: string;
  JobType: string;
  Language: string;
  Location: string;
  PaidTimeOff: number;
  ProcessID: number;
  RequiredExperience: number;
  Responsibilities: string;
  WeeklyHours: number;
  address: string;
  age: number;
  city: string;
  country: string;
  email: string;
  first_name: string;
  gender: string;
  last_name: string;
  linkedin: string;
  numberOfPositions: number | null;
  previous_company: string;
  rating: number;
  zip_code: string;
  hrmanagerAccepted: boolean;
}

interface JobStandardsWithTopCandidatesRating{
  AnnualSalary: number;
  Benefits: string;
  CandidateID: number;
  GraduationLevel: string;
  Industry: string;
  JobDescription: string;
  JobMode: string;
  JobTitle: string;
  JobType: string;
  Language: string;
  Location: string;
  PaidTimeOff: number;
  ProcessID: number;
  RequiredExperience: number;
  Responsibilities: string;
  WeeklyHours: number;
  address: string;
  age: number;
  city: string;
  country: string;
  email: string;
  first_name: string;
  gender: string;
  last_name: string;
  linkedin: string;
  numberOfPositions: number | null;
  previous_company: string;
  rating: number;
  zip_code: string;
  hrmanagerAccepted: boolean;
  ratingHrManager: number;
  ratingHrRepresentative: number;
  ratingVP: number;
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

  // The getTopCandidate() method is used to retrieve the top candidate from the backend.
  getTopCandidate(): Observable<any[]> {
    console.log("Data top candidates from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_top_candidates")
  }

  // The getTopCandidateAccepted() method is used to retrieve the top candidate that are accepted by the hrmanager from the backend.
  getTopCandidateAccepted(): Observable<any[]> {
    console.log("Data accepted top candidates from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_top_candidates_accepted")
  }

   // The getJobStandards() method is used to retrieve the job standards that created by the hrmanager from the backend.
  getJobStandards(): Observable<any[]> {
    console.log("Data job standards from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_job_standards")
  }

   // The getJobOffer() method is used to retrieve the job offers that created by the hrdepartment from the backend.
  getJobOffer(): Observable<any[]> {
    console.log("Data job offers from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_job_offer")
  }

    // The getJobOfferAccepted() method is used to retrieve the job offer that are accepted by the hrmanager from the backend.
   getJobOfferAccepted(): Observable<any[]> {
    console.log("Data accepted job offers from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_job_offer_accepted")
  }

  // The getNewEmployees() method is used to retrieve the new employees who were successfully hired in the process.
  getNewEmployees(): Observable<any[]> {
    console.log("Data new employees from backend retrieved")
    return this.http.get<any[]>(this.apiUrl+"/get_new_employees")
  }
  

  // The sendJobOffer() method is used to send a new job offer that is created by the hrdepartment in the GUI to the backend.
  sendJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log("Data new job offer sent to backend");
    return this.http.post<any>(this.apiUrl + "/add_job_offer", jobOffer); 
  }

  // This method is used to update the status of an accepted job offer in the backend
  updateJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log(jobOffer.processID)
    console.log("Data update job offer sent to backend");
    return this.http.post<any>(this.apiUrl + "/update_job_offer", jobOffer); 
  }

// This method is used to update the status of an accepted job offer after a jop standard is created for it in the backend
  updateJobOfferAfterSend(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log(jobOffer.processID)
    console.log("Data update job offer sent to backend");
    return this.http.post<any>(this.apiUrl + "/update_job_offer_after_send", jobOffer); 
  }


  // This method is used to delete a rejected job offer in the backend
  deleteJobOffer(jobOffer: JobOffer): Observable<any> {
    console.log(jobOffer.professionTitel);
    console.log(jobOffer.professionType);
    console.log(jobOffer.numberProfessions);
    console.log(jobOffer.description);
    console.log(jobOffer.processID)
    console.log("Data delete job offer sent to backend");
    return this.http.post<any>(this.apiUrl + "/delete_job_offer", jobOffer); 
  }

   // The sendStandards() method is used to send a new job standards that is created by the hrmanager in the GUI to the backend.
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

  
    // This method updates a top candidate in the backend after he/she was accepted by the hrmanager.
    updateTopCandidate(topCandidate: JobStandardsWithTopCandidates): Observable<any> {
      console.log(topCandidate.CandidateID);
      console.log(topCandidate.address);
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
      return this.http.post<any>(this.apiUrl + "/update_top_candidates", topCandidate); 
    }
  
    // This method delets a top candidate in the backend.
    deleteTopCandidate(topCandidate: JobStandardsWithTopCandidates): Observable<any> {
      console.log(topCandidate.CandidateID);
      console.log(topCandidate.address);
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

    //The getCurrentSuggestions() method retries the current contracts suggestions from the backend
    getCurrentSuggestions(): Observable<any[]>{
      return this.http.get<any[]>(`${this.apiUrl}/get_current_contracts_suggestions`);
    }

    //The postCurrentContractSuggestion() method sends the current contracts suggestions to the backend
    postCurrentContractSuggestion(data: Contract): Observable<any []>{
      return this.http.post<any>(`${this.apiUrl}/post_current_contracts_suggestions`, data);
    }

    //The getJobStandardsWithCandidates method retrieves the top candidates for the specified job standards from the backend.
    getJobStandardsWithCandidates(jobStandards: number): Observable<any[]> {
      const params = new HttpParams().set('ProcessID', jobStandards.toString());
      return this.http.get<any[]>(`${this.apiUrl}/get_jobstandards_with_top_candidates`, {params} );
    }
  
  // The setLoginUser method adds a logged-in user to the backend.
  setLoginUser(username: string, isLoggedIn: boolean): Observable<any> {
    const data = { username: username, isLoggedIn: isLoggedIn };
    return this.http.post<any>(`${this.apiUrl}/add_login_user`, data);
  }

  // The getLoginUsers() method retrieves the list of logged-in users from the backend.
  getLoginUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/get_login_users`);
  }

  // The deleteLoginUser(username: string) method deletes a logged-in user from the backend.
  deleteLoginUser(username: string): Observable<any> {
    const data = { username: username };
    return this.http.post<any>(`${this.apiUrl}/delete_login_user`, data);
  }

  getJobStandardsWithCandidatesCurrently(jobStandards: number): Observable<any[]> {
    const params = new HttpParams().set('ProcessID', jobStandards.toString());
    return this.http.get<any[]>(`${this.apiUrl}/get_jobstandards_with_top_candidates_only_one`, {params} );
  }

  getJobStandardsWithCandidatesCurrentlyForInterview(jobStandards: number): Observable<any[]> {
    const params = new HttpParams().set('ProcessID', jobStandards.toString());
    return this.http.get<any[]>(`${this.apiUrl}/get_jobstandards_with_top_candidates_only_one_for_interview`, {params} );
  }

    // This method sets interview results
    set_interview_results(topCandidate: JobStandardsWithTopCandidatesRating): Observable<any> {
      console.log("Data delete job offer sent to backend");
      return this.http.post<any>(this.apiUrl + "/set_interview_results_for_candidate", topCandidate); 
    }

}

 