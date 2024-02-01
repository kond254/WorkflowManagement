import { Injectable } from '@angular/core';
import { WrappedSocket } from './wrapped.socket';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SocketService {
  constructor(private socket: WrappedSocket) {}

  onJobOfferUpdated(): Observable<any> {
    return this.socket.fromEvent('job_offer_updated');
  }

  onJobOfferAcceptedUpdated(): Observable<any> {
    return this.socket.fromEvent('job_offer__accepted_updated');
  }

  onJobStandardsUpdated(): Observable<any> {
    return this.socket.fromEvent('job_standards_updated');
  }

  onTopCandidatesUpdated(): Observable<any> {
    return this.socket.fromEvent('top_candidates_updated');
  }

}
