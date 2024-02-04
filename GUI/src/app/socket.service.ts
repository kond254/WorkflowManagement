import { Injectable } from '@angular/core';
import { WrappedSocket } from './wrapped.socket';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})

//This class enables communication via WebSocket and is triggered by executing the methods (e.g. methods update sql table) in backend.py. This allows other components to be triggered to open an update for information.
export class SocketService {
  constructor(private socket: WrappedSocket) {}

  //This method returns an observable that listens for the job_offer_updated socket event. It makes it possible to receive notifications about updates to job offers.
  onJobOfferUpdated(): Observable<any> {
    return this.socket.fromEvent('job_offer_updated');
  }

  //This method returns an observable that listens for job_offer__accepted_updated socket event. It makes it possible to receive notifications about updates to accepted job offers.
  onJobOfferAcceptedUpdated(): Observable<any> {
    return this.socket.fromEvent('job_offer__accepted_updated');
  }

  //This method returns an observable that listens for the job_standards_updated socket event. It makes it possible to receive notifications about updates to job standards.
  onJobStandardsUpdated(): Observable<any> {
    return this.socket.fromEvent('job_standards_updated');
  }

  //This method returns an observable that listens for the top_candidates_updated socket event. It makes it possible to receive notifications about updates to top candidates.
  onTopCandidatesAcceptedUpdated(): Observable<any> {
    return this.socket.fromEvent('top_candidates_updated');
  }

  //This method returns an observable that listens for the temp_login_users_updated socket event. It makes it possible to receive notifications about updates to current user logins.
  onLoginUsersUpdated(): Observable<any> {
    return this.socket.fromEvent('temp_login_users_updated');
  }

  onJobOfferUpdatedAfterSend(): Observable<any> {
    return this.socket.fromEvent('job_offer_updated_after_send');
  }


  




}
