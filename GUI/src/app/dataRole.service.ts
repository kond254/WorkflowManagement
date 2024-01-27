import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


interface DataRoleServiceService {

  [key: string]: {
    home: boolean;
    hrdepartment: boolean;
    hrmanagement: boolean;
    accounting: boolean;
  };
}

@Injectable({
  providedIn: 'root',
})

export class DataRoleService {

  private home: boolean = false;
  private hrdepartment: boolean = false;
  private hrmanagement: boolean = false;
  private accounting: boolean = false;
  private apiUrl = 'assets/roleData.json';

  constructor(private http: HttpClient) {}

  getRoleData(role: string): Observable<DataRoleServiceService> {
    return this.http.get<DataRoleServiceService>(this.apiUrl);
  }

  get showRoleHome(): boolean {
    return this.home;
  }

  set showRoleHome(value: boolean) {
    this.home = value;
  }

  get showRoleHrdepartment(): boolean {
    return this.hrdepartment;
  }

  set showRoleHrdepartment(value: boolean) {
    this.hrdepartment = value;
  }

  get showRoleHrmanagement(): boolean {
    return this.hrmanagement;
  }

  set showRoleHrmanagement(value: boolean) {
    this.hrmanagement = value;
  }

  get showRoleAccouting(): boolean {
    return this.accounting;
  }

  set showRoleAccouting(value: boolean) {
    this.accounting = value;
  }
  
  updateRechte(showRoleHome: boolean, showRoleHrdepartment: boolean, showRoleHrmanagement: boolean, howRoleAccouting: boolean): void {
    this.home = showRoleHome;
    this.hrdepartment = showRoleHrdepartment;
    this.hrmanagement = showRoleHrmanagement;
    this.accounting = howRoleAccouting;
  }
}